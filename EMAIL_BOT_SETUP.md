# 📧 Настройка Email-бота - Полная инструкция

## 🎯 Что это?

Email-бот **полностью дублирует функционал Telegram-бота**, но работает через электронную почту.

**Пользователь может выбрать:**
- 💬 Telegram-бот → регистрация через Telegram
- 📧 Email-бот → регистрация через почту

Все данные хранятся в одной базе данных!

---

## 🚀 Быстрая настройка (5 минут)

### Шаг 1: Настройте SMTP/IMAP на Mail.ru

Вам НЕ нужны дополнительные настройки Mail.ru - всё работает сразу!

### Шаг 2: Добавьте переменные в Render

1. Откройте: https://dashboard.render.com
2. Ваш Worker: **summit-registration-bot**
3. **Environment** → **Add Environment Variable**
4. Добавьте **10 переменных**:

```bash
# SMTP (отправка писем)
SMTP_HOST=smtp.mail.ru
SMTP_PORT=587
SMTP_USER=support@alef-bet.tech
SMTP_PASSWORD=Eshiva11!
FROM_EMAIL=support@alef-bet.tech
FROM_NAME=Aleph Bet Foresight Summit

# IMAP (получение писем)
IMAP_HOST=imap.mail.ru
IMAP_PORT=993
IMAP_USER=support@alef-bet.tech
IMAP_PASSWORD=Eshiva11!
```

5. **Save Changes**

⚠️ **ВАЖНО:** После деплоя **СМЕНИТЕ ПАРОЛЬ** на почте!

### Шаг 3: Обновите Procfile

Нужно запускать одновременно **Telegram-бот** и **Email-бот**.

Render.yaml обновится автоматически после push.

---

## 🌐 Интеграция с сайтом

### Вариант 1: Две кнопки на сайте

```html
<!-- На вашей лендинг-странице Tilda -->

<div class="registration-choice">
  <h2>Выберите удобный способ регистрации:</h2>
  
  <!-- Кнопка Telegram -->
  <a href="https://t.me/AlephBetForesightSummitbot?start=register" 
     class="btn btn-telegram">
    💬 Зарегистрироваться через Telegram
  </a>
  
  <!-- Кнопка Email -->
  <a href="mailto:support@alef-bet.tech?subject=Регистрация&body=СТАРТ" 
     class="btn btn-email">
    📧 Зарегистрироваться через Email
  </a>
</div>
```

### Вариант 2: Форма с выбором

```html
<form id="registration-form">
  <h2>Регистрация на Summit</h2>
  
  <label>Выберите способ связи:</label>
  <select id="contact-method">
    <option value="telegram">💬 Telegram</option>
    <option value="email">📧 Email</option>
  </select>
  
  <div id="email-input" style="display:none;">
    <input type="email" id="user-email" placeholder="Ваш email">
  </div>
  
  <button type="submit">Начать регистрацию</button>
</form>

<script>
document.getElementById('contact-method').addEventListener('change', function() {
  if (this.value === 'email') {
    document.getElementById('email-input').style.display = 'block';
  } else {
    document.getElementById('email-input').style.display = 'none';
  }
});

document.getElementById('registration-form').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const method = document.getElementById('contact-method').value;
  
  if (method === 'telegram') {
    window.open('https://t.me/AlephBetForesightSummitbot?start=register', '_blank');
  } else {
    const email = document.getElementById('user-email').value;
    if (email) {
      window.location.href = `mailto:support@alef-bet.tech?subject=Регистрация&body=СТАРТ`;
    } else {
      alert('Пожалуйста, введите ваш email');
    }
  }
});
</script>
```

### Вариант 3: Tilda Zero Block

В Tilda создайте Zero Block с двумя кнопками:

1. **Кнопка 1 (Telegram):**
   - Текст: "💬 Telegram-регистрация"
   - Ссылка: `https://t.me/AlephBetForesightSummitbot?start=register`
   - Открыть: в новом окне

2. **Кнопка 2 (Email):**
   - Текст: "📧 Email-регистрация"
   - Ссылка: `mailto:support@alef-bet.tech?subject=Регистрация&body=СТАРТ`
   - Открыть: по умолчанию

---

## 📧 Как работает Email-бот

### 1. Пользователь отправляет письмо

**Кому:** support@alef-bet.tech  
**Тема:** Регистрация  
**Текст:** СТАРТ

### 2. Бот отвечает с выбором языка

```
Шалом!

Добро пожаловать на регистрацию Aleph Bet Foresight Summit!

🌍 Выберите язык:

Ответьте на это письмо одним словом:
1. РУССКИЙ
2. ENGLISH  
3. עברית

После выбора языка вы получите дальнейшие инструкции.
```

### 3. Пользователь выбирает язык

**Ответ:** РУССКИЙ

### 4. Бот отправляет приветствие и даты

```
✡️ Поздравляем — вы со своим народом!
Шалом! Меня зовут Шломо

🎉 Вы приглашены на Zoom-встречу...

Ответьте на это письмо с номером даты:

1. 🗓️ Сегодня, 22 октября (19:00)
2. 🗓️ Завтра, 23 октября (19:00)  
3. 🗓️ Послезавтра, 25 октября (19:00)
```

### 5. Пользователь выбирает дату

**Ответ:** 2

### 6. Бот отправляет подтверждение

```
✅ Регистрация завершена!

🎫 Ваш ID: №12001
🔑 Код активации: 123456
📅 Дата встречи: 23 октября 2025

⚠️ Для активации необходимо присутствовать на Zoom-встрече
📋 Полная инструкция отправлена вам отдельным письмом
```

### 7. Пользователь может запросить меню

**Ответ:** МЕНЮ

```
📱 Главное меню

Ваш ID: №12001
Ваш код активации: 123456

Доступные команды:
1. ID - напомнить ID
2. КОД - напомнить код
3. ИНСТРУКЦИЯ - инструкция Zoom
4. ПОМОЩЬ - справка
```

---

## 🔄 Параллельная работа Telegram + Email

### Обновите `bot.py`:

Добавьте в конец файла:

```python
# Запуск Email-бота в отдельном потоке
import threading
from email_bot import start_email_bot

def run_bots():
    """Запуск обоих ботов параллельно"""
    # Telegram bot в главном потоке
    telegram_thread = threading.Thread(target=application.run_polling)
    telegram_thread.start()
    
    # Email bot в фоновом потоке
    email_thread = threading.Thread(target=start_email_bot, daemon=True)
    email_thread.start()
    
    # Ждём Telegram бота
    telegram_thread.join()

if __name__ == '__main__':
    run_bots()
```

---

## 🧪 Тестирование

### 1. Отправьте письмо на support@alef-bet.tech

```
Тема: Тест
Текст: СТАРТ
```

### 2. Проверьте ответ (~1 минута)

Должно прийти письмо с выбором языка.

### 3. Ответьте: РУССКИЙ

### 4. Должна прийти анкета с датами

### 5. Проверьте логи на Render

```
Email bot started
Processing email from test@example.com
Sent welcome email to test@example.com
```

---

## 📊 Статистика и админ-панель

**Email-пользователи видны в админ-панели Telegram!**

Админ-команды:
- `/admin` - общая статистика (включая email-регистрации)
- `/sendlink` - отправить Zoom-ссылку (можно выбрать email-рассылку)
- `/export` - экспорт всех данных (Telegram + Email)

---

## 🔒 Безопасность

### ⚠️ КРИТИЧНО:

1. **Смените пароль** после деплоя:
   - Зайдите на mail.ru
   - Смените пароль на почте
   - Обновите `SMTP_PASSWORD` и `IMAP_PASSWORD` на Render

2. **НЕ публикуйте пароли** в:
   - Git-репозиториях
   - Скриншотах
   - Сообщениях

3. **Используйте .env** для локальной разработки:
   ```bash
   SMTP_PASSWORD=ваш_новый_пароль
   IMAP_PASSWORD=ваш_новый_пароль
   ```

---

## 💡 Дополнительные возможности

### Что уже работает:
- ✅ Регистрация через email
- ✅ Выбор языка (ru/en/he)
- ✅ Выбор даты Zoom
- ✅ Отправка ID и кода активации
- ✅ Отправка инструкций
- ✅ Меню и команды

### Что можно добавить:
- 📊 Автоматические напоминания перед Zoom
- 📧 Email-рассылка объявлений из админки
- 🔔 Уведомления о новых событиях
- 📝 Сбор дополнительной информации (телефон, город и т.д.)
- 📸 Прикрепление QR-кода в письмо

**Хотите что-то добавить? Скажите!**

---

## 🚀 Готово!

После настройки пользователи смогут регистрироваться **двумя способами**:

1. 💬 **Telegram** → быстро, удобно, с кнопками
2. 📧 **Email** → классический способ, без установки приложений

Все данные в **одной базе**, вся статистика в **одной админке**!

---

## 📞 Поддержка

Если что-то не работает:
1. Проверьте переменные окружения на Render
2. Посмотрите логи: Dashboard → Worker → Logs
3. Убедитесь, что пароль от почты правильный

**Готово к запуску! 🎉**

