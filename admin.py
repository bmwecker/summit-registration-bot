"""
Модуль админ-функций для Aleph Bet Foresight Summit Bot
Статистика, экспорт, массовая активация, рассылки
"""

import csv
import io
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from database import Database

db = Database()


def get_statistics() -> Dict:
    """Получить общую статистику"""
    participants = db.get_all_participants()
    
    total = len(participants)
    activated = sum(1 for p in participants if p.get('is_activated'))
    not_activated = total - activated
    
    # По языкам
    by_language = {}
    for p in participants:
        lang = p.get('language', 'ru')
        by_language[lang] = by_language.get(lang, 0) + 1
    
    # По датам
    by_date = {}
    for p in participants:
        date = p.get('zoom_date', 'не указана')
        by_date[date] = by_date.get(date, 0) + 1
    
    # По типам участников
    by_type = {}
    for p in participants:
        ptype = p.get('participant_type', 'participant')
        by_type[ptype] = by_type.get(ptype, 0) + 1
    
    return {
        'total': total,
        'activated': activated,
        'not_activated': not_activated,
        'by_language': by_language,
        'by_date': by_date,
        'by_type': by_type
    }


def get_participants_by_date(zoom_date: str) -> List[Dict]:
    """Получить участников по дате"""
    return db.get_participants_by_date(zoom_date)


def get_recent_participants(limit: int = 20) -> List[Dict]:
    """Получить последних зарегистрированных участников"""
    participants = db.get_all_participants()
    return participants[:limit]


def export_participants_to_csv() -> io.StringIO:
    """Экспорт всех участников в CSV"""
    participants = db.get_all_participants()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow([
        'ID участника',
        'Telegram ID',
        'Username',
        'Имя',
        'Тип участника',
        'Код активации',
        'Дата регистрации',
        'Дата Zoom',
        'Язык',
        'Активирован',
        'Дата активации'
    ])
    
    # Данные
    for p in participants:
        writer.writerow([
            p.get('participant_id', ''),
            p.get('telegram_id', ''),
            p.get('username', ''),
            p.get('first_name', ''),
            p.get('participant_type', ''),
            p.get('activation_code', ''),
            p.get('registration_date', ''),
            p.get('zoom_date', ''),
            p.get('language', ''),
            'Да' if p.get('is_activated') else 'Нет',
            p.get('activation_date', '')
        ])
    
    output.seek(0)
    return output


def export_participants_by_date_to_csv(zoom_date: str) -> io.StringIO:
    """Экспорт участников конкретной даты в CSV"""
    participants = db.get_participants_by_date(zoom_date)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow([
        'ID участника',
        'Telegram ID',
        'Username',
        'Имя',
        'Код активации',
        'Язык',
        'Активирован'
    ])
    
    # Данные
    for p in participants:
        writer.writerow([
            p.get('participant_id', ''),
            p.get('telegram_id', ''),
            p.get('username', ''),
            p.get('first_name', ''),
            p.get('activation_code', ''),
            p.get('language', ''),
            'Да' if p.get('is_activated') else 'Нет'
        ])
    
    output.seek(0)
    return output


def get_participant_details(telegram_id: int) -> Optional[Dict]:
    """Получить подробную информацию об участнике"""
    return db.get_user(telegram_id)


def activate_participants_bulk(codes: List[str]) -> Tuple[int, int]:
    """
    Массовая активация по кодам
    Возвращает (успешно, ошибок)
    """
    return db.activate_users_bulk(codes)


def get_dates_with_counts() -> List[Dict]:
    """Получить все даты с количеством участников"""
    participants = db.get_all_participants()
    
    dates_dict = {}
    for p in participants:
        date = p.get('zoom_date')
        if date and date != 'не указана':
            if date not in dates_dict:
                dates_dict[date] = {
                    'date': date,
                    'total': 0,
                    'activated': 0,
                    'by_language': {}
                }
            
            dates_dict[date]['total'] += 1
            
            if p.get('is_activated'):
                dates_dict[date]['activated'] += 1
            
            lang = p.get('language', 'ru')
            dates_dict[date]['by_language'][lang] = dates_dict[date]['by_language'].get(lang, 0) + 1
    
    # Сортируем по дате
    dates_list = sorted(dates_dict.values(), key=lambda x: x['date'])
    return dates_list


def get_telegram_ids_by_category(
    language: Optional[str] = None,
    participant_type: Optional[str] = None,
    zoom_date: Optional[str] = None,
    only_activated: bool = False
) -> List[int]:
    """
    Получить список Telegram ID по категориям для рассылки
    """
    participants = db.get_participants_by_category(
        language=language,
        participant_type=participant_type,
        zoom_date=zoom_date
    )
    
    if only_activated:
        participants = [p for p in participants if p.get('is_activated')]
    
    return [p['telegram_id'] for p in participants]

