"""
Telegram-бот для Aleph Bet Foresight Summit
Многоязычная версия (Русский, English, עברית)
С логотипом, приветствием от Шломо, ID с 12000, 6-значными кодами
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from telegram.error import TelegramError
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Импортируем наши модули
from database import Database
from languages import get_text, LANGUAGE_NAMES, TEXTS
from bot_admin_handlers import (
    admin_command,
    admin_callback_handler,
    admin_message_handler,
    is_admin,
    ADMIN_IDS
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы для ConversationHandler
CHOOSING_LANGUAGE, CHOOSING_DATE, SHOWING_MENU = range(3)

# Константы
LOGO_PATH = "aleph-beth.png"
MAX_PARTICIPANTS_PER_DATE = 290
ADMIN_IDS = [386965305]  # Ваш ID

# Инициализация БД
db = Database()


def get_next_three_days() -> list:
    """
    Возвращает список из 3 ближайших дней (исключая пятницу и субботу)
    Формат: [(дата, день_недели_на_русском), ...]
    """
    days = []
    current = datetime.now()
    
    while len(days) < 3:
        # Пропускаем пятницу (4) и субботу (5)
        if current.weekday() not in [4, 5]:
            days.append(current)
        current += timedelta(days=1)
    
    return days


def format_date_button(date: datetime, language: str, index: int) -> str:
    """Форматирует дату для кнопки в зависимости от языка"""
    date_str = date.strftime('%d.%m.%Y')
    weekday = date.weekday()
    
    # Названия дней недели
    weekday_names = {
        'ru': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'he': ['יום שני', 'יום שלישי', 'יום רביעי', 'יום חמישי', 'יום שישי', 'שבת', 'יום ראשון']
    }
    
    # Сегодня, завтра, послезавтра
    relative_names = {
        'ru': ['Сегодня', 'Завтра', 'Послезавтра'],
        'en': ['Today', 'Tomorrow', 'Day after tomorrow'],
        'he': ['היום', 'מחר', 'מחרתיים']
    }
    
    day_name = weekday_names.get(language, weekday_names['ru'])[weekday]
    relative = relative_names.get(language, relative_names['ru'])[index] if index < 3 else ''
    
    if relative:
        return f"{relative} ({day_name}) - {date_str}"
    else:
        return f"{day_name} - {date_str}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало работы с ботом - выбор языка с логотипом"""
    user = update.effective_user
    telegram_id = user.id
    
    logger.info(f"User {telegram_id} ({user.username}) started the bot")
    
    # Проверяем, зарегистрирован ли пользователь
    existing_user = db.get_user(telegram_id)
    
    # Отправляем логотип
    try:
        if os.path.exists(LOGO_PATH):
            with open(LOGO_PATH, 'rb') as logo:
                await update.message.reply_photo(
                    photo=logo,
                    caption='🕊️ Aleph Bet Foresight Summit'
                )
    except Exception as e:
        logger.warning(f"Could not send logo: {e}")
    
    # Если пользователь уже есть - показываем меню
    if existing_user:
        language = db.get_user_language(telegram_id)
        context.user_data['language'] = language
        await show_main_menu(update, context, language)
        return SHOWING_MENU
    
    # Если новый пользователь - выбор языка
    keyboard = [
        [InlineKeyboardButton(LANGUAGE_NAMES['ru'], callback_data='lang_ru')],
        [InlineKeyboardButton(LANGUAGE_NAMES['en'], callback_data='lang_en')],
        [InlineKeyboardButton(LANGUAGE_NAMES['he'], callback_data='lang_he')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        TEXTS['ru']['welcome_choose_lang'],
        reply_markup=reply_markup
    )
    
    return CHOOSING_LANGUAGE


async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора языка"""
    query = update.callback_query
    await query.answer()
    
    language = query.data.split('_')[1]
    context.user_data['language'] = language
    
    # Сохраняем язык в БД (если пользователь уже есть)
    user = update.effective_user
    telegram_id = user.id
    existing_user = db.get_user(telegram_id)
    
    if existing_user:
        db.set_user_language(telegram_id, language)
        await query.edit_message_text(get_text(language, 'language_changed'))
        await show_main_menu_new_message(update, context, language)
        return SHOWING_MENU
    
    # Приветствие от Шломо
    await query.edit_message_text(get_text(language, 'greeting'))
    
    # Показываем кнопки с датами (новое сообщение)
    try:
        await show_date_selection(update, context, language, edit=False)
    except Exception as e:
        logger.error(f"Error showing date selection: {e}")
        # Если ошибка - пробуем через query
        dates = get_next_three_days()
        keyboard = []
        for i, date in enumerate(dates):
            date_str = date.strftime('%Y-%m-%d')
            button_text = format_date_button(date, language, i)
            count = db.get_participants_count_by_date(date_str)
            if count >= MAX_PARTICIPANTS_PER_DATE:
                button_text += " ❌ FULL"
            else:
                button_text += f" ({count}/{MAX_PARTICIPANTS_PER_DATE})"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f'date_{date_str}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=get_text(language, 'choose_date'),
            reply_markup=reply_markup
        )
    
    return CHOOSING_DATE


async def show_date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str, edit: bool = False):
    """Показать кнопки выбора даты"""
    logger.info(f"show_date_selection called with language={language}, edit={edit}")
    
    dates = get_next_three_days()
    logger.info(f"Got {len(dates)} dates: {[d.strftime('%Y-%m-%d') for d in dates]}")
    
    keyboard = []
    
    for i, date in enumerate(dates):
        date_str = date.strftime('%Y-%m-%d')
        button_text = format_date_button(date, language, i)
        
        # Проверяем количество участников на эту дату
        count = db.get_participants_count_by_date(date_str)
        logger.info(f"Date {date_str}: {count} participants")
        
        if count >= MAX_PARTICIPANTS_PER_DATE:
            button_text += " ❌ FULL"
        else:
            button_text += f" ({count}/{MAX_PARTICIPANTS_PER_DATE})"
        
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f'date_{date_str}')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = get_text(language, 'choose_date')
    
    logger.info(f"Sending date selection with {len(keyboard)} buttons")
    
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        logger.info("Date selection sent via edit_message_text")
    else:
        chat_id = update.effective_chat.id
        logger.info(f"Sending date selection to chat_id={chat_id}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
        logger.info("Date selection sent via send_message")


async def date_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора даты"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    telegram_id = user.id
    language = context.user_data.get('language', 'ru')
    
    date_str = query.data.split('_')[1]
    
    # Проверяем лимит
    count = db.get_participants_count_by_date(date_str)
    if count >= MAX_PARTICIPANTS_PER_DATE:
        await query.edit_message_text(get_text(language, 'date_full'))
        await show_date_selection(update, context, language, edit=False)
        return CHOOSING_DATE
    
    # Проверяем, зарегистрирован ли пользователь
    existing_user = db.get_user(telegram_id)
    
    if existing_user:
        # Обновляем дату
        db.update_zoom_date(telegram_id, date_str)
        await query.edit_message_text(get_text(language, 'meeting_confirmed'))
        await show_main_menu_new_message(update, context, language)
        return SHOWING_MENU
    else:
        # Создаём нового пользователя
        username = user.username or ''
        first_name = user.first_name or ''
        
        # participant_type пока не выбираем (можно будет добавить после активации)
        participant_id, activation_code = db.create_user(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            participant_type='participant',  # По умолчанию
            language=language
        )
        
        # Обновляем дату
        db.update_zoom_date(telegram_id, date_str)
        
        # Подтверждение
        await query.edit_message_text(get_text(language, 'meeting_confirmed'))
        
        # Отправляем ID и код
        id_text = get_text(
            language,
            'id_and_code',
            participant_id=participant_id,
            activation_code=activation_code
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=id_text)
        
        # Показываем меню
        await show_main_menu_new_message(update, context, language)
        
        return SHOWING_MENU


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str):
    """Показать главное меню (редактирование текущего сообщения)"""
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_remind_id'), callback_data='menu_remind_id')],
        [InlineKeyboardButton(get_text(language, 'btn_remind_code'), callback_data='menu_remind_code')],
        [InlineKeyboardButton(get_text(language, 'btn_remind_date'), callback_data='menu_remind_date')],
        [InlineKeyboardButton(get_text(language, 'btn_reschedule'), callback_data='menu_reschedule')],
        [InlineKeyboardButton(get_text(language, 'btn_how_activate'), callback_data='menu_how_activate')],
        [InlineKeyboardButton(get_text(language, 'btn_change_language'), callback_data='menu_change_language')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            get_text(language, 'main_menu'),
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            get_text(language, 'main_menu'),
            reply_markup=reply_markup
        )


async def show_main_menu_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str):
    """Показать главное меню (новое сообщение)"""
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_remind_id'), callback_data='menu_remind_id')],
        [InlineKeyboardButton(get_text(language, 'btn_remind_code'), callback_data='menu_remind_code')],
        [InlineKeyboardButton(get_text(language, 'btn_remind_date'), callback_data='menu_remind_date')],
        [InlineKeyboardButton(get_text(language, 'btn_reschedule'), callback_data='menu_reschedule')],
        [InlineKeyboardButton(get_text(language, 'btn_how_activate'), callback_data='menu_how_activate')],
        [InlineKeyboardButton(get_text(language, 'btn_change_language'), callback_data='menu_change_language')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_text(language, 'main_menu'),
        reply_markup=reply_markup
    )


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка кнопок меню"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    telegram_id = user.id
    language = context.user_data.get('language', db.get_user_language(telegram_id))
    
    action = query.data.split('_', 1)[1]
    
    user_data = db.get_user(telegram_id)
    if not user_data:
        await query.edit_message_text(get_text(language, 'not_registered'))
        return ConversationHandler.END
    
    # Напомнить ID
    if action == 'remind_id':
        text = get_text(language, 'your_id', participant_id=user_data['participant_id'])
        keyboard = [[InlineKeyboardButton(get_text(language, 'btn_back_to_menu'), callback_data='menu_back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return SHOWING_MENU
    
    # Напомнить код
    elif action == 'remind_code':
        text = get_text(language, 'your_code', activation_code=user_data['activation_code'])
        keyboard = [[InlineKeyboardButton(get_text(language, 'btn_back_to_menu'), callback_data='menu_back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return SHOWING_MENU
    
    # Напомнить дату
    elif action == 'remind_date':
        date_str = user_data.get('zoom_date', 'не указана')
        text = get_text(language, 'your_date', zoom_date=date_str)
        keyboard = [[InlineKeyboardButton(get_text(language, 'btn_back_to_menu'), callback_data='menu_back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return SHOWING_MENU
    
    # Перенести встречу
    elif action == 'reschedule':
        await show_date_selection(update, context, language, edit=True)
        return CHOOSING_DATE
    
    # Как активировать ID
    elif action == 'how_activate':
        text = get_text(language, 'how_to_activate')
        keyboard = [
            [InlineKeyboardButton(get_text(language, 'btn_instruction'), callback_data='menu_instruction')],
            [InlineKeyboardButton(get_text(language, 'btn_back_to_menu'), callback_data='menu_back')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return SHOWING_MENU
    
    # Инструкция по Zoom
    elif action == 'instruction':
        text = get_text(language, 'zoom_instruction')
        keyboard = [[InlineKeyboardButton(get_text(language, 'btn_back_to_menu'), callback_data='menu_back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return SHOWING_MENU
    
    # Изменить язык
    elif action == 'change_language':
        keyboard = [
            [InlineKeyboardButton(LANGUAGE_NAMES['ru'], callback_data='lang_ru')],
            [InlineKeyboardButton(LANGUAGE_NAMES['en'], callback_data='lang_en')],
            [InlineKeyboardButton(LANGUAGE_NAMES['he'], callback_data='lang_he')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            TEXTS['ru']['welcome_choose_lang'],
            reply_markup=reply_markup
        )
        return CHOOSING_LANGUAGE
    
    # Назад в меню
    elif action == 'back':
        await show_main_menu(update, context, language)
        return SHOWING_MENU
    
    return SHOWING_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена разговора"""
    language = context.user_data.get('language', 'ru')
    await update.message.reply_text('Отменено. Используйте /start для начала.')
    return ConversationHandler.END


def main():
    """Запуск бота"""
    # Получаем токен
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    # Создаём приложение
    application = Application.builder().token(token).build()
    
    # ConversationHandler для основного потока
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_LANGUAGE: [CallbackQueryHandler(language_chosen, pattern='^lang_')],
            CHOOSING_DATE: [CallbackQueryHandler(date_chosen, pattern='^date_')],
            SHOWING_MENU: [CallbackQueryHandler(menu_handler, pattern='^menu_')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    
    application.add_handler(conv_handler)
    
    # Админ-команды
    application.add_handler(CommandHandler('admin', admin_command))
    application.add_handler(CallbackQueryHandler(admin_callback_handler, pattern='^(admin_|broadcast_)'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_message_handler))
    
    # Запускаем бота
    logger.info("🚀 Aleph Bet Foresight Summit Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

