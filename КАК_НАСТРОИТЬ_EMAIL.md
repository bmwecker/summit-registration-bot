# 📧 Как настроить Email (Быстрая инструкция)

## ✅ Что уже сделано

- ✅ Модуль отправки email создан (`email_sender.py`)
- ✅ База данных обновлена (добавлено поле `email`)
- ✅ Задеплоено на Render
- ✅ Бот работает и БЕЗ email (опционально)

---

## 🚀 Что сделать ВАМ

### Вариант 1: Использовать Gmail (Рекомендуется)

#### Шаг 1: Получите App Password

1. Откройте: https://myaccount.google.com/apppasswords
2. Если просит - включите **2-Step Verification** сначала
3. Создайте **App Password**:
   - App: Mail
   - Device: Other → "Aleph Bet Bot"
4. **Скопируйте 16-символьный пароль** (например: `abcd efgh ijkl mnop`)

#### Шаг 2: Добавьте в Render

1. Зайдите на https://dashboard.render.com
2. Откройте ваш **Background Worker**: `summit-registration-bot`
3. **Environment** → **Add Environment Variable**
4. Добавьте **5 переменных**:

```
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = ваш-email@gmail.com
SMTP_PASSWORD = abcd efgh ijkl mnop (из шага 1)
FROM_EMAIL = ваш-email@gmail.com
FROM_NAME = Aleph Bet Foresight Summit
```

5. **Save Changes**
6. Подождите пока Render перезапустит бота (~1 минута)

---

### Вариант 2: Использовать Mail.ru / Yandex

#### Mail.ru:
```
SMTP_HOST = smtp.mail.ru
SMTP_PORT = 587
SMTP_USER = ваш-email@mail.ru
SMTP_PASSWORD = ваш-пароль
FROM_EMAIL = ваш-email@mail.ru
FROM_NAME = Aleph Bet Foresight Summit
```

#### Yandex:
```
SMTP_HOST = smtp.yandex.ru
SMTP_PORT = 587
SMTP_USER = ваш-email@yandex.ru
SMTP_PASSWORD = ваш-пароль
FROM_EMAIL = ваш-email@yandex.ru
FROM_NAME = Aleph Bet Foresight Summit
```

---

## 🧪 Как проверить

После настройки в Render:

1. Зарегистрируйте тестового пользователя **с email**
2. Проверьте почту - должно прийти письмо с:
   - ✉️ ID участника
   - ✉️ Код активации
   - ✉️ Дата Zoom-встречи

**Если письмо не пришло:**
- Проверьте папку **Спам**
- Проверьте правильность SMTP настроек
- Посмотрите логи на Render

---

## 📝 Что будет отправляться

### Автоматически (если email собран):

1. **При регистрации:**
   ```
   Тема: ✡️ Регистрация на Aleph Bet Foresight Summit
   
   Шалом!
   🎫 Ваш ID: №12001
   🔑 Код активации: 123456
   📅 Дата: 2025-10-23
   ```

2. **Перед Zoom-встречей** (через админку):
   ```
   Тема: 🔗 Ссылка на Zoom-встречу
   
   🔗 Ссылка: https://zoom.us/j/...
   ⏰ Время: 19:00
   🔑 Ваш код: 123456
   ```

---

## 💡 Если НЕ хотите настраивать email

**Ничего делать не нужно!**

Бот проверяет наличие SMTP настроек:
- ✅ Если настроено - отправляет email
- ✅ Если нет - просто пропускает и работает через Telegram

---

## 🔒 Безопасность

⚠️ **ВАЖНО:**
- Используйте **App Password** для Gmail (не основной пароль!)
- **НЕ** публикуйте пароли в коде
- Храните только в **Environment Variables** на Render

---

## 📊 Лимиты

- **Gmail:** 500 писем/день
- **Mail.ru:** 100 писем/час
- **Yandex:** 500 писем/день

Этого достаточно для вашего саммита! 👍

---

## ✅ Готово!

Настройка займёт **5 минут**. После этого участники будут получать красивые email уведомления!

Полная документация: `EMAIL_SETUP.md`

