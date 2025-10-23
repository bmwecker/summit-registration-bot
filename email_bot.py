"""
Email-бот для Aleph Bet Foresight Summit
Полностью дублирует функционал Telegram-бота через email
"""

import os
import imaplib
import email
from email.header import decode_header
import time
import logging
from datetime import datetime
from typing import Optional, Dict
import re
import hashlib

from database import Database
from languages import get_text, LANGUAGE_NAMES
from email_sender import email_sender

logger = logging.getLogger(__name__)

# IMAP настройки
IMAP_HOST = os.getenv("IMAP_HOST", "imap.mail.ru")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")

# Константы
MAX_PARTICIPANTS_PER_DATE = 290

# Инициализация БД
db = Database()


def email_to_telegram_id(email_address: str) -> int:
    """Конвертировать email в уникальный отрицательный telegram_id"""
    # Используем хеш email и делаем отрицательным чтобы отличить от Telegram пользователей
    hash_value = int(hashlib.md5(email_address.lower().encode()).hexdigest()[:8], 16)
    return -hash_value  # Отрицательный ID для email пользователей


class EmailBot:
    """Email-бот с полным функционалом Telegram-бота"""
    
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
            logger.info(f"Connecting to IMAP: {self.imap_host}:{self.imap_port}")
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(self.imap_user, self.imap_password)
            logger.info("IMAP connection successful")
            return mail
        except Exception as e:
            logger.error(f"Failed to connect to IMAP: {e}")
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
        text = text.lower().strip()
        
        # Команда START (только на английском!)
        if text == 'start' or 'start' in text.split():
            return 'start'
        
        # Выбор языка
        if text in ['ru', 'russian', 'русский']:
            return 'lang_ru'
        elif text in ['en', 'english', 'английский']:
            return 'lang_en'
        elif text in ['he', 'hebrew', 'иврит', 'עברית']:
            return 'lang_he'
        
        # Выбор даты (просто цифра)
        if text in ['1', '2', '3']:
            return f'date_{text}'
        
        # Команды меню
        if 'menu' in text or 'меню' in text or 'תפריט' in text:
            return 'menu'
        if 'help' in text or 'помощь' in text or 'עזרה' in text:
            return 'help'
        
        return None
    
    def get_user_by_email(self, email_address: str) -> Optional[Dict]:
        """Получить пользователя по email"""
        telegram_id = email_to_telegram_id(email_address)
        return db.get_user(telegram_id)
    
    def send_welcome(self, to_email: str):
        """Отправить приветствие с выбором языка"""
        subject = "🕊️ Aleph Bet Foresight Summit"
        body = """🕊️ Welcome! Добро пожаловать! ברוכים הבאים!

Please choose language / Выберите язык / בחר שפה:

Reply to this email with ONE of these words:
Ответьте на это письмо ОДНИМ из этих слов:
ענה למייל זה עם אחת המילים הבאות:

• RU (или RUSSIAN)
• EN (или ENGLISH)  
• HE (или HEBREW / עברית)

---

Best regards / С уважением / בברכה,
Aleph Bet Foresight Summit Team
"""
        
        email_sender.send_email(to_email, subject, body)
        logger.info(f"Sent welcome email to {to_email}")
    
    def send_greeting(self, to_email: str, language: str):
        """Отправить приветствие от Шломо с выбором даты"""
        greeting_text = get_text(language, 'greeting')
        
        subject_map = {
            'ru': "✡️ Добро пожаловать!",
            'en': "✡️ Welcome!",
            'he': "✡️ ברוכים הבאים!"
        }
        
        # Получаем 3 доступные даты
        from bot import get_next_three_days, format_date_button
        dates = get_next_three_days()
        
        date_options = []
        for i, date in enumerate(dates):
            date_str = date.strftime('%Y-%m-%d')
            button_text = format_date_button(date, language, i)
            count = db.get_participants_count_by_date(date_str)
            
            if count >= MAX_PARTICIPANTS_PER_DATE:
                button_text += " ❌ FULL"
            else:
                button_text += f" ({count}/{MAX_PARTICIPANTS_PER_DATE})"
            
            date_options.append(f"{i+1}. {button_text}")
        
        instructions_map = {
            'ru': f"\n\n📅 Выберите удобную дату для Zoom-встречи:\n\n" + "\n".join(date_options) + "\n\nОтветьте на это письмо цифрой (1, 2 или 3):",
            'en': f"\n\n📅 Choose a convenient date for the Zoom meeting:\n\n" + "\n".join(date_options) + "\n\nReply to this email with a number (1, 2, or 3):",
            'he': f"\n\n📅 בחר תאריך נוח לפגישת Zoom:\n\n" + "\n".join(date_options) + "\n\nענה למייל זה עם מספר (1, 2 או 3):"
        }
        
        body = greeting_text + instructions_map.get(language, instructions_map['ru'])
        
        email_sender.send_email(
            to_email,
            subject_map.get(language, subject_map['ru']),
            body
        )
        logger.info(f"Sent greeting email to {to_email} in {language}")
    
    def send_confirmation(
        self,
        to_email: str,
        participant_id: int,
        activation_code: str,
        zoom_date: str,
        language: str
    ):
        """Отправить подтверждение регистрации с ID и кодом"""
        confirmation_text = get_text(language, 'meeting_confirmed')
        id_code_text = get_text(
            language,
            'id_and_code',
            participant_id=participant_id,
            activation_code=activation_code
        )
        
        subject_map = {
            'ru': "🎫 Ваша регистрация подтверждена!",
            'en': "🎫 Your registration is confirmed!",
            'he': "🎫 הרישום שלך אושר!"
        }
        
        menu_text_map = {
            'ru': "\n\n📱 Вы можете в любой момент написать:\n• MENU - главное меню\n• HELP - справка",
            'en': "\n\n📱 You can write anytime:\n• MENU - main menu\n• HELP - help",
            'he': "\n\n📱 אתה יכול לכתוב בכל עת:\n• MENU - תפריט ראשי\n• HELP - עזרה"
        }
        
        body = confirmation_text + "\n\n" + id_code_text + menu_text_map.get(language, menu_text_map['ru'])
        
        email_sender.send_email(
            to_email,
            subject_map.get(language, subject_map['ru']),
            body
        )
        logger.info(f"Sent confirmation to {to_email}, ID: {participant_id}")
    
    def send_date_full(self, to_email: str, language: str):
        """Отправить сообщение что дата заполнена"""
        subject_map = {
            'ru': "❌ Дата заполнена",
            'en': "❌ Date is full",
            'he': "❌ התאריך מלא"
        }
        
        body = get_text(language, 'date_full')
        body += "\n\n" + get_text(language, 'choose_date')
        
        email_sender.send_email(
            to_email,
            subject_map.get(language, subject_map['ru']),
            body
        )
    
    def process_incoming_emails(self):
        """Обработка входящих писем"""
        if not self.is_configured():
            logger.warning("IMAP not configured")
            return
        
        mail = self.connect_imap()
        if not mail:
            return
        
        try:
            # Выбираем папку входящих
            mail.select('INBOX')
            logger.info("Connected to INBOX, checking for emails...")
            
            # Ищем непрочитанные письма
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                logger.warning(f"Search failed: {status}")
                return
            
            email_ids = messages[0].split()
            
            if email_ids:
                logger.info(f"Found {len(email_ids)} unread emails")
            
            for email_id in email_ids:
                try:
                    # Получаем письмо
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        continue
                    
                    # Парсим письмо
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Получаем адрес отправителя
                    from_email = msg.get('From')
                    # Извлекаем чистый email
                    from_match = re.search(r'[\w\.-]+@[\w\.-]+', from_email)
                    if from_match:
                        from_email = from_match.group()
                    
                    # Получаем тему
                    subject = decode_header(msg.get('Subject', ''))[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    # Получаем тело письма
                    body = self.get_email_body(msg)
                    
                    logger.info(f"Processing email from {from_email}: {body[:50]}")
                    
                    # Обрабатываем команду
                    self.process_email_command(from_email, body, subject)
                    
                except Exception as e:
                    logger.error(f"Error processing email {email_id}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    continue
        
        finally:
            try:
                mail.close()
                mail.logout()
            except:
                pass
    
    def process_email_command(self, from_email: str, body: str, subject: str):
        """Обработка команды из письма"""
        # Получаем telegram_id для этого email
        telegram_id = email_to_telegram_id(from_email)
        
        # Проверяем, есть ли пользователь в БД
        user = db.get_user(telegram_id)
        
        command = self.parse_command(body)
        
        logger.info(f"Parsed command: {command} for user: {user}")
        
        if not command:
            # Если не распознали команду, отправляем помощь
            language = user.get('language', 'ru') if user else 'ru'
            self.send_help(from_email, language)
            return
        
        # Команда START
        if command == 'start':
            if user:
                # Пользователь уже есть - отправляем меню
                self.send_menu(from_email, user)
            else:
                # Новый пользователь - отправляем приветствие с выбором языка
                self.send_welcome(from_email)
            return
        
        # Выбор языка
        if command.startswith('lang_'):
            language = command.split('_')[1]
            
            if user:
                # Обновляем язык существующего пользователя
                db.set_user_language(telegram_id, language)
                logger.info(f"Updated language for {from_email} to {language}")
                self.send_greeting(from_email, language)
            else:
                # Создаём нового пользователя (пока без даты и ID)
                username = from_email.split('@')[0]
                first_name = username
                
                # Создаём временного пользователя с выбранным языком
                db.create_user(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    participant_type='participant',
                    language=language
                )
                
                # Сохраняем email
                db.update_user_email(telegram_id, from_email)
                
                logger.info(f"Created new user for {from_email} with language {language}")
                
                # Отправляем приветствие с выбором даты
                self.send_greeting(from_email, language)
            return
        
        # Выбор даты
        if command.startswith('date_'):
            if not user:
                # Пользователь должен сначала выбрать язык
                self.send_welcome(from_email)
                return
            
            language = user.get('language', 'ru')
            date_index = int(command.split('_')[1]) - 1  # 1 -> 0, 2 -> 1, 3 -> 2
            
            # Получаем даты
            from bot import get_next_three_days
            dates = get_next_three_days()
            
            if date_index < 0 or date_index >= len(dates):
                self.send_help(from_email, language)
                return
            
            selected_date = dates[date_index]
            date_str = selected_date.strftime('%Y-%m-%d')
            
            # Проверяем лимит
            count = db.get_participants_count_by_date(date_str)
            if count >= MAX_PARTICIPANTS_PER_DATE:
                self.send_date_full(from_email, language)
                return
            
            # Обновляем дату
            db.update_zoom_date(telegram_id, date_str)
            
            # Получаем обновлённого пользователя
            user = db.get_user(telegram_id)
            
            logger.info(f"Set date {date_str} for {from_email}, ID: {user['participant_id']}")
            
            # Отправляем подтверждение с ID и кодом
            self.send_confirmation(
                from_email,
                user['participant_id'],
                user['activation_code'],
                date_str,
                language
            )
            return
        
        # Команда MENU
        if command == 'menu':
            if not user:
                self.send_welcome(from_email)
                return
            
            self.send_menu(from_email, user)
            return
        
        # Команда HELP
        if command == 'help':
            language = user.get('language', 'ru') if user else 'ru'
            self.send_help(from_email, language)
            return
    
    def send_help(self, to_email: str, language: str = 'ru'):
        """Отправить справку"""
        help_texts = {
            'ru': """📖 Справка по Email-боту

Доступные команды (отвечайте на письма этими словами):

• START - начать регистрацию
• RU / EN / HE - выбрать язык
• 1 / 2 / 3 - выбрать дату (после выбора языка)
• MENU - главное меню
• HELP - эта справка

Вы также можете просто отвечать на письма, следуя инструкциям.

С уважением,
Aleph Bet Foresight Summit
""",
            'en': """📖 Email Bot Help

Available commands (reply to emails with these words):

• START - begin registration
• RU / EN / HE - choose language
• 1 / 2 / 3 - choose date (after language selection)
• MENU - main menu
• HELP - this help

You can also simply reply to emails following the instructions.

Best regards,
Aleph Bet Foresight Summit
""",
            'he': """📖 עזרה עבור Email בוט

פקודות זמינות (השב למיילים עם המילים הבאות):

• START - התחל רישום
• RU / EN / HE - בחר שפה
• 1 / 2 / 3 - בחר תאריך (אחרי בחירת שפה)
• MENU - תפריט ראשי
• HELP - עזרה זו

אתה יכול גם פשוט להשיב למיילים בעקבות ההוראות.

בברכה,
Aleph Bet Foresight Summit
"""
        }
        
        email_sender.send_email(
            to_email,
            "📖 Help / Справка / עזרה",
            help_texts.get(language, help_texts['ru'])
        )
    
    def send_menu(self, to_email: str, user: Dict):
        """Отправить главное меню"""
        language = user.get('language', 'ru')
        
        menu_texts = {
            'ru': f"""📱 Главное меню

🎫 Ваш ID: №{user.get('participant_id', 'N/A')}
🔑 Ваш код активации: {user.get('activation_code', 'N/A')}
📅 Дата встречи: {user.get('zoom_date', 'не указана')}

Вы можете писать:
• HELP - справка по командам

Если нужно изменить данные или получить инструкции - напишите нам!

С уважением,
Команда Aleph Bet Foresight Summit
""",
            'en': f"""📱 Main Menu

🎫 Your ID: №{user.get('participant_id', 'N/A')}
🔑 Your activation code: {user.get('activation_code', 'N/A')}
📅 Meeting date: {user.get('zoom_date', 'not set')}

You can write:
• HELP - help with commands

If you need to change data or get instructions - write to us!

Best regards,
Aleph Bet Foresight Summit Team
""",
            'he': f"""📱 תפריט ראשי

🎫 ה-ID שלך: №{user.get('participant_id', 'N/A')}
🔑 קוד ההפעלה שלך: {user.get('activation_code', 'N/A')}
📅 תאריך הפגישה: {user.get('zoom_date', 'לא נקבע')}

אתה יכול לכתוב:
• HELP - עזרה עם פקודות

אם אתה צריך לשנות נתונים או לקבל הוראות - כתוב לנו!

בברכה,
צוות Aleph Bet Foresight Summit
"""
        }
        
        email_sender.send_email(
            to_email,
            "📱 Menu / Меню / תפריט",
            menu_texts.get(language, menu_texts['ru'])
        )
    
    def run(self, interval: int = 30):
        """Запустить бота с проверкой каждые N секунд"""
        logger.info("Email bot started")
        
        while True:
            try:
                self.process_incoming_emails()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in email bot loop: {e}")
                import traceback
                logger.error(traceback.format_exc())
                time.sleep(interval)


def start_email_bot():
    """Запустить email-бота"""
    bot = EmailBot()
    
    if not bot.is_configured():
        logger.warning("Email bot not configured (missing IMAP settings)")
        return
    
    logger.info("Starting email bot...")
    bot.run()


if __name__ == '__main__':
    # Настройка логирования
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    start_email_bot()
