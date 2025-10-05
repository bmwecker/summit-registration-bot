"""
Обработчики админских команд для бота
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import admin
from database import Database

db = Database()

# ВАЖНО: Укажите ваш Telegram ID (получите от @userinfobot)
ADMIN_IDS = [
    # 123456789,  # Замените на ваш ID
]

# Можно также использовать переменную окружения
if os.getenv("ADMIN_TELEGRAM_ID"):
    try:
        ADMIN_IDS.append(int(os.getenv("ADMIN_TELEGRAM_ID")))
    except:
        pass


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь админом"""
    return user_id in ADMIN_IDS


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /admin - показать общую статистику"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return
    
    text = admin.format_statistics_message()
    
    keyboard = [
        [InlineKeyboardButton("📅 По датам", callback_data="admin_dates")],
        [InlineKeyboardButton("📝 Последние", callback_data="admin_recent")],
        [InlineKeyboardButton("📊 CSV экспорт", callback_data="admin_export")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def admin_dates_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать меню выбора даты"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if not is_admin(user.id):
        await query.edit_message_text("❌ У вас нет доступа.")
        return
    
    dates = admin.get_all_dates_with_participants()
    
    if not dates:
        await query.edit_message_text("📅 Нет записей на встречи.")
        return
    
    keyboard = []
    for date in dates:
        participants_count = len(admin.get_participants_by_date(date))
        from datetime import datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted = date_obj.strftime("%d.%m.%Y")
        
        keyboard.append([
            InlineKeyboardButton(
                f"{formatted} ({participants_count} чел.)",
                callback_data=f"admin_date_{date}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("« Назад", callback_data="admin_back")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📅 Выберите дату для просмотра участников:",
        reply_markup=reply_markup
    )


async def admin_date_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать детали по дате"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if not is_admin(user.id):
        await query.edit_message_text("❌ У вас нет доступа.")
        return
    
    date = query.data.replace("admin_date_", "")
    text = admin.format_participants_by_date(date)
    
    keyboard = [
        [InlineKeyboardButton("📨 Отправить ссылку всем", callback_data=f"admin_send_{date}")],
        [InlineKeyboardButton("« Назад к датам", callback_data="admin_dates")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Telegram ограничивает сообщения 4096 символами
    if len(text) > 4000:
        # Разбиваем на части
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # Последняя часть с кнопками
                await query.message.reply_text(part, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await query.message.reply_text(part, parse_mode='Markdown')
        await query.edit_message_text("📄 Список отправлен частями ↓")
    else:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)


async def admin_recent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать последние регистрации"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if not is_admin(user.id):
        await query.edit_message_text("❌ У вас нет доступа.")
        return
    
    text = admin.format_recent_registrations(20)
    
    keyboard = [
        [InlineKeyboardButton("« Назад", callback_data="admin_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)


async def admin_export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Экспортировать данные в CSV"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if not is_admin(user.id):
        await query.edit_message_text("❌ У вас нет доступа.")
        return
    
    csv_data = admin.export_to_csv()
    
    # Сохраняем в файл
    filename = f"participants_{admin.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', encoding='utf-8-sig') as f:  # utf-8-sig для корректного открытия в Excel
        f.write(csv_data)
    
    # Отправляем файл
    with open(filename, 'rb') as f:
        await query.message.reply_document(
            document=f,
            filename=filename,
            caption="📊 Экспорт всех участников в CSV"
        )
    
    # Удаляем временный файл
    try:
        os.remove(filename)
    except:
        pass
    
    await query.edit_message_text("✅ CSV файл отправлен")


async def admin_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вернуться к главному меню админа"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if not is_admin(user.id):
        return
    
    text = admin.format_statistics_message()
    
    keyboard = [
        [InlineKeyboardButton("📅 По датам", callback_data="admin_dates")],
        [InlineKeyboardButton("📝 Последние", callback_data="admin_recent")],
        [InlineKeyboardButton("📊 CSV экспорт", callback_data="admin_export")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def admin_send_zoom_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подготовка к отправке ссылки на Zoom"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if not is_admin(user.id):
        await query.edit_message_text("❌ У вас нет доступа.")
        return
    
    date = query.data.replace("admin_send_", "")
    participants = admin.get_participants_by_date(date)
    
    from datetime import datetime
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted = date_obj.strftime("%d.%m.%Y")
    
    text = f"📨 **Отправка ссылки на Zoom**\n\n"
    text += f"Дата: {formatted}\n"
    text += f"Участников: {len(participants)}\n\n"
    text += "Используйте команду:\n"
    text += f"`/sendlink {date} ВАША_ССЫЛКА_НА_ZOOM`\n\n"
    text += "Например:\n"
    text += f"`/sendlink {date} https://zoom.us/j/123456789`"
    
    await query.edit_message_text(text, parse_mode='Markdown')


async def admin_sendlink_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для отправки ссылки на Zoom всем участникам даты
    
    Использование: /sendlink 2025-10-10 https://zoom.us/j/123456789
    """
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Неверный формат.\n\n"
            "Использование:\n"
            "`/sendlink YYYY-MM-DD ссылка_на_zoom`\n\n"
            "Пример:\n"
            "`/sendlink 2025-10-10 https://zoom.us/j/123456789`",
            parse_mode='Markdown'
        )
        return
    
    date = context.args[0]
    zoom_link = context.args[1]
    
    # Получаем участников
    participants = admin.get_participants_by_date(date)
    
    if not participants:
        await update.message.reply_text(f"❌ На {date} нет зарегистрированных участников.")
        return
    
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted = date_obj.strftime("%d.%m.%Y")
    except:
        await update.message.reply_text("❌ Неверный формат даты. Используйте YYYY-MM-DD")
        return
    
    # Подтверждение
    await update.message.reply_text(
        f"📨 Начинаю рассылку ссылки на Zoom:\n\n"
        f"Дата: {formatted}\n"
        f"Участников: {len(participants)}\n"
        f"Ссылка: {zoom_link}\n\n"
        f"⏳ Отправка..."
    )
    
    # Отправляем ссылки
    success = 0
    failed = 0
    
    for p in participants:
        try:
            lang = p.get('language', 'ru')
            
            # Формируем сообщение на языке участника
            if lang == 'ru':
                message = (
                    f"🎥 **Ссылка на Zoom-встречу**\n\n"
                    f"Дата: {formatted}\n"
                    f"Ваш сертификат: №{p['certificate_number']}\n\n"
                    f"Ссылка для подключения:\n{zoom_link}\n\n"
                    f"⏰ Пожалуйста, подключитесь вовремя!\n"
                    f"Для активации сертификата необходимо присутствие на встрече."
                )
            elif lang == 'en':
                message = (
                    f"🎥 **Zoom Meeting Link**\n\n"
                    f"Date: {formatted}\n"
                    f"Your certificate: №{p['certificate_number']}\n\n"
                    f"Join link:\n{zoom_link}\n\n"
                    f"⏰ Please join on time!\n"
                    f"Meeting attendance is required for certificate activation."
                )
            else:  # he
                message = (
                    f"🎥 **קישור לפגישת Zoom**\n\n"
                    f"תאריך: {formatted}\n"
                    f"התעודה שלך: №{p['certificate_number']}\n\n"
                    f"קישור להצטרפות:\n{zoom_link}\n\n"
                    f"⏰ אנא הצטרף בזמן!\n"
                    f"נוכחות בפגישה נדרשת להפעלת התעודה."
                )
            
            await context.bot.send_message(
                chat_id=p['telegram_id'],
                text=message,
                parse_mode='Markdown'
            )
            success += 1
            
        except Exception as e:
            failed += 1
            print(f"Failed to send to {p['telegram_id']}: {e}")
    
    # Отчет
    await update.message.reply_text(
        f"✅ **Рассылка завершена!**\n\n"
        f"Успешно: {success}\n"
        f"Ошибок: {failed}\n"
        f"Всего: {len(participants)}",
        parse_mode='Markdown'
    )


async def admin_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения информации об участнике
    
    Использование: /info TELEGRAM_ID
    """
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "Использование: `/info TELEGRAM_ID`",
            parse_mode='Markdown'
        )
        return
    
    try:
        telegram_id = int(context.args[0])
    except:
        await update.message.reply_text("❌ Неверный формат ID")
        return
    
    text = admin.get_participant_info(telegram_id)
    await update.message.reply_text(text, parse_mode='Markdown')


async def admin_mark_attended_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для отметки посещения
    
    Использование: /attended TELEGRAM_ID
    """
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "Использование: `/attended TELEGRAM_ID`",
            parse_mode='Markdown'
        )
        return
    
    try:
        telegram_id = int(context.args[0])
    except:
        await update.message.reply_text("❌ Неверный формат ID")
        return
    
    if admin.mark_user_attended(telegram_id):
        await update.message.reply_text(f"✅ Участник {telegram_id} отмечен как посетивший встречу")
    else:
        await update.message.reply_text(f"❌ Ошибка при отметке участника {telegram_id}")
