# 📋 Шпаргалка команд

Быстрая справка по всем командам для работы с ботом.

## 🤖 Команды бота для пользователей

| Команда | Описание |
|---------|----------|
| `/start` | Начать регистрацию (или показать информацию, если уже зарегистрирован) |
| `/menu` | Открыть меню участника с информацией |
| `/cancel` | Отменить текущую операцию |

## 💻 Команды для разработки

### Первоначальная настройка:

```powershell
# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение (Windows)
.\venv\Scripts\activate

# Активировать виртуальное окружение (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать файл конфигурации
copy .env.example .env

# Запустить бота локально
python bot.py
```

### Git команды:

```bash
# Инициализировать репозиторий
git init

# Добавить все файлы
git add .

# Сделать коммит
git commit -m "Initial commit"

# Подключить удалённый репозиторий
git remote add origin https://github.com/ваш-username/summit-registration-bot.git

# Переименовать ветку в main
git branch -M main

# Загрузить на GitHub
git push -u origin main
```

### Обновление после изменений:

```bash
# Проверить статус
git status

# Добавить изменённые файлы
git add .

# Сделать коммит
git commit -m "Описание изменений"

# Загрузить на GitHub
git push
```

## 🔧 Полезные команды Python

```powershell
# Проверить версию Python
python --version

# Обновить pip
python -m pip install --upgrade pip

# Установить новую библиотеку
pip install название-библиотеки

# Обновить requirements.txt после добавления библиотек
pip freeze > requirements.txt

# Выйти из виртуального окружения
deactivate
```

## 🗄️ Работа с базой данных

### Просмотр данных в SQLite:

```powershell
# Установить SQLite Browser (графический интерфейс)
# Скачайте с: https://sqlitebrowser.org/

# Или через командную строку:
sqlite3 summit_bot.db

# Внутри SQLite:
.tables                              # Показать все таблицы
SELECT * FROM participants;          # Показать всех участников
SELECT COUNT(*) FROM participants;   # Количество участников
.exit                                # Выход
```

## 🚀 Render команды

### Через веб-интерфейс:

1. **Просмотр логов:**
   - Зайдите в ваш сервис на Render
   - Вкладка "Logs"
   - Здесь видны все ошибки и сообщения бота

2. **Перезапуск:**
   - Вкладка "Manual Deploy"
   - Кнопка "Deploy latest commit"

3. **Изменение переменных окружения:**
   - Вкладка "Environment"
   - Добавить/изменить переменные
   - Сохранить (сервис автоматически перезапустится)

## 📊 Администрирование бота

### Добавить команду для статистики:

В `bot.py` добавьте:

```python
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статистика для администратора (только для вашего ID)"""
    ADMIN_ID = 123456789  # Замените на ваш Telegram ID
    
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("У вас нет доступа к этой команде.")
        return
    
    participants = db.get_all_participants()
    total = len(participants)
    individual = len([p for p in participants if p['participant_type'] == 'individual'])
    organization = len([p for p in participants if p['participant_type'] == 'organization'])
    
    text = f"""📊 *Статистика регистраций*
    
Всего участников: {total}
👤 Частных лиц: {individual}
🏢 Организаций: {organization}

Последние 5 регистраций:
"""
    
    for p in participants[:5]:
        date = p['registration_date'][:10]
        text += f"\n#{p['certificate_number']} - {p['first_name']} ({date})"
    
    await update.message.reply_text(text, parse_mode='Markdown')

# Добавьте в main():
application.add_handler(CommandHandler("admin", admin_stats))
```

### Узнать свой Telegram ID:

1. Найдите бота [@userinfobot](https://t.me/userinfobot)
2. Отправьте ему любое сообщение
3. Он пришлёт ваш ID

## 🔍 Отладка

### Если бот не отвечает:

```powershell
# Проверьте, что файл .env создан и содержит токен
cat .env

# Проверьте, что все зависимости установлены
pip list

# Запустите с подробным логированием
python bot.py
```

### Если ошибка при запуске:

```powershell
# Переустановите зависимости
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Проверьте версию Python (нужна 3.9+)
python --version
```

## 📱 Тестирование

### Чек-лист перед запуском:

- [ ] Токен бота указан в `.env`
- [ ] Все зависимости установлены
- [ ] Бот запущен (локально или на Render)
- [ ] Протестирована команда `/start`
- [ ] Проверены оба типа участника
- [ ] QR-коды генерируются
- [ ] Даты отображаются корректно
- [ ] Меню `/menu` работает
- [ ] Информационные разделы открываются

### Сценарии тестирования:

1. **Новый пользователь:**
   - `/start` → выбор типа → выбор даты → получение сертификата

2. **Повторная регистрация:**
   - `/start` → должно показать, что уже зарегистрирован

3. **Текстовый ввод вместо кнопки:**
   - `/start` → написать текст вместо нажатия кнопки → должно попросить нажать кнопку

4. **Меню:**
   - `/menu` → проверить все разделы

## 🎯 Быстрые ссылки

- [BotFather](https://t.me/BotFather) - создание бота
- [Render Dashboard](https://dashboard.render.com) - управление хостингом
- [GitHub](https://github.com) - хранение кода
- [Tilda](https://tilda.cc) - конструктор сайтов

## 💡 Полезные ресурсы

- [Документация python-telegram-bot](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)


