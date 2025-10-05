"""
Telegram-бот для регистрации на саммит
Поддерживает выбор типа участника, запись на Zoom и выдачу сертификата
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
CHOOSING_TYPE, CHOOSING_DATE, INFO_MENU = range(3)

# Создание директории для QR-кодов
os.makedirs("qr_codes", exist_ok=True)


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
    
    # Проверяем, не зарегистрирован ли уже пользователь
    existing_user = db.get_user(user.id)
    if existing_user:
        await update.message.reply_text(
            f"✡️ Шалом, {user.first_name}!\n\n"
            f"Вы уже зарегистрированы.\n"
            f"📜 Номер вашего сертификата: №{existing_user['certificate_number']}\n\n"
            "Используйте /menu для доступа к информации."
        )
        return ConversationHandler.END
    
    keyboard = [
        [InlineKeyboardButton("🔘 Я со своим народом", callback_data="type_individual")],
        [InlineKeyboardButton("🔘 Наша организация со своим народом", callback_data="type_organization")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🕊️ Добро пожаловать на регистрацию саммита!\n\n"
        "Пожалуйста, выберите, кто вы:",
        reply_markup=reply_markup
    )
    
    return CHOOSING_TYPE


async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка текстового ввода вместо нажатия кнопки"""
    keyboard = [
        [InlineKeyboardButton("🔘 Я со своим народом", callback_data="type_individual")],
        [InlineKeyboardButton("🔘 Наша организация со своим народом", callback_data="type_organization")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🙏 Пожалуйста, выберите один из вариантов, чтобы продолжить:",
        reply_markup=reply_markup
    )
    
    return CHOOSING_TYPE


async def participant_type_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора типа участника"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    participant_type = query.data.replace("type_", "")
    
    # Сохраняем тип участника в контексте
    context.user_data['participant_type'] = participant_type
    context.user_data['participant_type_ru'] = (
        "частное лицо" if participant_type == "individual" else "организация"
    )
    
    # Создаем пользователя в базе данных
    certificate_number = db.create_user(
        telegram_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        participant_type=participant_type
    )
    
    context.user_data['certificate_number'] = certificate_number
    
    # Формируем приветствие в зависимости от типа
    if participant_type == "individual":
        greeting = (
            "✡️ Шалом! Поздравляем — вы со своим народом!\n\n"
            "🎉 Вы приглашены на Zoom-встречу с оргкомитетом для новичков, "
            "где познакомитесь с организаторами.\n\n"
            "Для вашего удобства вы можете выбрать любой день встречи, "
            "но важно попасть на неё в течение 6 рабочих дней."
        )
    else:
        greeting = (
            "✡️ Шалом! Ваша организация со своим народом!\n\n"
            "🎉 Ваша команда приглашена на Zoom-встречу с оргкомитетом "
            "для новых партнёров и представителей общин.\n\n"
            "Для вашего удобства можно выбрать любой день встречи "
            "в течение 6 рабочих дней."
        )
    
    await query.edit_message_text(greeting)
    
    # Показываем доступные даты
    dates = get_available_dates()
    keyboard = []
    for date in dates:
        date_str = date.strftime("%d.%m.%Y (%A)")
        date_value = date.strftime("%Y-%m-%d")
        # Переводим день недели на русский
        weekday_ru = {
            'Monday': 'Понедельник',
            'Tuesday': 'Вторник',
            'Wednesday': 'Среда',
            'Thursday': 'Четверг',
            'Friday': 'Пятница'
        }
        day_name = weekday_ru.get(date.strftime("%A"), date.strftime("%A"))
        display_text = date.strftime(f"%d.%m.%Y ({day_name})")
        
        keyboard.append([InlineKeyboardButton(display_text, callback_data=f"date_{date_value}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "📅 Выберите удобную дату для Zoom-встречи:",
        reply_markup=reply_markup
    )
    
    return CHOOSING_DATE


async def date_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора даты"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    date_value = query.data.replace("date_", "")
    
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
    weekday_ru = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница'
    }
    formatted_date = date_obj.strftime(f"%d.%m.%Y ({weekday_ru[date_obj.weekday()]})")
    
    await query.edit_message_text(
        f"✅ Отлично! Встреча назначена на {formatted_date}"
    )
    
    # Отправляем сертификат и QR-код
    with open(qr_path, 'rb') as qr_file:
        await query.message.reply_photo(
            photo=qr_file,
            caption=(
                f"🎫 Ваш номер сертификата участника: №{certificate_number}\n"
                f"📲 QR-код для активации сертификата\n\n"
                f"⚠️ Для активации сертификата необходимо присутствовать на Zoom-встрече.\n"
                f"После активации можно выбрать форму участия в саммите."
            )
        )
    
    # Показываем меню информации
    keyboard = [
        [InlineKeyboardButton("🔹 Виды участия", callback_data="info_types")],
        [InlineKeyboardButton("🔹 О саммите", callback_data="info_summit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Чтобы получить ключевую информацию, нажмите одну из кнопок:",
        reply_markup=reply_markup
    )
    
    return INFO_MENU


async def info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора в меню информации"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "info_types":
        text = (
            "📋 *Виды участия в саммите*\n\n"
            "1️⃣ *Онлайн-участие (частное лицо)*\n"
            "   • Доступ ко всем онлайн-трансляциям\n"
            "   • Участие в общих чатах\n"
            "   • Сертификат участника\n\n"
            "2️⃣ *Офлайн-участие (частное лицо)*\n"
            "   • Личное присутствие на мероприятии\n"
            "   • Все преимущества онлайн-участия\n"
            "   • Networking с другими участниками\n"
            "   • Памятные подарки\n\n"
            "3️⃣ *Организационное участие*\n"
            "   • Представление вашей общины/организации\n"
            "   • Возможность выступления\n"
            "   • Партнёрские материалы\n"
            "   • Особые условия для команды\n\n"
            "💡 Окончательный выбор формы участия можно будет сделать "
            "после Zoom-встречи с оргкомитетом."
        )
    else:  # info_summit
        text = (
            "🌟 *О саммите*\n\n"
            "Саммит — это уникальное мероприятие, объединяющее представителей "
            "еврейских общин, организаций и всех, кто связан со своим народом.\n\n"
            "*Цели саммита:*\n"
            "• Укрепление связей между общинами\n"
            "• Обмен опытом и лучшими практиками\n"
            "• Обсуждение актуальных вопросов\n"
            "• Создание новых партнёрств\n"
            "• Культурное обогащение\n\n"
            "*Почему это важно для вас?*\n"
            "• Возможность найти единомышленников\n"
            "• Доступ к уникальной информации и ресурсам\n"
            "• Укрепление еврейской идентичности\n"
            "• Вклад в развитие общины\n\n"
            "📅 Саммит проводится ежегодно и собирает сотни участников "
            "со всего мира."
        )
    
    # Добавляем кнопки для повторного просмотра
    keyboard = [
        [InlineKeyboardButton("🔹 Виды участия", callback_data="info_types")],
        [InlineKeyboardButton("🔹 О саммите", callback_data="info_summit")],
        [InlineKeyboardButton("✅ Завершить", callback_data="finish")]
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
    
    await query.edit_message_text(
        "✅ Регистрация завершена!\n\n"
        "Мы отправим вам напоминание о Zoom-встрече за день до мероприятия.\n\n"
        "Используйте команду /menu для доступа к информации в любое время.\n\n"
        "До встречи! 🕊️"
    )
    
    return ConversationHandler.END


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu для доступа к информации"""
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text(
            "Вы еще не зарегистрированы. Используйте команду /start для регистрации."
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("🔹 Виды участия", callback_data="info_types")],
        [InlineKeyboardButton("🔹 О саммите", callback_data="info_summit")],
        [InlineKeyboardButton("📜 Мой сертификат", callback_data="my_certificate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📱 Меню участника саммита:",
        reply_markup=reply_markup
    )


async def show_certificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать сертификат пользователя"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await query.edit_message_text(
            "Вы еще не зарегистрированы. Используйте команду /start для регистрации."
        )
        return
    
    qr_path = user_data['qr_code_path']
    certificate_number = user_data['certificate_number']
    zoom_date = user_data['zoom_date']
    
    date_obj = datetime.strptime(zoom_date, "%Y-%m-%d")
    weekday_ru = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница'
    }
    formatted_date = date_obj.strftime(f"%d.%m.%Y ({weekday_ru[date_obj.weekday()]})")
    
    with open(qr_path, 'rb') as qr_file:
        await query.message.reply_photo(
            photo=qr_file,
            caption=(
                f"🎫 Ваш номер сертификата: №{certificate_number}\n"
                f"📅 Дата Zoom-встречи: {formatted_date}\n"
                f"⚠️ Для активации сертификата необходимо присутствовать на встрече."
            )
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена диалога"""
    await update.message.reply_text(
        "Регистрация отменена. Используйте /start для начала регистрации."
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
                CallbackQueryHandler(participant_type_chosen, pattern="^type_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input)
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
    
    # Запускаем бота
    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()


