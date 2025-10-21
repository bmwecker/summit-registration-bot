"""
Обработчики админ-команд для Aleph Bet Foresight Summit Bot
/admin, /stats, /sendlink, /export, /activate, /broadcast
"""

import logging
from typing import List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import TelegramError

from admin import (
    get_statistics,
    get_dates_with_counts,
    get_participants_by_date,
    export_participants_to_csv,
    export_participants_by_date_to_csv,
    activate_participants_bulk,
    get_telegram_ids_by_category
)

logger = logging.getLogger(__name__)

# ID администраторов
ADMIN_IDS = [386965305]  # Ваш ID

# Состояния для ConversationHandler
ADMIN_MENU, SENDING_LINK, ACTIVATING_CODES, BROADCASTING = range(4)


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь админом"""
    return user_id in ADMIN_IDS


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню админки"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав администратора.")
        return
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data='admin_stats')],
        [InlineKeyboardButton("📅 Участники по датам", callback_data='admin_dates')],
        [InlineKeyboardButton("📤 Экспорт данных", callback_data='admin_export')],
        [InlineKeyboardButton("🔗 Разослать Zoom-ссылку", callback_data='admin_sendlink')],
        [InlineKeyboardButton("✅ Массовая активация", callback_data='admin_activate')],
        [InlineKeyboardButton("📢 Рассылка сообщения", callback_data='admin_broadcast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔧 **Админ-панель**\n\nВыберите действие:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок админ-панели"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await query.edit_message_text("❌ У вас нет прав администратора.")
        return
    
    action = query.data
    
    # Статистика
    if action == 'admin_stats':
        stats = get_statistics()
        
        text = (
            "📊 **СТАТИСТИКА**\n\n"
            f"👥 Всего участников: {stats['total']}\n"
            f"✅ Активировано: {stats['activated']}\n"
            f"⏳ Не активировано: {stats['not_activated']}\n\n"
            "**По языкам:**\n"
        )
        
        for lang, count in stats['by_language'].items():
            lang_name = {'ru': '🇷🇺 Русский', 'en': '🇬🇧 English', 'he': '🇮🇱 עברית'}.get(lang, lang)
            text += f"{lang_name}: {count}\n"
        
        text += "\n**По датам:**\n"
        for date, count in sorted(stats['by_date'].items()):
            text += f"{date}: {count} чел.\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='admin_back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    # Участники по датам
    elif action == 'admin_dates':
        dates = get_dates_with_counts()
        
        if not dates:
            text = "📅 Нет зарегистрированных участников."
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='admin_back')]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        text = "📅 **УЧАСТНИКИ ПО ДАТАМ**\n\nВыберите дату для подробностей:"
        keyboard = []
        
        for date_info in dates:
            date = date_info['date']
            total = date_info['total']
            activated = date_info['activated']
            
            button_text = f"{date}: {total} чел. (✅ {activated})"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f'admin_date_{date}')])
        
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='admin_back')])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    # Подробности по дате
    elif action.startswith('admin_date_'):
        date = action.replace('admin_date_', '')
        participants = get_participants_by_date(date)
        
        text = f"📅 **Дата: {date}**\n\n"
        text += f"Всего участников: {len(participants)}\n"
        text += f"Активировано: {sum(1 for p in participants if p.get('is_activated'))}\n\n"
        
        # По языкам
        by_lang = {}
        for p in participants:
            lang = p.get('language', 'ru')
            by_lang[lang] = by_lang.get(lang, 0) + 1
        
        text += "**По языкам:**\n"
        for lang, count in by_lang.items():
            lang_name = {'ru': '🇷🇺 RU', 'en': '🇬🇧 EN', 'he': '🇮🇱 HE'}.get(lang, lang)
            text += f"{lang_name}: {count}\n"
        
        text += f"\n💾 Используйте /export_{date} для экспорта списка"
        
        keyboard = [
            [InlineKeyboardButton("🔗 Отправить Zoom-ссылку", callback_data=f'admin_sendlink_{date}')],
            [InlineKeyboardButton("📄 Экспортировать", callback_data=f'admin_export_{date}')],
            [InlineKeyboardButton("🔙 Назад", callback_data='admin_dates')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    # Экспорт всех данных
    elif action == 'admin_export':
        await query.edit_message_text("📤 Экспортирую данные...")
        
        csv_data = export_participants_to_csv()
        filename = f"participants_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=csv_data.getvalue().encode('utf-8-sig'),
            filename=filename,
            caption="📊 Экспорт всех участников"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='admin_back')]]
        await query.message.reply_text("✅ Экспорт завершён!", reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Экспорт по дате
    elif action.startswith('admin_export_'):
        date = action.replace('admin_export_', '')
        await query.edit_message_text(f"📤 Экспортирую данные за {date}...")
        
        csv_data = export_participants_by_date_to_csv(date)
        filename = f"participants_{date}.csv"
        
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=csv_data.getvalue().encode('utf-8-sig'),
            filename=filename,
            caption=f"📊 Участники на {date}"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='admin_dates')]]
        await query.message.reply_text("✅ Экспорт завершён!", reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Отправить Zoom-ссылку
    elif action == 'admin_sendlink':
        dates = get_dates_with_counts()
        
        if not dates:
            text = "📅 Нет зарегистрированных участников."
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='admin_back')]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        text = "🔗 **РАССЫЛКА ZOOM-ССЫЛКИ**\n\nВыберите дату:"
        keyboard = []
        
        for date_info in dates:
            date = date_info['date']
            total = date_info['total']
            button_text = f"{date} ({total} чел.)"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f'admin_sendlink_{date}')])
        
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='admin_back')])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    # Подготовка к отправке ссылки
    elif action.startswith('admin_sendlink_'):
        date = action.replace('admin_sendlink_', '')
        context.user_data['sendlink_date'] = date
        
        participants = get_participants_by_date(date)
        text = (
            f"🔗 **Рассылка Zoom-ссылки на {date}**\n\n"
            f"Получателей: {len(participants)}\n\n"
            "Отправьте мне Zoom-ссылку и текст сообщения (можно в несколько строк).\n"
            "Пример:\n"
            "```\n"
            "https://zoom.us/j/123456789\n"
            "Добро пожаловать на встречу!\n"
            "Время: 19:00 по Иерусалиму\n"
            "```\n\n"
            "Или /cancel для отмены."
        )
        
        await query.edit_message_text(text, parse_mode='Markdown')
        context.user_data['awaiting_link'] = True
    
    # Массовая активация
    elif action == 'admin_activate':
        text = (
            "✅ **МАССОВАЯ АКТИВАЦИЯ**\n\n"
            "Отправьте коды активации (по одному на строку или через запятую).\n"
            "Пример:\n"
            "```\n"
            "123456\n"
            "789012\n"
            "345678\n"
            "```\n\n"
            "Или /cancel для отмены."
        )
        await query.edit_message_text(text, parse_mode='Markdown')
        context.user_data['awaiting_codes'] = True
    
    # Рассылка сообщения
    elif action == 'admin_broadcast':
        keyboard = [
            [InlineKeyboardButton("📢 Всем", callback_data='broadcast_all')],
            [InlineKeyboardButton("🇷🇺 Русским", callback_data='broadcast_ru')],
            [InlineKeyboardButton("🇬🇧 Английским", callback_data='broadcast_en')],
            [InlineKeyboardButton("🇮🇱 Ивриту", callback_data='broadcast_he')],
            [InlineKeyboardButton("✅ Только активированным", callback_data='broadcast_activated')],
            [InlineKeyboardButton("🔙 Назад", callback_data='admin_back')]
        ]
        text = "📢 **РАССЫЛКА СООБЩЕНИЯ**\n\nВыберите категорию получателей:"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    # Выбор категории для рассылки
    elif action.startswith('broadcast_'):
        category = action.replace('broadcast_', '')
        context.user_data['broadcast_category'] = category
        
        # Подсчитываем получателей
        if category == 'all':
            ids = get_telegram_ids_by_category()
            cat_text = "всем участникам"
        elif category == 'activated':
            ids = get_telegram_ids_by_category(only_activated=True)
            cat_text = "активированным участникам"
        elif category in ['ru', 'en', 'he']:
            ids = get_telegram_ids_by_category(language=category)
            lang_names = {'ru': 'русскоязычным', 'en': 'англоязычным', 'he': 'ивритоязычным'}
            cat_text = lang_names[category]
        else:
            ids = []
            cat_text = "неизвестной категории"
        
        context.user_data['broadcast_ids'] = ids
        
        text = (
            f"📢 **Рассылка {cat_text}**\n\n"
            f"Получателей: {len(ids)}\n\n"
            "Отправьте мне текст сообщения для рассылки.\n\n"
            "Или /cancel для отмены."
        )
        
        await query.edit_message_text(text, parse_mode='Markdown')
        context.user_data['awaiting_broadcast'] = True
    
    # Назад в главное меню
    elif action == 'admin_back':
        keyboard = [
            [InlineKeyboardButton("📊 Статистика", callback_data='admin_stats')],
            [InlineKeyboardButton("📅 Участники по датам", callback_data='admin_dates')],
            [InlineKeyboardButton("📤 Экспорт данных", callback_data='admin_export')],
            [InlineKeyboardButton("🔗 Разослать Zoom-ссылку", callback_data='admin_sendlink')],
            [InlineKeyboardButton("✅ Массовая активация", callback_data='admin_activate')],
            [InlineKeyboardButton("📢 Рассылка сообщения", callback_data='admin_broadcast')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔧 **Админ-панель**\n\nВыберите действие:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def admin_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений от админа"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        return
    
    # Отправка Zoom-ссылки
    if context.user_data.get('awaiting_link'):
        date = context.user_data.get('sendlink_date')
        message_text = update.message.text
        
        participants = get_participants_by_date(date)
        telegram_ids = [p['telegram_id'] for p in participants]
        
        await update.message.reply_text(f"📤 Отправляю {len(telegram_ids)} сообщений...")
        
        success = 0
        failed = 0
        
        for tid in telegram_ids:
            try:
                await context.bot.send_message(chat_id=tid, text=message_text)
                success += 1
            except TelegramError as e:
                logger.error(f"Failed to send message to {tid}: {e}")
                failed += 1
        
        await update.message.reply_text(
            f"✅ **Рассылка завершена!**\n\n"
            f"Успешно: {success}\n"
            f"Ошибок: {failed}",
            parse_mode='Markdown'
        )
        
        context.user_data['awaiting_link'] = False
        context.user_data['sendlink_date'] = None
    
    # Массовая активация
    elif context.user_data.get('awaiting_codes'):
        text = update.message.text
        
        # Парсим коды
        codes = []
        for line in text.split('\n'):
            line = line.strip()
            if ',' in line:
                codes.extend([c.strip() for c in line.split(',')])
            elif line:
                codes.append(line)
        
        # Фильтруем только 6-значные коды
        valid_codes = [c for c in codes if c.isdigit() and len(c) == 6]
        
        if not valid_codes:
            await update.message.reply_text("❌ Не найдено ни одного валидного 6-значного кода.")
            return
        
        await update.message.reply_text(f"⏳ Активирую {len(valid_codes)} кодов...")
        
        success, failed = activate_participants_bulk(valid_codes)
        
        await update.message.reply_text(
            f"✅ **Активация завершена!**\n\n"
            f"Успешно активировано: {success}\n"
            f"Не найдено/ошибок: {failed}",
            parse_mode='Markdown'
        )
        
        context.user_data['awaiting_codes'] = False
    
    # Рассылка сообщения
    elif context.user_data.get('awaiting_broadcast'):
        message_text = update.message.text
        telegram_ids = context.user_data.get('broadcast_ids', [])
        
        if not telegram_ids:
            await update.message.reply_text("❌ Список получателей пуст.")
            return
        
        await update.message.reply_text(f"📤 Отправляю {len(telegram_ids)} сообщений...")
        
        success = 0
        failed = 0
        
        for tid in telegram_ids:
            try:
                await context.bot.send_message(chat_id=tid, text=message_text)
                success += 1
            except TelegramError as e:
                logger.error(f"Failed to send broadcast to {tid}: {e}")
                failed += 1
        
        await update.message.reply_text(
            f"✅ **Рассылка завершена!**\n\n"
            f"Успешно: {success}\n"
            f"Ошибок: {failed}",
            parse_mode='Markdown'
        )
        
        context.user_data['awaiting_broadcast'] = False
        context.user_data['broadcast_category'] = None
        context.user_data['broadcast_ids'] = None


# Импортируем datetime для экспорта
from datetime import datetime

