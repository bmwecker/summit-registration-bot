# 📧 Настройка Email уведомлений

## 🎯 Зачем нужна email интеграция?

Email уведомления позволяют:
- ✅ Отправлять подтверждение регистрации с ID и кодом
- ✅ Присылать Zoom-ссылку перед встречей
- ✅ Делать массовые рассылки участникам
- ✅ Напоминать о встречах

---

## 🔧 Настройка SMTP

### Вариант 1: Gmail (Рекомендуется)

#### Шаг 1: Создайте App Password

1. Зайдите в ваш Google Account: https://myaccount.google.com
2. **Security** → **2-Step Verification** (включите если не включено)
3. **Security** → **App passwords**
4. Выберите:
   - App: **Mail**
   - Device: **Other** → введите "Aleph Bet Bot"
5. Скопируйте сгенерированный пароль (16 символов)

#### Шаг 2: Добавьте в Environment Variables

На **Render**:
1. Dashboard → Ваш Background Worker
2. **Environment** → **Add Environment Variable**
3. Добавьте следующие переменные:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=ваш_app_password_из_шага_1
FROM_EMAIL=your-email@gmail.com
FROM_NAME=Aleph Bet Foresight Summit
```

**Локально (.env файл):**

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=ваш_app_password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=Aleph Bet Foresight Summit
```

---

### Вариант 2: Другие почтовые сервисы

#### Mail.ru

```env
SMTP_HOST=smtp.mail.ru
SMTP_PORT=587
SMTP_USER=your-email@mail.ru
SMTP_PASSWORD=ваш_пароль
FROM_EMAIL=your-email@mail.ru
FROM_NAME=Aleph Bet Foresight Summit
```

#### Yandex

```env
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=587
SMTP_USER=your-email@yandex.ru
SMTP_PASSWORD=ваш_пароль
FROM_EMAIL=your-email@yandex.ru
FROM_NAME=Aleph Bet Foresight Summit
```

#### Outlook/Hotmail

```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=ваш_пароль
FROM_EMAIL=your-email@outlook.com
FROM_NAME=Aleph Bet Foresight Summit
```

---

## 🧪 Проверка настройки

После настройки SMTP:

1. Перезапустите бота на Render
2. Зарегистрируйте тестового пользователя с реальным email
3. Проверьте, пришло ли письмо с подтверждением

---

## 📝 Как работает

### Автоматические email:

1. **При регистрации** (если email собран):
   - Подтверждение регистрации
   - ID участника
   - Код активации
   - Дата Zoom-встречи

### Из админ-панели:

**Планируется добавить:**
- Кнопка "Отправить email с Zoom-ссылкой"
- Массовая рассылка по email
- Напоминания перед встречей

---

## 🔒 Безопасность

⚠️ **ВАЖНО:**

1. **НЕ** публикуйте SMTP_PASSWORD в коде!
2. Используйте **App Passwords**, а не основной пароль
3. Храните пароли только в Environment Variables
4. Для Gmail включите 2-Factor Authentication

---

## ❌ Если email не работает

### Проверьте:

1. **SMTP_USER и SMTP_PASSWORD** правильно указаны
2. **SMTP_HOST и SMTP_PORT** соответствуют вашему провайдеру
3. Для Gmail используется **App Password**, а не обычный пароль
4. **2FA** включена для Gmail
5. Проверьте логи бота на Render - есть ли ошибки SMTP

### Типичные ошибки:

```
SMTPAuthenticationError: Username and Password not accepted
```
→ Неверный пароль или не используется App Password

```
SMTPServerDisconnected: Connection unexpectedly closed
```
→ Неверный SMTP_HOST или SMTP_PORT

```
TimeoutError: timed out
```
→ Проблема с сетью или блокировка порта

---

## 📊 Лимиты отправки

### Gmail:
- **500 писем в день** для обычных аккаунтов
- **2000 писем в день** для Google Workspace

### Mail.ru:
- **100 писем в час**

### Yandex:
- **500 писем в день**

**Совет:** Для больших рассылок используйте сервисы вроде SendGrid или Mailgun (бесплатно до 100 писем/день).

---

## 🚀 Готово!

После настройки SMTP бот будет автоматически отправлять email уведомления участникам!

Если email не настроен - бот просто пропускает отправку и продолжает работать через Telegram.

