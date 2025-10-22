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

from database import Database
from languages import get_text, LANGUAGE_NAMES
from email_sender import email_sender

logger = logging.getLogger(__name__)

# IMAP настройки
IMAP_HOST = os.getenv("IMAP_HOST", "imap.mail.ru")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")

# Инициализация БД
db = Database()


class EmailBot:
    """Email-бот с полным функционалом Telegram-бота"""
    
    def __init__(self):
        self.imap_host = IMAP_HOST
        self.imap_port = IMAP_PORT
        self.imap_user = IMAP_USER
        self.imap_password = IMAP_PASSWORD
        self.processed_emails = set()  # Чтобы не обрабатывать дважды
    
    def is_configured(self) -> bool:
        """Проверка настройки IMAP"""
        return bool(self.imap_user and self.imap_password)
    
    def connect_imap(self):
        """Подключение к IMAP серверу"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(self.imap_user, self.imap_password)
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
        
        # Команды на русском
        if 'старт' in text or 'начать' in text or 'регистрация' in text:
            return 'start'
        elif 'русский' in text or 'russian' in text:
            return 'lang_ru'
        elif 'английский' in text or 'english' in text or 'англ' in text:
            return 'lang_en'
        elif 'иврит' in text or 'hebrew' in text:
            return 'lang_he'
        elif 'сегодня' in text or 'today' in text:
            return 'date_today'
        elif 'завтра' in text or 'tomorrow' in text:
            return 'date_tomorrow'
        elif 'послезавтра' in text or 'day after' in text:
            return 'date_after'
        elif 'меню' in text or 'menu' in text:
            return 'menu'
        elif 'помощь' in text or 'help' in text:
            return 'help'
        
        # Попытка распознать код активации (6 цифр)
        code_match = re.search(r'\b\d{6}\b', text)
        if code_match:
            return f'code_{code_match.group()}'
        
        return None
    
    def send_welcome(self, to_email: str, first_name: str = ""):
        """Отправить приветствие и выбор языка"""
        subject = "🕊️ Aleph Bet Foresight Summit"
        body = f"""Шалом{f', {first_name}' if first_name else ''}!

Добро пожаловать на регистрацию Aleph Bet Foresight Summit!

🌍 Пожалуйста, выберите язык / Please choose language / בחר שפה:

Ответьте на это письмо одним словом:
1. РУССКИЙ (или RU)
2. ENGLISH (или EN)
3. עברית (или HE)

---

После выбора языка вы получите дальнейшие инструкции.

С уважением,
Команда Aleph Bet Foresight Summit
🕊️
"""
        
        email_sender.send_email(to_email, subject, body)
        logger.info(f"Sent welcome email to {to_email}")
    
    def send_greeting(self, to_email: str, language: str, first_name: str = ""):
        """Отправить приветствие от Шломо"""
        greeting_text = get_text(language, 'greeting')
        
        subject_map = {
            'ru': "✡️ Добро пожаловать на Aleph Bet Summit!",
            'en': "✡️ Welcome to Aleph Bet Summit!",
            'he': "✡️ ברוכים הבאים ל-Aleph Bet Summit!"
        }
        
        # Получаем 3 доступные даты
        from bot import get_next_three_days, format_date_button
        dates = get_next_three_days()
        
        date_options = "\n".join([
            f"{i+1}. {format_date_button(date, language, i)}"
            for i, date in enumerate(dates)
        ])
        
        instructions_map = {
            'ru': f"\n\nОтветьте на это письмо, указав номер желаемой даты (1, 2 или 3):\n\n{date_options}",
            'en': f"\n\nReply to this email with the number of your preferred date (1, 2, or 3):\n\n{date_options}",
            'he': f"\n\nענה למייל זה עם מספר התאריך המועדף (1, 2 או 3):\n\n{date_options}"
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
        first_name: str,
        participant_id: int,
        activation_code: str,
        zoom_date: str,
        language: str
    ):
        """Отправить подтверждение регистрации с ID и кодом"""
        email_sender.send_registration_confirmation(
            to_email,
            first_name,
            participant_id,
            activation_code,
            zoom_date,
            language
        )
        logger.info(f"Sent confirmation to {to_email}, ID: {participant_id}")
    
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
            
            # Ищем непрочитанные письма
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                return
            
            email_ids = messages[0].split()
            
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
                    continue
        
        finally:
            mail.close()
            mail.logout()
    
    def process_email_command(self, from_email: str, body: str, subject: str):
        """Обработка команды из письма"""
        # Проверяем, есть ли пользователь в БД
        user = self.get_user_by_email(from_email)
        
        command = self.parse_command(body)
        
        if not command:
            # Если не распознали команду, отправляем помощь
            self.send_help(from_email, user.get('language', 'ru') if user else 'ru')
            return
        
        # Команда START
        if command == 'start':
            if user:
                # Пользователь уже есть
                self.send_menu(from_email, user)
            else:
                # Новый пользователь
                self.send_welcome(from_email)
            return
        
        # Выбор языка
        if command.startswith('lang_'):
            language = command.split('_')[1]
            
            if user:
                # Обновляем язык
                db.set_user_language(user['telegram_id'], language)
                self.send_menu(from_email, user)
            else:
                # Создаём пользователя (временно без ID)
                # Сохраняем email в отдельной таблице или используем email как идентификатор
                # Для простоты пока отправляем приветствие
                first_name = from_email.split('@')[0]
                self.send_greeting(from_email, language, first_name)
            return
        
        # TODO: Добавить обработку выбора даты, меню и т.д.
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Получить пользователя по email"""
        # TODO: Добавить поиск по email в database.py
        return None
    
    def send_help(self, to_email: str, language: str = 'ru'):
        """Отправить справку"""
        help_texts = {
            'ru': """📖 Справка по Email-боту

Доступные команды (отвечайте на письма этими словами):

• СТАРТ - начать регистрацию
• РУССКИЙ / ENGLISH / עברית - выбрать язык
• МЕНЮ - главное меню
• ПОМОЩЬ - эта справка

Вы также можете просто отвечать на письма, следуя инструкциям.

С уважением,
Aleph Bet Foresight Summit
""",
            'en': """📖 Email Bot Help

Available commands (reply to emails with these words):

• START - begin registration
• RUSSIAN / ENGLISH / HEBREW - choose language
• MENU - main menu
• HELP - this help

You can also simply reply to emails following the instructions.

Best regards,
Aleph Bet Foresight Summit
""",
            'he': """📖 עזרה עבור Email בוט

פקודות זמינות (השב למיילים עם המילים הבאות):

• START - התחל רישום
• RUSSIAN / ENGLISH / HEBREW - בחר שפה
• MENU - תפריט ראשי
• HELP - עזרה זו

אתה יכול גם פשוט להשיב למיילים בעקבות ההוראות.

בברכה,
Aleph Bet Foresight Summit
"""
        }
        
        email_sender.send_email(
            to_email,
            "📖 Справка / Help / עזרה",
            help_texts.get(language, help_texts['ru'])
        )
    
    def send_menu(self, to_email: str, user: Dict):
        """Отправить главное меню"""
        language = user.get('language', 'ru')
        
        menu_texts = {
            'ru': f"""📱 Главное меню

Ваш ID: №{user.get('participant_id', 'N/A')}
Ваш код активации: {user.get('activation_code', 'N/A')}
Дата встречи: {user.get('zoom_date', 'не указана')}

Доступные команды:
1. ID - напомнить ID
2. КОД - напомнить код активации
3. ДАТА - напомнить дату встречи
4. ИНСТРУКЦИЯ - инструкция по Zoom
5. ПОМОЩЬ - справка

Ответьте на это письмо с нужной командой.
""",
            'en': f"""📱 Main Menu

Your ID: №{user.get('participant_id', 'N/A')}
Your activation code: {user.get('activation_code', 'N/A')}
Meeting date: {user.get('zoom_date', 'not set')}

Available commands:
1. ID - remind my ID
2. CODE - remind activation code
3. DATE - remind meeting date
4. INSTRUCTION - Zoom instruction
5. HELP - help

Reply to this email with the needed command.
""",
            'he': f"""📱 תפריט ראשי

ה-ID שלך: №{user.get('participant_id', 'N/A')}
קוד ההפעלה שלך: {user.get('activation_code', 'N/A')}
תאריך הפגישה: {user.get('zoom_date', 'לא נקבע')}

פקודות זמינות:
1. ID - להזכיר ID
2. CODE - להזכיר קוד הפעלה
3. DATE - להזכיר תאריך פגישה
4. INSTRUCTION - הוראות Zoom
5. HELP - עזרה

השב למייל זה עם הפקודה הנדרשת.
"""
        }
        
        email_sender.send_email(
            to_email,
            get_text(language, 'main_menu'),
            menu_texts.get(language, menu_texts['ru'])
        )
    
    def run(self, interval: int = 60):
        """Запуск email-бота в цикле"""
        logger.info("Email bot started")
        
        while True:
            try:
                self.process_incoming_emails()
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Email bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in email bot loop: {e}")
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

