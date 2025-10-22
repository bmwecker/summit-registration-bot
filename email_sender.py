"""
Модуль для отправки email уведомлений участникам
Использует SMTP для отправки писем
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# Настройки SMTP из переменных окружения
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
FROM_NAME = os.getenv("FROM_NAME", "Aleph Bet Foresight Summit")


class EmailSender:
    """Класс для отправки email"""
    
    def __init__(self):
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_password = SMTP_PASSWORD
        self.from_email = FROM_EMAIL
        self.from_name = FROM_NAME
    
    def is_configured(self) -> bool:
        """Проверка, настроен ли SMTP"""
        return bool(self.smtp_user and self.smtp_password)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None
    ) -> bool:
        """
        Отправка email
        
        Args:
            to_email: Email получателя
            subject: Тема письма
            body_text: Текст письма (plain text)
            body_html: HTML версия письма (опционально)
        
        Returns:
            True если отправлено, False если ошибка
        """
        if not self.is_configured():
            logger.warning("SMTP not configured, skipping email")
            return False
        
        try:
            # Создаём сообщение
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Добавляем текстовую версию
            part1 = MIMEText(body_text, 'plain', 'utf-8')
            msg.attach(part1)
            
            # Добавляем HTML версию если есть
            if body_html:
                part2 = MIMEText(body_html, 'html', 'utf-8')
                msg.attach(part2)
            
            # Подключаемся к SMTP и отправляем
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_registration_confirmation(
        self,
        to_email: str,
        first_name: str,
        participant_id: int,
        activation_code: str,
        zoom_date: str,
        language: str = 'ru'
    ) -> bool:
        """Отправка подтверждения регистрации"""
        
        subjects = {
            'ru': f"✡️ Регистрация на Aleph Bet Foresight Summit - ID №{participant_id}",
            'en': f"✡️ Registration for Aleph Bet Foresight Summit - ID №{participant_id}",
            'he': f"✡️ רישום ל-Aleph Bet Foresight Summit - ID №{participant_id}"
        }
        
        texts = {
            'ru': f"""Шалом, {first_name}!

Поздравляем с регистрацией на Aleph Bet Foresight Summit!

🎫 Ваш ID: №{participant_id}
🔑 Код активации: {activation_code}
📅 Дата Zoom-встречи: {zoom_date}

⚠️ ВАЖНО:
• Для активации вашего ID необходимо присутствовать на Zoom-встрече
• На встрече отправьте ваш код активации в общий чат
• После активации вы сможете выбрать форму участия в саммите

Ссылку на Zoom-встречу вы получите за несколько часов до начала.

С уважением,
Команда Aleph Bet Foresight Summit
🕊️
""",
            'en': f"""Shalom, {first_name}!

Congratulations on registering for Aleph Bet Foresight Summit!

🎫 Your ID: №{participant_id}
🔑 Activation code: {activation_code}
📅 Zoom meeting date: {zoom_date}

⚠️ IMPORTANT:
• To activate your ID, you must attend the Zoom meeting
• At the meeting, send your activation code to the general chat
• After activation, you can choose your participation format in the summit

You will receive the Zoom meeting link a few hours before it starts.

Best regards,
Aleph Bet Foresight Summit Team
🕊️
""",
            'he': f"""שלום, {first_name}!

ברכות על ההרשמה ל-Aleph Bet Foresight Summit!

🎫 ה-ID שלך: №{participant_id}
🔑 קוד הפעלה: {activation_code}
📅 תאריך פגישת Zoom: {zoom_date}

⚠️ חשוב:
• להפעלת ה-ID שלך, עליך להשתתף בפגישת Zoom
• בפגישה, שלח את קוד ההפעלה שלך לצ'אט הכללי
• לאחר ההפעלה, תוכל לבחור את פורמט ההשתתפות שלך בפסגה

תקבל את הקישור לפגישת Zoom מספר שעות לפני תחילתה.

בברכה,
צוות Aleph Bet Foresight Summit
🕊️
"""
        }
        
        subject = subjects.get(language, subjects['ru'])
        body = texts.get(language, texts['ru'])
        
        return self.send_email(to_email, subject, body)
    
    def send_zoom_link(
        self,
        to_email: str,
        first_name: str,
        zoom_link: str,
        meeting_time: str,
        activation_code: str,
        language: str = 'ru'
    ) -> bool:
        """Отправка Zoom-ссылки"""
        
        subjects = {
            'ru': "🔗 Ссылка на Zoom-встречу Aleph Bet Summit",
            'en': "🔗 Zoom Meeting Link - Aleph Bet Summit",
            'he': "🔗 קישור לפגישת Zoom - Aleph Bet Summit"
        }
        
        texts = {
            'ru': f"""Шалом, {first_name}!

Ваша Zoom-встреча начнётся совсем скоро!

🔗 Ссылка на встречу: {zoom_link}
⏰ Время: {meeting_time}
🔑 Ваш код активации: {activation_code}

⚠️ НЕ ЗАБУДЬТЕ:
• Подключитесь за 5 минут до начала
• Отправьте ваш код активации ({activation_code}) в общий чат встречи
• Это необходимо для активации вашего ID

До встречи!
Команда Aleph Bet Foresight Summit
🕊️
""",
            'en': f"""Shalom, {first_name}!

Your Zoom meeting will start soon!

🔗 Meeting link: {zoom_link}
⏰ Time: {meeting_time}
🔑 Your activation code: {activation_code}

⚠️ DON'T FORGET:
• Join 5 minutes before start
• Send your activation code ({activation_code}) to the general chat
• This is required to activate your ID

See you there!
Aleph Bet Foresight Summit Team
🕊️
""",
            'he': f"""שלום, {first_name}!

פגישת ה-Zoom שלך תתחיל בקרוב!

🔗 קישור לפגישה: {zoom_link}
⏰ שעה: {meeting_time}
🔑 קוד ההפעלה שלך: {activation_code}

⚠️ אל תשכח:
• הצטרף 5 דקות לפני ההתחלה
• שלח את קוד ההפעלה שלך ({activation_code}) לצ'אט הכללי
• זה נדרש להפעלת ה-ID שלך

נתראה שם!
צוות Aleph Bet Foresight Summit
🕊️
"""
        }
        
        subject = subjects.get(language, subjects['ru'])
        body = texts.get(language, texts['ru'])
        
        return self.send_email(to_email, subject, body)
    
    def send_bulk_emails(
        self,
        recipients: List[tuple],
        subject: str,
        message: str
    ) -> tuple[int, int]:
        """
        Массовая рассылка
        
        Args:
            recipients: Список кортежей (email, first_name)
            subject: Тема письма
            message: Текст письма
        
        Returns:
            (успешно, ошибок)
        """
        success = 0
        failed = 0
        
        for email, first_name in recipients:
            # Персонализируем сообщение
            personalized_message = message.replace('{first_name}', first_name)
            
            if self.send_email(email, subject, personalized_message):
                success += 1
            else:
                failed += 1
        
        return success, failed


# Создаём глобальный экземпляр
email_sender = EmailSender()

