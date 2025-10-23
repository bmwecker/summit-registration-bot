"""
Email-бот для Aleph Bet Foresight Summit
Полностью дублирует функционал Telegram/WhatsApp-бота через email
"""

import os
import imaplib
import email
from email.header import decode_header
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
import re
import hashlib

from database import Database
from email_sender import email_sender

logger = logging.getLogger(__name__)

# IMAP настройки
IMAP_HOST = os.getenv("IMAP_HOST", "imap.mail.ru")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")

# Константы
MAX_PARTICIPANTS_PER_DATE = 290

# Тексты ТОЧНО как в WhatsApp боте
TEXTS = {
    'ru': {
        'welcome': '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1️⃣ Русский 🇷🇺\n2️⃣ English 🇬🇧\n3️⃣ עברית 🇮🇱\n\nОтветьте на это письмо цифрой или словом (RU/EN/HE)',
        'greeting': '✡️ Поздравляем — вы со своим народом!\nШалом! Меня зовут Шломо\n\n🎉 Вы приглашены на Zoom-встречу с оргкомитетом для знакомства с организаторами. Также на ней, вы сможете выбрать ту миссию, которая Вам по душе!\n\nКогда Вы хотите присоединиться к ZOOM встрече? Сегодня, завтра или послезавтра?',
        'choose_date': '📅 Выберите удобную дату для Zoom-встречи:',
        'date_full': '❌ К сожалению, на эту дату все места заняты. Пожалуйста, выберите другую дату.',
        'meeting_confirmed': 'Отлично! Мы будем очень рады Вас видеть на нашей первой встрече!',
        'id_and_code': '🎫 Ваш ID: №{participant_id}\n📲 Уникальный код для активации ID: {activation_code}\n\n⚠️ Для активации Вашего ID необходимо присутствовать на Zoom-встрече.\nПосле активации можно выбрать форму участия в саммите.',
        'main_menu': '📱 Главное меню:\n\n1️⃣ Напомнить номер ID\n2️⃣ Напомнить код активации\n3️⃣ Напомнить дату встречи\n4️⃣ Перенести встречу\n5️⃣ Как активировать ID?\n6️⃣ Изменить язык\n\n_Ответьте номером (1-6) или командой (MENU, HELP)_',
        'your_id': '📜 Ваш ID: №{participant_id}',
        'your_code': '🔑 Ваш код активации: {activation_code}',
        'your_date': '📅 Ваша дата Zoom-встречи: {zoom_date}',
        'how_to_activate': '❓ Как активировать ID?\n\nВ день ZOOM встречи, Вы получите ссылку на онлайн встречу, и точное время её проведения, на которой Вы должны будете отправить свой уникальный код в общий чат.\n\nПо окончанию ZOOM встречи Ваш ID будет активирован.',
        'help': '📖 Справка\n\nДоступные команды:\n• START - начать регистрацию\n• MENU - главное меню\n• 1-6 - выбрать пункт меню\n• HELP - эта справка',
        'today': 'Сегодня',
        'tomorrow': 'Завтра',
        'day_after_tomorrow': 'Послезавтра'
    },
    'en': {
        'welcome': '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1️⃣ Русский 🇷🇺\n2️⃣ English 🇬🇧\n3️⃣ עברית 🇮🇱\n\nReply with number or word (RU/EN/HE)',
        'greeting': '✡️ Congratulations — you are with your people!\nShalom! My name is Shlomo\n\n🎉 You are invited to a Zoom meeting with the organizing committee to meet the organizers. You will also be able to choose the mission that suits you!\n\nWhen would you like to join the ZOOM meeting? Today, tomorrow, or the day after tomorrow?',
        'choose_date': '📅 Choose a convenient date for the Zoom meeting:',
        'date_full': '❌ Unfortunately, all places for this date are taken. Please choose another date.',
        'meeting_confirmed': 'Great! We will be very happy to see you at our first meeting!',
        'id_and_code': '🎫 Your ID: №{participant_id}\n📲 Unique activation code: {activation_code}\n\n⚠️ You must attend the Zoom meeting to activate your ID.\nAfter activation, you can choose your form of participation in the summit.',
        'main_menu': '📱 Main menu:\n\n1️⃣ Remind ID number\n2️⃣ Remind activation code\n3️⃣ Remind meeting date\n4️⃣ Reschedule meeting\n5️⃣ How to activate ID?\n6️⃣ Change language\n\n_Reply with number (1-6) or command (MENU, HELP)_',
        'your_id': '📜 Your ID: №{participant_id}',
        'your_code': '🔑 Your activation code: {activation_code}',
        'your_date': '📅 Your Zoom meeting date: {zoom_date}',
        'how_to_activate': '❓ How to activate ID?\n\nOn the day of the ZOOM meeting, you will receive a link to the online meeting and the exact time it will take place. You must send your unique code to the general chat.\n\nAfter the ZOOM meeting is over, your ID will be activated.',
        'help': '📖 Help\n\nAvailable commands:\n• START - start registration\n• MENU - main menu\n• 1-6 - select menu item\n• HELP - this help',
        'today': 'Today',
        'tomorrow': 'Tomorrow',
        'day_after_tomorrow': 'Day after tomorrow'
    },
    'he': {
        'welcome': '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1️⃣ Русский 🇷🇺\n2️⃣ English 🇬🇧\n3️⃣ עברית 🇮🇱\n\n(HE/EN/RU) ענה עם מספר או מילה',
        'greeting': '✡️ !ברוכים הבאים — אתם עם העם שלכם\n!שלום! שמי שלמה\n\n🎉 אתם מוזמנים לפגישת Zoom עם הוועדה המארגנת כדי להכיר את המארגנים. תוכלו גם לבחור את המשימה המתאימה לכם!\n\nמתי תרצו להצטרף לפגישת ZOOM? היום, מחר או מחרתיים?',
        'choose_date': '📅 :בחרו תאריך נוח לפגישת Zoom',
        'date_full': '❌ למרבה הצער, כל המקומות לתאריך זה תפוסים. אנא בחרו תאריך אחר.',
        'meeting_confirmed': '!מצוין! נשמח מאוד לראותכם בפגישה הראשונה שלנו',
        'id_and_code': '🎫 ה-ID שלך: №{participant_id}\n📲 :קוד הפעלה ייחודי {activation_code}\n\n⚠️ עליך להשתתף בפגישת Zoom כדי להפעיל את ה-ID שלך.\n.לאחר ההפעלה, תוכל לבחור את צורת ההשתתפות שלך בפסגה',
        'main_menu': '📱 :תפריט ראשי\n\n1️⃣ הזכר מספר ID\n2️⃣ הזכר קוד הפעלה\n3️⃣ הזכר תאריך פגישה\n4️⃣ קבע מחדש פגישה\n5️⃣ ?כיצד להפעיל ID\n6️⃣ שנה שפה\n\n_(MENU ,HELP) ענה במספר (1-6) או פקודה_',
        'your_id': '📜 ה-ID שלך: №{participant_id}',
        'your_code': '🔑 קוד ההפעלה שלך: {activation_code}',
        'your_date': '📅 תאריך פגישת Zoom שלך: {zoom_date}',
        'how_to_activate': '❓ ?כיצד להפעיל ID\n\nביום פגישת ZOOM, תקבל קישור לפגישה המקוונת והשעה המדויקת שבה היא תתקיים. עליך לשלוח את הקוד הייחודי שלך לצ\'אט הכללי.\n\n.בתום פגישת ZOOM, ה-ID שלך יופעל',
        'help': '📖 עזרה\n\n:פקודות זמינות\n• START - התחל רישום\n• MENU - תפריט ראשי\n• 1-6 - בחר פריט תפריט\n• HELP - עזרה זו',
        'today': 'היום',
        'tomorrow': 'מחר',
        'day_after_tomorrow': 'מחרתיים'
    }
}

# Названия дней недели
WEEKDAY_NAMES = {
    'ru': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
    'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'he': ['יום שני', 'יום שלישי', 'יום רביעי', 'יום חמישי', 'יום שישי', 'שבת', 'יום ראשון']
}

# Инициализация БД
db = Database()

# Состояние пользователей (в памяти)
user_states = {}


def email_to_telegram_id(email_address: str) -> int:
    """Генерирует уникальный отрицательный telegram_id из email"""
    hash_object = hashlib.sha256(email_address.lower().encode())
    hex_dig = hash_object.hexdigest()
    return -int(hex_dig[:15], 16)


def get_next_three_days():
    """Получение следующих трёх дней (пропуск пятницы и субботы)"""
    days = []
    current = datetime.now()
    
    while len(days) < 3:
        day_of_week = current.weekday()
        # Пропускаем пятницу (4) и субботу (5)
        if day_of_week not in [4, 5]:
            days.append(current)
        current += timedelta(days=1)
    
    return days


def format_date(date):
    """Форматирование даты DD.MM.YYYY"""
    return date.strftime('%d.%m.%Y')


def format_date_for_db(date):
    """Форматирование даты для БД YYYY-MM-DD"""
    return date.strftime('%Y-%m-%d')


def get_weekday_name(date, language):
    """Получение названия дня недели"""
    day_index = date.weekday()
    return WEEKDAY_NAMES[language][day_index]


class EmailBot:
    """Email-бот с полным функционалом"""
    
    def __init__(self):
        self.imap_host = IMAP_HOST
        self.imap_port = IMAP_PORT
        self.imap_user = IMAP_USER
        self.imap_password = IMAP_PASSWORD
        self.processed_emails = set()
    
    def is_configured(self) -> bool:
        """Проверка настройки IMAP"""
        return bool(self.imap_user and self.imap_password)
    
    def connect_imap(self):
        """Подключение к IMAP серверу"""
        try:
            logger.info(f"[EMAIL] Connecting to IMAP: {self.imap_host}:{self.imap_port}")
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(self.imap_user, self.imap_password)
            logger.info("[EMAIL] IMAP connection successful")
            return mail
        except Exception as e:
            logger.error(f"[EMAIL] Failed to connect to IMAP: {e}")
            return None
    
    def get_email_body(self, msg) -> str:
        """Извлечь текст письма"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                pass
        
        return body.strip()
    
    def parse_command(self, text: str) -> Optional[str]:
        """Распознать команду в тексте письма"""
        if not text:
            return None
        
        logger.info(f"[EMAIL] Raw text: {repr(text[:200])}")
        
        # Берем только первую непустую строку
        lines = text.strip().split('\n')
        first_line = ''
        for line in lines:
            clean_line = line.strip()
            # Пропускаем пустые строки, цитаты (>), служебные заголовки
            if clean_line and not clean_line.startswith('>') and not clean_line.startswith('On ') and not clean_line.startswith('It looks like'):
                first_line = clean_line
                break
        
        if not first_line:
            return None
        
        logger.info(f"[EMAIL] First line: {repr(first_line)}")
        
        # Удаляем маркеры списков
        first_line = re.sub(r'^[•\-\*\+]\s+', '', first_line)
        # Удаляем скобки с пояснениями
        first_line = re.sub(r'\s*\(.*?\)\s*', ' ', first_line).strip()
        
        # Проверяем иврит ДО lowercase
        if 'עברית' in first_line:
            logger.info("[EMAIL] Command: lang_he (Hebrew detected)")
            return 'lang_he'
        
        # Lowercase для остальных
        command = first_line.lower().strip()
        
        logger.info(f"[EMAIL] Cleaned command: {repr(command)}")
        
        # START - точное совпадение
        if command == 'start' or command == 'старт':
            logger.info("[EMAIL] Command: start")
            return 'start'
        
        # Даты - ТОЛЬКО цифры
        if command in ['1', '2', '3']:
            logger.info(f"[EMAIL] Command: date/menu_{command}")
            return command  # Вернем просто цифру, контекст определит значение
        
        # Пункты меню 4-6
        if command in ['4', '5', '6']:
            logger.info(f"[EMAIL] Command: menu_{command}")
            return command
        
        # Языки - ТОЧНОЕ совпадение
        if command in ['ru', 'russian', 'русский']:
            logger.info("[EMAIL] Command: lang_ru")
            return 'lang_ru'
        if command in ['en', 'english', 'английский']:
            logger.info("[EMAIL] Command: lang_en")
            return 'lang_en'
        if command in ['he', 'hebrew', 'иврит']:
            logger.info("[EMAIL] Command: lang_he")
            return 'lang_he'
        
        # MENU и HELP
        if 'menu' in command or 'меню' in command or 'תפריט' in first_line:
            logger.info("[EMAIL] Command: menu")
            return 'menu'
        if 'help' in command or 'помощь' in command or 'עזרה' in first_line:
            logger.info("[EMAIL] Command: help")
            return 'help'
        
        logger.warning(f"[EMAIL] Command not recognized: {repr(command)}")
        return None
    
    def get_user_by_email(self, email_address: str) -> Optional[Dict]:
        """Получить пользователя по email"""
        telegram_id = email_to_telegram_id(email_address)
        return db.get_user(telegram_id)
    
    def get_dates_message(self, language: str) -> str:
        """Сформировать сообщение с датами"""
        dates = get_next_three_days()
        texts = TEXTS[language]
        relative = [texts['today'], texts['tomorrow'], texts['day_after_tomorrow']]
        emojis = ['1️⃣', '2️⃣', '3️⃣']
        
        message = texts['greeting'] + '\n\n' + texts['choose_date'] + '\n\n'
        
        for i, date in enumerate(dates):
            weekday = get_weekday_name(date, language)
            formatted = format_date(date)
            count = db.get_participants_count_by_date(format_date_for_db(date))
            message += f"{emojis[i]} {relative[i]} ({weekday}) - {formatted} ({count}/{MAX_PARTICIPANTS_PER_DATE})\n"
        
        message += "\nОтветьте цифрой (1, 2 или 3)" if language == 'ru' else "\nReply with number (1, 2, or 3)" if language == 'en' else "\n(3 ,2 ,1) ענה במספר"
        
        return message
    
    def send_email(self, to_email: str, subject: str, body: str):
        """Отправить email"""
        email_sender.send_email(to_email, subject, body)
        logger.info(f"[EMAIL] Sent email to {to_email}: {subject}")
    
    def process_email_command(self, from_email: str, body: str, subject: str):
        """Обработка команды из email"""
        telegram_id = email_to_telegram_id(from_email)
        user = self.get_user_by_email(from_email)
        state = user_states.get(from_email, {'step': 'start'})
        command = self.parse_command(body)
        
        logger.info(f"[EMAIL] From: {from_email}, Command: {command}, State: {state['step']}, User exists: {bool(user)}")
        
        if not command:
            # Не распознали команду
            texts = TEXTS[user['language'] if user else 'ru']
            self.send_email(from_email, "📖 Help / Справка", texts['help'])
            return
        
        # Команда START
        if command == 'start':
            if user:
                # Показать меню для существующего пользователя
                texts = TEXTS[user['language']]
                menu_text = texts['main_menu']
                self.send_email(from_email, "📱 Menu / Меню", menu_text)
                user_states[from_email] = {'step': 'registered', 'language': user['language']}
            else:
                # Новый пользователь - выбор языка
                self.send_email(from_email, "🕊️ Welcome / Добро пожаловать", TEXTS['ru']['welcome'])
                user_states[from_email] = {'step': 'choosing_language'}
            return
        
        # Если пользователя нет и это не START - показать welcome
        if not user and state['step'] == 'start':
            self.send_email(from_email, "🕊️ Welcome / Добро пожаловать", TEXTS['ru']['welcome'])
            user_states[from_email] = {'step': 'choosing_language'}
            return
        
        # Выбор языка - обрабатываем и цифры (1,2,3) и слова (lang_ru, ru, russian)
        if state['step'] == 'choosing_language':
            language = None
            
            # Цифры: 1=ru, 2=en, 3=he
            if command == '1':
                language = 'ru'
            elif command == '2':
                language = 'en'
            elif command == '3':
                language = 'he'
            # Команды lang_*
            elif command.startswith('lang_'):
                language = command.split('_')[1]
            
            if language:
                logger.info(f"[EMAIL] Language selected: {language}")
            
            if language:
                if not user:
                    # Создаем нового пользователя
                    first_name = from_email.split('@')[0]
                    participant_id, activation_code = db.create_user(
                        telegram_id=telegram_id,
                        username=from_email,
                        first_name=first_name,
                        participant_type='email_participant',
                        language=language
                    )
                    db.update_user_email(telegram_id, from_email)
                    user = db.get_user(telegram_id)
                    logger.info(f"[EMAIL] User created: ID={participant_id}, Code={activation_code}")
                else:
                    # Обновляем язык для существующего пользователя
                    db.set_user_language(telegram_id, language)
                    db.update_user_email(telegram_id, from_email)
                    user = db.get_user(telegram_id)
                
                # Отправляем список дат
                dates_message = self.get_dates_message(language)
                subject_map = {
                    'ru': '✡️ Добро пожаловать!',
                    'en': '✡️ Welcome!',
                    'he': '✡️ ברוכים הבאים!'
                }
                self.send_email(from_email, subject_map[language], dates_message)
                user_states[from_email] = {'step': 'choosing_date', 'language': language}
                return
            else:
                # Не распознали язык - показываем help
                texts = TEXTS['ru']
                self.send_email(from_email, "📖 Help / Справка", texts['help'])
                return
        
        # Выбор даты
        if state['step'] == 'choosing_date' and command in ['1', '2', '3']:
            if not user:
                self.send_email(from_email, "🕊️ Welcome", TEXTS['ru']['welcome'])
                user_states[from_email] = {'step': 'choosing_language'}
                return
            
            date_index = int(command) - 1
            dates = get_next_three_days()
            
            if 0 <= date_index < len(dates):
                selected_date = format_date_for_db(dates[date_index])
                count = db.get_participants_count_by_date(selected_date)
                
                texts = TEXTS[user['language']]
                
                if count >= MAX_PARTICIPANTS_PER_DATE:
                    # Дата заполнена
                    full_message = texts['date_full'] + "\n\n" + self.get_dates_message(user['language'])
                    self.send_email(from_email, "❌ Date full / Дата заполнена", full_message)
                    return
                
                # Обновляем дату
                db.update_zoom_date(telegram_id, selected_date)
                user = db.get_user(telegram_id)
                
                # Отправляем подтверждение с ID и кодом
                confirmation = texts['meeting_confirmed'] + "\n\n" + texts['id_and_code'].replace('{participant_id}', str(user['participant_id'])).replace('{activation_code}', user['activation_code'])
                subject_map = {
                    'ru': '🎫 Регистрация подтверждена!',
                    'en': '🎫 Registration confirmed!',
                    'he': '🎫 !הרישום אושר'
                }
                self.send_email(from_email, subject_map[user['language']], confirmation)
                
                # Отправляем меню
                menu_text = texts['main_menu']
                self.send_email(from_email, "📱 Menu / Меню", menu_text)
                
                user_states[from_email] = {'step': 'registered', 'language': user['language']}
                logger.info(f"[EMAIL] Date selected: {selected_date}")
            return
        
        # Обработка меню (пункты 1-6) - только для зарегистрированных
        if user and state['step'] == 'registered' and command in ['1', '2', '3', '4', '5', '6']:
            texts = TEXTS[user['language']]
            menu_choice = int(command)
            
            if menu_choice == 1:
                # Напомнить ID
                text = texts['your_id'].replace('{participant_id}', str(user['participant_id']))
                self.send_email(from_email, "📜 Your ID", text)
                logger.info(f"[EMAIL] Reminded ID")
                return
            
            if menu_choice == 2:
                # Напомнить код
                text = texts['your_code'].replace('{activation_code}', user['activation_code'])
                self.send_email(from_email, "🔑 Activation code / Код активации", text)
                logger.info(f"[EMAIL] Reminded activation code")
                return
            
            if menu_choice == 3:
                # Напомнить дату
                date_text = format_date(datetime.strptime(user['zoom_date'], '%Y-%m-%d')) if user.get('zoom_date') else 'не выбрана'
                text = texts['your_date'].replace('{zoom_date}', date_text)
                self.send_email(from_email, "📅 Meeting date / Дата встречи", text)
                logger.info(f"[EMAIL] Reminded meeting date")
                return
            
            if menu_choice == 4:
                # Перенести встречу
                dates_message = self.get_dates_message(user['language'])
                subject_map = {
                    'ru': '📅 Выберите новую дату',
                    'en': '📅 Choose new date',
                    'he': '📅 בחר תאריך חדש'
                }
                self.send_email(from_email, subject_map[user['language']], dates_message)
                user_states[from_email] = {'step': 'choosing_date', 'language': user['language']}
                logger.info(f"[EMAIL] Rescheduling meeting")
                return
            
            if menu_choice == 5:
                # Как активировать ID
                self.send_email(from_email, "❓ How to activate / Как активировать", texts['how_to_activate'])
                logger.info(f"[EMAIL] Showed activation info")
                return
            
            if menu_choice == 6:
                # Изменить язык
                self.send_email(from_email, "🌍 Change language / Изменить язык", TEXTS['ru']['welcome'])
                user_states[from_email] = {'step': 'choosing_language'}
                logger.info(f"[EMAIL] Changing language")
                return
        
        # Команда MENU
        if command == 'menu':
            if user:
                texts = TEXTS[user['language']]
                self.send_email(from_email, "📱 Menu / Меню", texts['main_menu'])
                user_states[from_email] = {'step': 'registered', 'language': user['language']}
            else:
                self.send_email(from_email, "🕊️ Welcome", TEXTS['ru']['welcome'])
                user_states[from_email] = {'step': 'choosing_language'}
            return
        
        # Команда HELP
        if command == 'help':
            texts = TEXTS[user['language'] if user else 'ru']
            self.send_email(from_email, "📖 Help / Справка", texts['help'])
            return
        
        # Если ничего не распознали
        texts = TEXTS[user['language'] if user else 'ru']
        self.send_email(from_email, "📖 Help / Справка", texts['help'])
    
    def process_incoming_emails(self):
        """Обработка входящих писем"""
        if not self.is_configured():
            logger.warning("[EMAIL] IMAP not configured")
            return
        
        mail = self.connect_imap()
        if not mail:
            return
        
        try:
            mail.select('INBOX')
            logger.info("[EMAIL] Connected to INBOX, checking for emails...")
            
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                logger.warning(f"[EMAIL] Search failed: {status}")
                return
            
            email_ids = messages[0].split()
            
            if not email_ids:
                logger.info("[EMAIL] No new emails")
                return
            
            logger.info(f"[EMAIL] Found {len(email_ids)} new emails")
            
            for email_id in email_ids:
                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        continue
                    
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            
                            # Получаем отправителя
                            from_email = msg.get('From', '')
                            if '<' in from_email:
                                from_email = from_email.split('<')[1].split('>')[0]
                            
                            # Получаем тему
                            subject = msg.get('Subject', '')
                            if subject:
                                decoded = decode_header(subject)[0]
                                if isinstance(decoded[0], bytes):
                                    subject = decoded[0].decode(decoded[1] or 'utf-8')
                                else:
                                    subject = decoded[0]
                            
                            # Получаем тело письма
                            body = self.get_email_body(msg)
                            
                            if not body:
                                continue
                            
                            logger.info(f"[EMAIL] Processing email from {from_email}")
                            
                            # Обрабатываем команду
                            self.process_email_command(from_email, body, subject)
                            
                except Exception as e:
                    logger.error(f"[EMAIL] Error processing email: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"[EMAIL] Error in process_incoming_emails: {e}")
        finally:
            try:
                mail.close()
                mail.logout()
            except:
                pass
    
    def run(self):
        """Запуск бота"""
        logger.info("[EMAIL] Email bot started")
        
        while True:
            try:
                self.process_incoming_emails()
            except Exception as e:
                logger.error(f"[EMAIL] Error in email bot: {e}")
            
            time.sleep(10)  # Проверяем каждые 10 секунд


def start_email_bot():
    """Запуск Email бота"""
    bot = EmailBot()
    if not bot.is_configured():
        logger.warning("[EMAIL] Email bot not configured - skipping")
        return
    
    logger.info("[EMAIL] Starting Email bot...")
    bot.run()


if __name__ == "__main__":
    start_email_bot()
