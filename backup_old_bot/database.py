"""
Модуль для работы с базой данных SQLite
Хранит информацию об участниках саммита
"""

import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any


class Database:
    """Класс для работы с базой данных участников"""
    
    def __init__(self, db_path: str = "summit_bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                participant_type TEXT,
                certificate_number INTEGER UNIQUE,
                zoom_date TEXT,
                qr_code_path TEXT,
                registration_date TEXT,
                zoom_attended INTEGER DEFAULT 0,
                participation_form TEXT,
                language TEXT DEFAULT 'ru'
            )
        """)
        
        # Add language column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE participants ADD COLUMN language TEXT DEFAULT 'ru'")
            conn.commit()
        except sqlite3.OperationalError:
            # Column already exists
            pass
        
        conn.commit()
        conn.close()
    
    def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получить информацию о пользователе по Telegram ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM participants WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def create_user(
        self,
        telegram_id: int,
        username: str,
        first_name: str,
        participant_type: str
    ) -> int:
        """Создать нового пользователя и вернуть номер сертификата"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Получаем последний номер сертификата
        cursor.execute("SELECT MAX(certificate_number) FROM participants")
        result = cursor.fetchone()
        last_cert_num = result[0] if result[0] is not None else 0
        certificate_number = last_cert_num + 1
        
        registration_date = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO participants 
            (telegram_id, username, first_name, participant_type, 
             certificate_number, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (telegram_id, username, first_name, participant_type,
              certificate_number, registration_date))
        
        conn.commit()
        conn.close()
        
        return certificate_number
    
    def update_zoom_date(self, telegram_id: int, zoom_date: str):
        """Обновить дату Zoom-встречи"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE participants SET zoom_date = ? WHERE telegram_id = ?",
            (zoom_date, telegram_id)
        )
        
        conn.commit()
        conn.close()
    
    def update_qr_code(self, telegram_id: int, qr_code_path: str):
        """Обновить путь к QR-коду"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE participants SET qr_code_path = ? WHERE telegram_id = ?",
            (qr_code_path, telegram_id)
        )
        
        conn.commit()
        conn.close()
    
    def mark_zoom_attended(self, telegram_id: int):
        """Отметить участие в Zoom-встрече"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE participants SET zoom_attended = 1 WHERE telegram_id = ?",
            (telegram_id,)
        )
        
        conn.commit()
        conn.close()
    
    def update_participation_form(self, telegram_id: int, form: str):
        """Обновить форму участия"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE participants SET participation_form = ? WHERE telegram_id = ?",
            (form, telegram_id)
        )
        
        conn.commit()
        conn.close()
    
    def get_all_participants(self):
        """Получить всех участников (для админки)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM participants ORDER BY registration_date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def set_user_language(self, telegram_id: int, language: str):
        """Установить язык пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE participants SET language = ? WHERE telegram_id = ?",
            (language, telegram_id)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_language(self, telegram_id: int) -> str:
        """Получить язык пользователя (по умолчанию 'ru')"""
        user = self.get_user(telegram_id)
        if user and 'language' in user:
            return user['language'] or 'ru'
        return 'ru'


