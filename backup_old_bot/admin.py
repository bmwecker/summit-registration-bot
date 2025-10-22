"""
Административный модуль для бота регистрации на саммит
Статистика, управление участниками, рассылка ссылок на Zoom
"""

from datetime import datetime
from typing import List, Dict
from database import Database

db = Database()


def get_statistics() -> Dict:
    """Получить общую статистику"""
    participants = db.get_all_participants()
    
    stats = {
        'total': len(participants),
        'individual': 0,
        'organization': 0,
        'with_qr': 0,
        'languages': {'ru': 0, 'en': 0, 'he': 0, 'unknown': 0},
        'by_date': {},
        'zoom_attended': 0
    }
    
    for p in participants:
        # Тип участника
        if p['participant_type'] == 'individual':
            stats['individual'] += 1
        elif p['participant_type'] == 'organization':
            stats['organization'] += 1
        
        # QR-код
        if p['qr_code_path']:
            stats['with_qr'] += 1
        
        # Язык
        lang = p.get('language', 'unknown')
        if lang in stats['languages']:
            stats['languages'][lang] += 1
        else:
            stats['languages']['unknown'] += 1
        
        # По датам Zoom
        zoom_date = p.get('zoom_date')
        if zoom_date:
            if zoom_date not in stats['by_date']:
                stats['by_date'][zoom_date] = {
                    'total': 0,
                    'ru': 0,
                    'en': 0,
                    'he': 0,
                    'individual': 0,
                    'organization': 0
                }
            stats['by_date'][zoom_date]['total'] += 1
            stats['by_date'][zoom_date][lang] += 1
            stats['by_date'][zoom_date][p['participant_type']] += 1
        
        # Посещение Zoom
        if p.get('zoom_attended') == 1:
            stats['zoom_attended'] += 1
    
    return stats


def format_statistics_message() -> str:
    """Форматировать статистику для отправки"""
    stats = get_statistics()
    
    text = "📊 **СТАТИСТИКА РЕГИСТРАЦИЙ**\n\n"
    text += f"👥 **Всего участников:** {stats['total']}\n"
    text += f"   • Частные лица: {stats['individual']}\n"
    text += f"   • Организации: {stats['organization']}\n\n"
    
    text += f"📲 **Получили QR-код:** {stats['with_qr']}\n\n"
    
    text += "🌍 **По языкам:**\n"
    text += f"   🇷🇺 Русский: {stats['languages']['ru']}\n"
    text += f"   🇬🇧 English: {stats['languages']['en']}\n"
    text += f"   🇮🇱 עברית: {stats['languages']['he']}\n\n"
    
    text += f"✅ **Посетили Zoom:** {stats['zoom_attended']}\n\n"
    
    text += "📅 **По датам Zoom-встреч:**\n"
    if stats['by_date']:
        for date, data in sorted(stats['by_date'].items()):
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted = date_obj.strftime("%d.%m.%Y")
            text += f"\n**{formatted}:**\n"
            text += f"   Всего: {data['total']} чел.\n"
            text += f"   🇷🇺 Русский: {data['ru']} | 🇬🇧 English: {data['en']} | 🇮🇱 עברית: {data['he']}\n"
            text += f"   👤 Частные: {data['individual']} | 🏢 Организации: {data['organization']}\n"
    else:
        text += "   Нет записей\n"
    
    return text


def get_participants_by_date(zoom_date: str) -> List[Dict]:
    """Получить участников по дате Zoom-встречи"""
    participants = db.get_all_participants()
    return [p for p in participants if p.get('zoom_date') == zoom_date]


def format_participants_by_date(zoom_date: str) -> str:
    """Форматировать список участников по дате"""
    participants = get_participants_by_date(zoom_date)
    
    if not participants:
        return f"На {zoom_date} нет записанных участников."
    
    date_obj = datetime.strptime(zoom_date, "%Y-%m-%d")
    formatted = date_obj.strftime("%d.%m.%Y")
    
    text = f"📅 **Участники на {formatted}:**\n\n"
    text += f"Всего: {len(participants)} чел.\n\n"
    
    for p in participants:
        lang_flag = {'ru': '🇷🇺', 'en': '🇬🇧', 'he': '🇮🇱'}.get(p.get('language', 'ru'), '🌐')
        type_emoji = '👤' if p['participant_type'] == 'individual' else '🏢'
        
        text += f"{type_emoji} {lang_flag} **{p['first_name']}**"
        if p.get('username'):
            text += f" (@{p['username']})"
        text += f"\n   📜 Сертификат: №{p['certificate_number']}\n"
        text += f"   🆔 ID: `{p['telegram_id']}`\n\n"
    
    return text


def get_all_dates_with_participants() -> List[str]:
    """Получить все даты, на которые есть записи"""
    participants = db.get_all_participants()
    dates = set()
    for p in participants:
        if p.get('zoom_date'):
            dates.add(p['zoom_date'])
    return sorted(list(dates))


def export_to_csv() -> str:
    """Экспортировать данные в CSV формат"""
    participants = db.get_all_participants()
    
    csv = "ID,Telegram_ID,Username,First_Name,Type,Certificate,Zoom_Date,Language,Registration_Date,Attended\n"
    
    for p in participants:
        csv += f"{p['id']},"
        csv += f"{p['telegram_id']},"
        csv += f"{p.get('username', '')},"
        csv += f"{p.get('first_name', '')},"
        csv += f"{p.get('participant_type', '')},"
        csv += f"{p.get('certificate_number', '')},"
        csv += f"{p.get('zoom_date', '')},"
        csv += f"{p.get('language', 'ru')},"
        csv += f"{p.get('registration_date', '')},"
        csv += f"{p.get('zoom_attended', 0)}\n"
    
    return csv


def get_telegram_ids_by_date(zoom_date: str) -> List[int]:
    """Получить Telegram ID участников по дате"""
    participants = get_participants_by_date(zoom_date)
    return [p['telegram_id'] for p in participants]


def mark_user_attended(telegram_id: int) -> bool:
    """Отметить, что пользователь посетил встречу"""
    try:
        db.mark_zoom_attended(telegram_id)
        return True
    except Exception as e:
        print(f"Error marking user attended: {e}")
        return False


def get_participant_info(telegram_id: int) -> str:
    """Получить детальную информацию об участнике"""
    user = db.get_user(telegram_id)
    
    if not user:
        return "Участник не найден."
    
    lang_name = {'ru': '🇷🇺 Русский', 'en': '🇬🇧 English', 'he': '🇮🇱 עברית'}.get(
        user.get('language', 'ru'), '🌐 Unknown'
    )
    type_name = 'Частное лицо' if user['participant_type'] == 'individual' else 'Организация'
    
    text = f"👤 **Информация об участнике**\n\n"
    text += f"**Имя:** {user.get('first_name', 'N/A')}\n"
    text += f"**Username:** @{user.get('username', 'нет')}\n"
    text += f"**Telegram ID:** `{user['telegram_id']}`\n\n"
    
    text += f"**Тип:** {type_name}\n"
    text += f"**Язык:** {lang_name}\n"
    text += f"**Сертификат:** №{user['certificate_number']}\n\n"
    
    if user.get('zoom_date'):
        date_obj = datetime.strptime(user['zoom_date'], "%Y-%m-%d")
        formatted = date_obj.strftime("%d.%m.%Y")
        text += f"**Zoom-встреча:** {formatted}\n"
    else:
        text += f"**Zoom-встреча:** не выбрана\n"
    
    text += f"**Посетил встречу:** {'✅ Да' if user.get('zoom_attended') == 1 else '❌ Нет'}\n"
    text += f"**Регистрация:** {user.get('registration_date', 'N/A')[:10]}\n"
    
    return text


def search_participants(query: str) -> List[Dict]:
    """Поиск участников по имени или username"""
    participants = db.get_all_participants()
    query_lower = query.lower()
    
    results = []
    for p in participants:
        if (query_lower in (p.get('first_name', '')).lower() or
            query_lower in (p.get('username', '')).lower() or
            str(p['telegram_id']) == query):
            results.append(p)
    
    return results


def get_unattended_by_date(zoom_date: str) -> List[Dict]:
    """Получить участников, которые НЕ посетили встречу"""
    participants = get_participants_by_date(zoom_date)
    return [p for p in participants if p.get('zoom_attended') != 1]


def get_attended_by_date(zoom_date: str) -> List[Dict]:
    """Получить участников, которые ПОСЕТИЛИ встречу"""
    participants = get_participants_by_date(zoom_date)
    return [p for p in participants if p.get('zoom_attended') == 1]


def get_participants_without_zoom_date() -> List[Dict]:
    """Получить участников без назначенной даты Zoom"""
    participants = db.get_all_participants()
    return [p for p in participants if not p.get('zoom_date')]


def get_recent_registrations(limit: int = 10) -> List[Dict]:
    """Получить последние регистрации"""
    participants = db.get_all_participants()
    # Уже отсортировано по registration_date DESC в get_all_participants
    return participants[:limit]


def format_recent_registrations(limit: int = 10) -> str:
    """Форматировать последние регистрации"""
    participants = get_recent_registrations(limit)
    
    if not participants:
        return "Нет регистраций."
    
    text = f"📝 **Последние {len(participants)} регистраций:**\n\n"
    
    for p in participants:
        lang_flag = {'ru': '🇷🇺', 'en': '🇬🇧', 'he': '🇮🇱'}.get(p.get('language', 'ru'), '🌐')
        type_emoji = '👤' if p['participant_type'] == 'individual' else '🏢'
        
        reg_date = p.get('registration_date', '')[:10]
        
        text += f"{type_emoji} {lang_flag} **{p['first_name']}**"
        if p.get('username'):
            text += f" (@{p['username']})"
        text += f"\n   📅 {reg_date} | 📜 №{p['certificate_number']}\n\n"
    
    return text
