# 🚀 START HERE - Aleph Bet Foresight Summit Bots

## 📋 Что у вас есть

У вас теперь есть **ДВА бота** для регистрации на саммит:

### 🇷🇺 Русская версия
**Папка:** `summit-registration-bot/` (текущая папка)
- Полностью на русском языке
- Приветствие "Шалом"
- Все тексты на русском

### 🇬🇧 Английская версия  
**Папка:** `summit-registration-bot-en/`
- Полностью на английском языке
- Greeting "Shalom"
- All texts in English
- **Bot username:** `AlephBetForesightSummitENbot`

---

## ⚡ Быстрый старт

### 1️⃣ Создать ботов в Telegram

Откройте [@BotFather](https://t.me/BotFather) и создайте **ДВА бота**:

**Русский бот:**
```
/newbot
Имя: Aleph Bet Foresight Summit RU
Username: YourRussianBotUsername_bot
Сохраните токен!
```

**Английский бот:**
```
/newbot
Имя: Aleph Bet Foresight Summit EN
Username: AlephBetForesightSummitENbot
Сохраните токен!
```

### 2️⃣ Тестирование локально

**Русский бот:**
```powershell
cd C:\Users\PC\summit-registration-bot
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Откройте .env и вставьте токен РУССКОГО бота
python bot.py
```

**Английский бот:**
```powershell
cd C:\Users\PC\summit-registration-bot\summit-registration-bot-en
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Откройте .env и вставьте токен АНГЛИЙСКОГО бота
python bot.py
```

### 3️⃣ Деплой на Render

Прочитайте **`BOTS_SETUP_GUIDE.md`** - там полная инструкция!

Кратко:
1. Создайте 2 репозитория на GitHub
2. Загрузите каждого бота в свой репозиторий
3. Создайте 2 Background Worker на Render
4. Добавьте токены в переменные окружения

---

## 📚 Документация

### Общие файлы:
- **`BOTS_SETUP_GUIDE.md`** ⭐ - **НАЧНИТЕ С ЭТОГО!** Полная инструкция для обоих ботов
- **`START_HERE.md`** - Этот файл (краткая навигация)

### Для русского бота (в текущей папке):
- `README.md` - Полная документация
- `QUICKSTART.md` - Быстрый старт для новичков
- `DEPLOY_RENDER.md` - Детальный деплой на Render
- `RENDER_QUICK_GUIDE.md` - Краткая шпаргалка Render
- `COMMANDS.md` - Все команды
- `TILDA_INTEGRATION.md` - Интеграция с сайтом

### Для английского бота (в папке `summit-registration-bot-en/`):
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start for beginners
- `DEPLOY_RENDER.md` - Detailed Render deployment
- `RENDER_QUICK_GUIDE.md` - Quick Render reference
- `COMMANDS.md` - All commands
- `TILDA_INTEGRATION.md` - Website integration

---

## 🎯 Следующие шаги

### Шаг 1: Прочитайте главный гайд
📖 Откройте **`BOTS_SETUP_GUIDE.md`**

### Шаг 2: Создайте ботов в @BotFather
🤖 Создайте оба бота и сохраните токены

### Шаг 3: Протестируйте локально
💻 Запустите оба бота на компьютере

### Шаг 4: Задеплойте на Render
🚀 Загрузите на бесплатный хостинг

### Шаг 5: Добавьте на сайт
🌐 Добавьте кнопки на Tilda

---

## 🆘 Нужна помощь?

### Вопрос: "С чего начать?"
**Ответ:** Откройте `BOTS_SETUP_GUIDE.md` - там всё пошагово!

### Вопрос: "Как создать бота?"
**Ответ:** См. раздел "Быстрый старт" выше или `QUICKSTART.md`

### Вопрос: "Как задеплоить?"
**Ответ:** См. `DEPLOY_RENDER.md` - очень подробная инструкция!

### Вопрос: "Где токены хранить?"
**Ответ:** В `.env` файле (НЕ коммитить в Git!)

### Вопрос: "Можно ли запустить оба бота одновременно локально?"
**Ответ:** Нет, только по очереди. Для одновременной работы - деплой на Render.

---

## ✅ Чеклист запуска

### Русский бот:
- [ ] Создан в @BotFather
- [ ] Токен сохранён
- [ ] Протестирован локально
- [ ] Репозиторий на GitHub
- [ ] Задеплоен на Render
- [ ] Работает в Telegram

### Английский бот:
- [ ] Создан в @BotFather
- [ ] Токен сохранён
- [ ] Протестирован локально
- [ ] Репозиторий на GitHub
- [ ] Задеплоен на Render
- [ ] Работает в Telegram

---

## 📞 Структура проекта

```
summit-registration-bot/
├── 📄 START_HERE.md              ← ВЫ ЗДЕСЬ
├── 📘 BOTS_SETUP_GUIDE.md        ← НАЧНИТЕ С ЭТОГО!
├── 🇷🇺 Русский бот (файлы в корне)
│   ├── bot.py
│   ├── database.py
│   ├── requirements.txt
│   └── 📚 Документация (*.md)
│
└── 📁 summit-registration-bot-en/
    ├── 🇬🇧 Английский бот
    ├── bot.py
    ├── database.py
    ├── requirements.txt
    └── 📚 Documentation (*.md)
```

---

## 🎉 Готово!

После настройки у вас будет:
- ✅ 2 работающих Telegram-бота
- ✅ Автоматическая регистрация участников
- ✅ Генерация QR-кодов
- ✅ Выбор даты Zoom-встречи
- ✅ Информация о саммите
- ✅ Хранение данных в базе

**Удачи с Aleph Bet Foresight Summit! 🕊️**
