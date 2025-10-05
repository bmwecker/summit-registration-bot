"""
Многоязычный Telegram-бот для регистрации на саммит
Поддерживает русский, английский и иврит
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict
import qrcode
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

from database import Database
from languages import get_text, get_weekday, LANGUAGE_NAMES

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db = Database()

# Состояния диалога
CHOOSING_TYPE, CHOOSING_DATE, INFO_MENU, CHOOSING_LANGUAGE = range(4)

# Создание директории для QR-кодов
os.makedirs("qr_codes", exist_ok=True)


def get_user_language(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получить язык пользователя из контекста или БД"""
    if 'language' in context.user_data:
        return context.user_data['language']
    
    lang = db.get_user_language(user_id)
    context.user_data['language'] = lang
    return lang


def set_user_language(user_id: int, language: str, context: ContextTypes.DEFAULT_TYPE):
    """Установить язык пользователя"""
    context.user_data['language'] = language
    db.set_user_language(user_id, language)


def generate_qr_code(data: str, filename: str) -> str:
    """Генерация QR-кода"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    filepath = f"qr_codes/{filename}"
    img.save(filepath)
    return filepath


def get_available_dates() -> list:
    """Получить доступные даты на ближайшие 6 рабочих дней"""
    dates = []
    current_date = datetime.now()
    days_added = 0
    
    while days_added < 6:
        current_date += timedelta(days=1)
        # Пропускаем выходные (суббота=5, воскресенье=6)
        if current_date.weekday() < 5:
            dates.append(current_date)
            days_added += 1
    
    return dates


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало работы бота - показ выбора типа участника"""
    user = update.effective_user
    
    # Определяем язык из параметра start или из БД
    if context.args and context.args[0] in ['ru', 'en', 'he']:
        language = context.args[0]
        context.user_data['language'] = language
        logger.info(f"User {user.id} started with language: {language}")
    else:
        language = get_user_language(user.id, context)
    
    # Проверяем, не зарегистрирован ли уже пользователь
    existing_user = db.get_user(user.id)
    if existing_user:
        # Сохраняем язык если пользователь уже зарегистрирован
        if context.args and context.args[0] in ['ru', 'en', 'he']:
            set_user_language(user.id, language, context)
        
        text = get_text(language, 'already_registered', 
                       name=user.first_name, 
                       cert_number=existing_user['certificate_number'])
        await update.message.reply_text(text)
        return ConversationHandler.END
    
    # Сохраняем язык в БД сразу при первом обращении
    if context.args and context.args[0] in ['ru', 'en', 'he']:
        # Создаем временную запись чтобы сохранить язык
        context.user_data['preferred_language'] = language
    
    # Кнопки выбора типа участника
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_individual'), 
                            callback_data="type_individual")],
        [InlineKeyboardButton(get_text(language, 'btn_organization'), 
                            callback_data="type_organization")],
        [InlineKeyboardButton(get_text(language, 'btn_language'), 
                            callback_data="choose_language")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        get_text(language, 'welcome'),
        reply_markup=reply_markup
    )
    
    return CHOOSING_TYPE


async def choose_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать меню выбора языка"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    current_lang = get_user_language(user.id, context)
    
    keyboard = []
    for lang_code, lang_name in LANGUAGE_NAMES.items():
        keyboard.append([InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text(current_lang, 'choose_language'),
        reply_markup=reply_markup
    )
    
    return CHOOSING_LANGUAGE


async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора языка"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    language = query.data.replace("lang_", "")
    
    set_user_language(user.id, language, context)
    context.user_data['preferred_language'] = language
    
    # Показываем подтверждение смены языка
    await query.edit_message_text(get_text(language, 'language_changed'))
    
    # Возвращаем к выбору типа участника
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_individual'), 
                            callback_data="type_individual")],
        [InlineKeyboardButton(get_text(language, 'btn_organization'), 
                            callback_data="type_organization")],
        [InlineKeyboardButton(get_text(language, 'btn_language'), 
                            callback_data="choose_language")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        get_text(language, 'welcome'),
        reply_markup=reply_markup
    )
    
    return CHOOSING_TYPE


async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка текстового ввода вместо нажатия кнопки"""
    user = update.effective_user
    language = get_user_language(user.id, context)
    
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_individual'), 
                            callback_data="type_individual")],
        [InlineKeyboardButton(get_text(language, 'btn_organization'), 
                            callback_data="type_organization")],
        [InlineKeyboardButton(get_text(language, 'btn_language'), 
                            callback_data="choose_language")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        get_text(language, 'select_option'),
        reply_markup=reply_markup
    )
    
    return CHOOSING_TYPE


async def participant_type_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора типа участника"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    participant_type = query.data.replace("type_", "")
    language = get_user_language(user.id, context)
    
    # Сохраняем тип участника в контексте
    context.user_data['participant_type'] = participant_type
    
    # Получаем предпочитаемый язык
    preferred_language = context.user_data.get('preferred_language', language)
    
    # Создаем пользователя в базе данных
    certificate_number = db.create_user(
        telegram_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        participant_type=participant_type
    )
    
    # Сохраняем язык пользователя
    set_user_language(user.id, preferred_language, context)
    
    context.user_data['certificate_number'] = certificate_number
    
    # Формируем приветствие в зависимости от типа
    if participant_type == "individual":
        greeting = get_text(language, 'greeting_individual')
    else:
        greeting = get_text(language, 'greeting_organization')
    
    await query.edit_message_text(greeting)
    
    # Показываем доступные даты
    dates = get_available_dates()
    keyboard = []
    for date in dates:
        date_value = date.strftime("%Y-%m-%d")
        day_name = get_weekday(date.weekday(), language)
        display_text = date.strftime(f"%d.%m.%Y ({day_name})")
        
        keyboard.append([InlineKeyboardButton(display_text, callback_data=f"date_{date_value}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        get_text(language, 'choose_date'),
        reply_markup=reply_markup
    )
    
    return CHOOSING_DATE


async def date_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора даты"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    date_value = query.data.replace("date_", "")
    language = get_user_language(user.id, context)
    
    # Сохраняем дату в базе данных
    db.update_zoom_date(user.id, date_value)
    
    # Генерируем QR-код
    certificate_number = context.user_data['certificate_number']
    qr_data = f"SUMMIT_CERT_{certificate_number}_{user.id}"
    qr_filename = f"cert_{certificate_number}_{user.id}.png"
    qr_path = generate_qr_code(qr_data, qr_filename)
    
    # Сохраняем путь к QR-коду в базе данных
    db.update_qr_code(user.id, qr_path)
    
    # Форматируем дату для отображения
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
    day_name = get_weekday(date_obj.weekday(), language)
    formatted_date = date_obj.strftime(f"%d.%m.%Y ({day_name})")
    
    await query.edit_message_text(
        get_text(language, 'meeting_scheduled', date=formatted_date)
    )
    
    # Отправляем сертификат и QR-код
    with open(qr_path, 'rb') as qr_file:
        caption = get_text(language, 'certificate_caption', cert_number=certificate_number)
        await query.message.reply_photo(
            photo=qr_file,
            caption=caption
        )
    
    # Показываем меню информации
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_types'), callback_data="info_types")],
        [InlineKeyboardButton(get_text(language, 'btn_summit'), callback_data="info_summit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        get_text(language, 'info_prompt'),
        reply_markup=reply_markup
    )
    
    return INFO_MENU


async def info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора в меню информации"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    language = get_user_language(user.id, context)
    
    if query.data == "info_types":
        text = get_text(language, 'info_types')
    else:  # info_summit
        text = get_text(language, 'info_summit')
    
    # Добавляем кнопки для повторного просмотра
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_types'), callback_data="info_types")],
        [InlineKeyboardButton(get_text(language, 'btn_summit'), callback_data="info_summit")],
        [InlineKeyboardButton(get_text(language, 'btn_finish'), callback_data="finish")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    
    return INFO_MENU


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение регистрации"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    language = get_user_language(user.id, context)
    
    await query.edit_message_text(
        get_text(language, 'registration_complete')
    )
    
    return ConversationHandler.END


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu для доступа к информации"""
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        language = get_user_language(user.id, context)
        await update.message.reply_text(
            get_text(language, 'not_registered')
        )
        return
    
    language = get_user_language(user.id, context)
    
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_types'), callback_data="info_types")],
        [InlineKeyboardButton(get_text(language, 'btn_summit'), callback_data="info_summit")],
        [InlineKeyboardButton(get_text(language, 'btn_my_certificate'), callback_data="my_certificate")],
        [InlineKeyboardButton(get_text(language, 'btn_language'), callback_data="change_language_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        get_text(language, 'menu_title'),
        reply_markup=reply_markup
    )


async def show_certificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать сертификат пользователя"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_data = db.get_user(user.id)
    language = get_user_language(user.id, context)
    
    if not user_data:
        await query.edit_message_text(
            get_text(language, 'not_registered')
        )
        return
    
    qr_path = user_data['qr_code_path']
    certificate_number = user_data['certificate_number']
    zoom_date = user_data['zoom_date']
    
    date_obj = datetime.strptime(zoom_date, "%Y-%m-%d")
    day_name = get_weekday(date_obj.weekday(), language)
    formatted_date = date_obj.strftime(f"%d.%m.%Y ({day_name})")
    
    caption = get_text(language, 'certificate_info', 
                      cert_number=certificate_number,
                      date=formatted_date)
    
    with open(qr_path, 'rb') as qr_file:
        await query.message.reply_photo(
            photo=qr_file,
            caption=caption
        )


async def change_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать меню смены языка из главного меню"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    current_lang = get_user_language(user.id, context)
    
    keyboard = []
    for lang_code, lang_name in LANGUAGE_NAMES.items():
        keyboard.append([InlineKeyboardButton(lang_name, callback_data=f"setlang_{lang_code}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text(current_lang, 'choose_language'),
        reply_markup=reply_markup
    )


async def set_language_from_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установить язык из меню"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    language = query.data.replace("setlang_", "")
    
    set_user_language(user.id, language, context)
    
    await query.edit_message_text(
        get_text(language, 'language_changed')
    )
    
    # Вызываем меню заново с новым языком
    keyboard = [
        [InlineKeyboardButton(get_text(language, 'btn_types'), callback_data="info_types")],
        [InlineKeyboardButton(get_text(language, 'btn_summit'), callback_data="info_summit")],
        [InlineKeyboardButton(get_text(language, 'btn_my_certificate'), callback_data="my_certificate")],
        [InlineKeyboardButton(get_text(language, 'btn_language'), callback_data="change_language_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        get_text(language, 'menu_title'),
        reply_markup=reply_markup
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена диалога"""
    user = update.effective_user
    language = get_user_language(user.id, context)
    
    await update.message.reply_text(
        get_text(language, 'registration_cancelled')
    )
    return ConversationHandler.END


def main():
    """Запуск бота"""
    # Получаем токен из переменных окружения
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не найден в переменных окружения!")
        return
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Настройка обработчика диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_TYPE: [
                CallbackQueryHandler(choose_language_menu, pattern="^choose_language$"),
                CallbackQueryHandler(participant_type_chosen, pattern="^type_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input)
            ],
            CHOOSING_LANGUAGE: [
                CallbackQueryHandler(language_chosen, pattern="^lang_")
            ],
            CHOOSING_DATE: [
                CallbackQueryHandler(date_chosen, pattern="^date_")
            ],
            INFO_MENU: [
                CallbackQueryHandler(finish, pattern="^finish$"),
                CallbackQueryHandler(info_menu, pattern="^info_")
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CallbackQueryHandler(show_certificate, pattern="^my_certificate$"))
    application.add_handler(CallbackQueryHandler(change_language_menu, pattern="^change_language_menu$"))
    application.add_handler(CallbackQueryHandler(set_language_from_menu, pattern="^setlang_"))
    
    # Запускаем бота
    logger.info("Многоязычный бот запущен! Поддерживаются: ru, en, he")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
