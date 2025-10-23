# 📱 НАСТРОЙКА WHATSAPP БОТА

## 🎯 ЧТО ЭТО?

WhatsApp бот через **whatsapp-web.js** (Node.js) для регистрации участников Summit.

✅ **Бесплатно** (без Twilio)  
✅ **Обычный WhatsApp** (не Business API)  
✅ **Общая база данных** с Telegram и Email ботами

---

## 🏗️ АРХИТЕКТУРА

```
┌─────────────────────────────────────────┐
│         PostgreSQL Database             │
│    (общая база для всех ботов)         │
└─────────────────────────────────────────┘
           ↑              ↑
           │              │
    ┌──────┴──────┐  ┌───┴────────────┐
    │   Python    │  │    Node.js     │
    │   Worker    │  │  Web Service   │
    ├─────────────┤  ├────────────────┤
    │ • Telegram  │  │  • WhatsApp    │
    │ • Email     │  │    (web.js)    │
    └─────────────┘  └────────────────┘
```

---

## 📦 ФАЙЛЫ

- `package.json` - зависимости Node.js
- `whatsapp_bot.js` - логика WhatsApp бота
- `whatsapp_server.js` - веб-сервер с QR-кодом
- `.env` - переменные окружения (DATABASE_URL)

---

## 🚀 ДЕПЛОЙ НА RENDER

### 1️⃣ Создать новый Web Service

1. Зайди на [Render Dashboard](https://dashboard.render.com/)
2. Нажми **New** → **Web Service**
3. Подключи репозиторий `summit-registration-bot`
4. **Настройки:**
   - **Name:** `summit-whatsapp-bot`
   - **Region:** Frankfurt (EU Central)
   - **Branch:** `main`
   - **Runtime:** Node
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
   - **Instance Type:** Free

### 2️⃣ Environment Variables

Добавь переменные окружения:

```
DATABASE_URL = postgresql://summit_user:WFkkQD09D9hBsNuN85K1QHvsmWh2wpE0@dpg-d3s0iq9r0fns73e52c70-a.frankfurt-postgres.render.com/summit_1lmm
```

*(Используй EXTERNAL Database URL от твоей PostgreSQL!)*

### 3️⃣ Deploy

Нажми **Create Web Service** → Render начнёт деплой.

---

## 📱 ПОДКЛЮЧЕНИЕ WHATSAPP

### ⚠️ ВАЖНО: Нужен телефон с WhatsApp!

После деплоя:

1. **Открой URL сервиса:**
   ```
   https://summit-whatsapp-bot.onrender.com
   ```

2. **На странице появится QR-код**

3. **На телефоне:**
   - Открой WhatsApp
   - Нажми **Меню (⋮)** → **Связанные устройства**
   - Нажми **Привязать устройство**
   - Отсканируй QR-код

4. **Готово!** ✅
   - На странице появится: "Бот подключен и работает!"
   - Сессия сохранена - повторное сканирование НЕ нужно

---

## 🧪 ТЕСТИРОВАНИЕ

### 1️⃣ Отправь сообщение боту

На WhatsApp напиши **боту** (на номер, который подключил):

```
START
```

### 2️⃣ Выбери язык

Бот ответит:
```
🕊️ Welcome to Aleph Bet Foresight Summit!

Choose language:
1️⃣ Русский (RU)
2️⃣ English (EN)
3️⃣ עברית (HE)
```

Ответь: `2` (для English)

### 3️⃣ Выбери дату

Бот предложит даты:
```
📅 Choose a convenient date:
1️⃣ Today...
2️⃣ Tomorrow...
3️⃣ Day after tomorrow...
```

Ответь: `1`

### 4️⃣ Получи ID

Бот отправит:
```
🎫 Your ID: №12003
📲 Activation code: 123456
```

✅ **Проверь в базе данных** - пользователь появился с `participant_type = 'whatsapp_participant'`

---

## 📊 ЛОГИ

Render → Services → `summit-whatsapp-bot` → **Logs**

Должны видеть:
```
[SERVER] Server running on port 10000
[WHATSAPP] QR code received
[WHATSAPP] Authenticated successfully
[WHATSAPP] Bot is ready!
[WHATSAPP] Message from 1234567890@c.us: START
```

---

## 🔧 КОМАНДЫ БОТА

| Команда | Описание |
|---------|----------|
| `START` | Начать регистрацию |
| `RU` / `EN` / `HE` | Выбрать язык |
| `1` / `2` / `3` | Выбрать дату (после выбора языка) |
| `MENU` | Показать главное меню |
| `HELP` | Справка |

---

## ⚠️ ВАЖНЫЕ МОМЕНТЫ

### Сессия WhatsApp

- **Сохраняется в `./whatsapp_session`** на Render
- При перезапуске сервиса НЕ нужно заново сканировать QR
- ❌ НО: Render Free tier может **удалять файлы** при остановке

### Решение проблемы с файлами

Если после рестарта просит QR снова:
1. Просто отсканируй QR заново
2. Сессия сохранится снова

**Для продакшена:** используй Render Paid Plan (файлы не удаляются) или добавь внешнее хранилище (AWS S3, Google Drive).

---

## 🆘 ПРОБЛЕМЫ

### Бот не отвечает

1. **Проверь логи** на Render
2. **Проверь сессию** - возможно, нужно заново отсканировать QR
3. **Проверь DATABASE_URL** - должен быть External URL

### QR не появляется

1. Подожди 30-60 секунд (Puppeteer запускается медленно)
2. Обнови страницу (авто-обновление каждые 10 сек)
3. Проверь логи - возможно ошибка

### "Authentication failure"

1. Зайди на сайт сервиса: `https://your-app.onrender.com`
2. Отсканируй QR заново
3. Если не помогает - удали `./whatsapp_session` и перезапусти сервис

---

## ✅ ИТОГ

✅ WhatsApp бот работает **параллельно** с Telegram и Email  
✅ Все используют **одну базу PostgreSQL**  
✅ Бесплатно и просто  
✅ Не нужен Twilio  

---

**Готово! Теперь у тебя 3 бота работают одновременно!** 🚀

