"""
Модуль работы с базой данных (PostgreSQL / SQLite)
Поддержка как локальной разработки, так и продакшена на Render
"""

import os
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any, List
import random

# Определяем тип БД
DATABASE_URL = os.getenv("DATABASE_URL")  # PostgreSQL на Render
USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    import psycopg
    from psycopg.rows import dict_row
    # Render использует postgres://, но psycopg требует postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


class Database:
    """Класс для работы с базой данных участников"""
    
    def __init__(self, db_path: str = "summit_bot.db"):
        self.db_path = db_path
        self.use_postgres = USE_POSTGRES
        self.init_database()
    
    def get_connection(self):
        """Получить подключение к БД"""
        if self.use_postgres:
            return psycopg.connect(DATABASE_URL, row_factory=dict_row)
        else:
            return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = self.get_connection()
        
        if self.use_postgres:
            cursor = conn.cursor()
        else:
            cursor = conn.cursor()
        
        # Таблица участников
        if self.use_postgres:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS participants (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    participant_type TEXT,
                    participant_id INTEGER UNIQUE,
                    activation_code VARCHAR(6) UNIQUE,
                    zoom_date DATE,
                    registration_date TIMESTAMP,
                    language TEXT DEFAULT 'ru',
                    is_activated BOOLEAN DEFAULT FALSE,
                    activation_date TIMESTAMP
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS participants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    participant_type TEXT,
                    participant_id INTEGER UNIQUE,
                    activation_code TEXT UNIQUE,
                    zoom_date TEXT,
                    registration_date TEXT,
                    language TEXT DEFAULT 'ru',
                    is_activated INTEGER DEFAULT 0,
                    activation_date TEXT
                )
            """)
        
        conn.commit()
        conn.close()
    
    def generate_participant_id(self) -> int:
        """Генерация уникального ID участника (начиная с 12000)"""
        if self.use_postgres:
            # Для MAX используем обычный курсор без dict_row
            import psycopg
            conn = psycopg.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(participant_id) FROM participants")
            result = cursor.fetchone()
            conn.close()
            last_id = result[0] if result and result[0] is not None else 11999
        else:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(participant_id) FROM participants")
            result = cursor.fetchone()
            conn.close()
            last_id = result[0] if result and result[0] is not None else 11999
        
        return last_id + 1
    
    def generate_activation_code(self) -> str:
        """Генерация уникального 6-значного кода активации"""
        while True:
            code = str(random.randint(100000, 999999))
            
            # Проверяем уникальность
            if self.use_postgres:
                # Для COUNT используем обычный курсор без dict_row
                import psycopg
                conn = psycopg.connect(DATABASE_URL)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM participants WHERE activation_code = %s",
                    (code,)
                )
                count = cursor.fetchone()[0]
                conn.close()
            else:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM participants WHERE activation_code = ?",
                    (code,)
                )
                count = cursor.fetchone()[0]
                conn.close()
            
            if count == 0:
                return code
    
    def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получить информацию о пользователе по Telegram ID"""
        conn = self.get_connection()
        
        if self.use_postgres:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM participants WHERE telegram_id = %s",
                (telegram_id,)
            )
            row = cursor.fetchone()
        else:
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
        participant_type: str,
        language: str = 'ru'
    ) -> tuple[int, str]:
        """Создать нового пользователя и вернуть (ID, код активации)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        participant_id = self.generate_participant_id()
        activation_code = self.generate_activation_code()
        registration_date = datetime.now()
        
        if self.use_postgres:
            cursor.execute("""
                INSERT INTO participants 
                (telegram_id, username, first_name, participant_type, 
                 participant_id, activation_code, registration_date, language)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (telegram_id, username, first_name, participant_type,
                  participant_id, activation_code, registration_date, language))
        else:
            cursor.execute("""
                INSERT INTO participants 
                (telegram_id, username, first_name, participant_type, 
                 participant_id, activation_code, registration_date, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (telegram_id, username, first_name, participant_type,
                  participant_id, activation_code, registration_date.isoformat(), language))
        
        conn.commit()
        conn.close()
        
        return participant_id, activation_code
    
    def update_zoom_date(self, telegram_id: int, zoom_date: str):
        """Обновить дату Zoom-встречи"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            cursor.execute(
                "UPDATE participants SET zoom_date = %s WHERE telegram_id = %s",
                (zoom_date, telegram_id)
            )
        else:
            cursor.execute(
                "UPDATE participants SET zoom_date = ? WHERE telegram_id = ?",
                (zoom_date, telegram_id)
            )
        
        conn.commit()
        conn.close()
    
    def get_participants_count_by_date(self, zoom_date: str) -> int:
        """Получить количество участников на дату"""
        if self.use_postgres:
            # Для COUNT используем обычный курсор без dict_row
            import psycopg
            conn = psycopg.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM participants WHERE zoom_date = %s",
                (zoom_date,)
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count
        else:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM participants WHERE zoom_date = ?",
                (zoom_date,)
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count
    
    def set_user_language(self, telegram_id: int, language: str):
        """Установить язык пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            cursor.execute(
                "UPDATE participants SET language = %s WHERE telegram_id = %s",
                (language, telegram_id)
            )
        else:
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
    
    def activate_user(self, activation_code: str) -> bool:
        """Активировать пользователя по коду"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        activation_date = datetime.now()
        
        if self.use_postgres:
            cursor.execute(
                "UPDATE participants SET is_activated = TRUE, activation_date = %s WHERE activation_code = %s",
                (activation_date, activation_code)
            )
        else:
            cursor.execute(
                "UPDATE participants SET is_activated = 1, activation_date = ? WHERE activation_code = ?",
                (activation_date.isoformat(), activation_code)
            )
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def activate_users_bulk(self, activation_codes: List[str]) -> tuple[int, int]:
        """Массовая активация пользователей. Возвращает (успешно, ошибок)"""
        success = 0
        failed = 0
        
        for code in activation_codes:
            if self.activate_user(code):
                success += 1
            else:
                failed += 1
        
        return success, failed
    
    def get_all_participants(self) -> List[Dict]:
        """Получить всех участников (для админки)"""
        conn = self.get_connection()
        
        if self.use_postgres:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM participants ORDER BY registration_date DESC")
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM participants ORDER BY registration_date DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_participants_by_date(self, zoom_date: str) -> List[Dict]:
        """Получить участников по дате"""
        conn = self.get_connection()
        
        if self.use_postgres:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM participants WHERE zoom_date = %s ORDER BY registration_date",
                (zoom_date,)
            )
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM participants WHERE zoom_date = ? ORDER BY registration_date",
                (zoom_date,)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_participants_by_category(
        self,
        language: Optional[str] = None,
        participant_type: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        zoom_date: Optional[str] = None
    ) -> List[Dict]:
        """Получить участников по категориям для рассылки"""
        conn = self.get_connection()
        
        query = "SELECT * FROM participants WHERE 1=1"
        params = []
        
        if language:
            if self.use_postgres:
                query += " AND language = %s"
            else:
                query += " AND language = ?"
            params.append(language)
        
        if participant_type:
            if self.use_postgres:
                query += " AND participant_type = %s"
            else:
                query += " AND participant_type = ?"
            params.append(participant_type)
        
        if date_from:
            if self.use_postgres:
                query += " AND registration_date >= %s"
            else:
                query += " AND registration_date >= ?"
            params.append(date_from)
        
        if date_to:
            if self.use_postgres:
                query += " AND registration_date <= %s"
            else:
                query += " AND registration_date <= ?"
            params.append(date_to)
        
        if zoom_date:
            if self.use_postgres:
                query += " AND zoom_date = %s"
            else:
                query += " AND zoom_date = ?"
            params.append(zoom_date)
        
        if self.use_postgres:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

