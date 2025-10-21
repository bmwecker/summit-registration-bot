# 🚀 Render - Быстрая шпаргалка

## 📝 Пошаговая инструкция (коротко)

### 1️⃣ Загрузка на GitHub (5 минут)

```powershell
cd C:\Users\PC\summit-registration-bot
git init
git add .
git commit -m "Первый коммит"
git remote add origin https://github.com/ВАШ_USERNAME/summit-registration-bot.git
git branch -M main
git push -u origin main
```

**Если просит логин/пароль:**
- Создайте Personal Access Token на GitHub
- Settings → Developer settings → Personal access tokens → Generate new token
- Выберите scope: `repo`
- Используйте токен вместо пароля

---

### 2️⃣ Настройка на Render.com (3 минуты)

1. **Зайти:** [render.com](https://render.com)
2. **Войти:** через GitHub
3. **Создать:** New+ → Background Worker
4. **Выбрать:** репозиторий `summit-registration-bot`

---

### 3️⃣ Заполнение полей

| Поле | Значение |
|------|----------|
| **Name** | `summit-bot` |
| **Region** | `Frankfurt (EU Central)` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |

---

### 4️⃣ Переменные окружения (ВАЖНО!)

**Нажать "Advanced" → Add Environment Variable:**

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | Ваш токен от @BotFather |
| `PYTHON_VERSION` | `3.11.0` |

**Как получить токен:**
1. Telegram → найти @BotFather
2. Отправить `/mybots`
3. Выбрать бота → API Token
4. Скопировать (выглядит как `1234567890:ABCdef...`)

---

### 5️⃣ Тариф

Выбрать: **Free** (0$/месяц)

---

### 6️⃣ Запуск

Нажать: **Create Background Worker**

Ждать 1-2 минуты → статус должен стать **Live** 🟢

---

## ✅ Проверка

1. Открыть Telegram
2. Найти своего бота
3. Отправить `/start`
4. Должен ответить с кнопками!

---

## 🔍 Просмотр логов

**На странице сервиса → вкладка "Logs"**

Должно быть:
```
==> Building...
==> Build successful 🎉
==> Starting service...
==> Бот запущен!
```

---

## ⚠️ Типичные ошибки

### ❌ "TELEGRAM_BOT_TOKEN не найден"
**Решение:** Environment → добавить переменную `TELEGRAM_BOT_TOKEN`

### ❌ "ModuleNotFoundError: No module named 'telegram'"
**Решение:** Build Command должен быть `pip install -r requirements.txt`

### ❌ "Conflict: terminated by other getUpdates"
**Решение:** Остановить локального бота (Ctrl+C), подождать 30 сек

---

## 🔄 Обновление кода

```powershell
git add .
git commit -m "Описание изменений"
git push
```

Render автоматически задеплоит изменения (~1-2 мин)

---

## 🛑 Управление

- **Перезапуск:** Manual Deploy → Deploy latest commit
- **Остановка:** Settings → Suspend Service
- **Логи:** вкладка Logs (в реальном времени)
- **Метрики:** вкладка Metrics (CPU, RAM)

---

## 💰 Бесплатный тариф

✅ **Что есть:**
- 750 часов/месяц (достаточно для круглосуточной работы)
- 512 MB RAM
- Автоматические деплои

⚠️ **Ограничение:**
- Может "засыпать" после 15 мин без активности
- Первый ответ после сна ~10-30 сек

**Для тестирования и небольшой нагрузки - отлично подходит!**

---

## 📞 Полная инструкция

См. файл **DEPLOY_RENDER.md** - там всё очень подробно расписано!

---

## 🎯 Чеклист перед запуском

- [ ] Токен от BotFather получен
- [ ] Код на GitHub загружен
- [ ] Background Worker создан на Render
- [ ] Переменная `TELEGRAM_BOT_TOKEN` добавлена
- [ ] Build и Start Commands правильные
- [ ] Статус сервиса: Live 🟢
- [ ] В логах: "Бот запущен!"
- [ ] Бот отвечает в Telegram

**Всё готово? Поздравляю! 🎉**


