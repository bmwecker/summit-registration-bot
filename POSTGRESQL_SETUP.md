# 🐘 PostgreSQL Setup для Render

## Зачем PostgreSQL?

Старая версия бота использовала SQLite, но на Render это проблема:
- SQLite файл теряется при каждом перезапуске
- Нет постоянного хранения данных
- PostgreSQL - надёжное решение для продакшена

## 🚀 Быстрая настройка

### Шаг 1: Создать PostgreSQL на Render

1. Зайдите на https://dashboard.render.com
2. Нажмите **New** → **PostgreSQL**
3. Заполните форму:

```
Name: summit-bot-db
Database: summit
User: summit_user
Region: Frankfurt (EU Central) или ближайший к вам
Instance Type: Free
```

4. Нажмите **Create Database**
5. Подождите ~2-3 минуты, пока БД создаётся

### Шаг 2: Получить Database URL

После создания БД:

1. Откройте созданную БД в Dashboard
2. Найдите раздел **Connections**
3. Скопируйте **Internal Database URL** (начинается с `postgres://` или `postgresql://`)

Пример:
```
postgresql://summit_user:paSSw0rd123@dpg-abc123.frankfurt-postgres.render.com/summit
```

### Шаг 3: Добавить в Background Worker

1. Перейдите в ваш Background Worker: `summit-registration-bot`
2. Откройте **Environment**
3. Нажмите **Add Environment Variable**
4. Заполните:

```
Key: DATABASE_URL
Value: (вставьте скопированный Internal Database URL)
```

5. Нажмите **Save Changes**

### Шаг 4: Перезапустить бота

1. В Dashboard Background Worker нажмите **Manual Deploy** → **Clear build cache & deploy**
2. Или просто сделайте коммит и пуш в GitHub - Render автоматически пересоберёт

```bash
git commit --allow-empty -m "Trigger redeploy"
git push origin main
```

## ✅ Проверка

### Проверить, что PostgreSQL работает:

1. Зайдите в **Logs** вашего Background Worker
2. Должны увидеть:

```
🚀 Aleph Bet Foresight Summit Bot started!
```

3. Отправьте `/start` боту в Telegram
4. Зарегистрируйтесь
5. Отправьте `/admin` и посмотрите статистику

Если видите данные - всё работает! 🎉

### Проверить подключение к БД (опционально):

На Render в настройках PostgreSQL есть **Shell** - можно подключиться и посмотреть таблицы:

```sql
-- Подключиться к БД
\c summit

-- Посмотреть таблицы
\dt

-- Посмотреть участников
SELECT * FROM participants;

-- Посчитать участников
SELECT COUNT(*) FROM participants;
```

## 🔄 Миграция данных (если были данные в старом SQLite)

Если у вас уже были участники в старой версии бота:

### Шаг 1: Экспортировать из SQLite

```bash
# На локальной машине
sqlite3 summit_bot.db
.mode csv
.headers on
.output participants.csv
SELECT * FROM participants;
.quit
```

### Шаг 2: Импортировать в PostgreSQL

1. Подключитесь к PostgreSQL через Shell на Render
2. Или используйте скрипт:

```python
# migrate_to_postgres.py
import sqlite3
import psycopg2
import os

# SQLite
sqlite_conn = sqlite3.connect('summit_bot.db')
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT * FROM participants")
rows = sqlite_cursor.fetchall()

# PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

for row in rows:
    pg_cursor.execute("""
        INSERT INTO participants 
        (telegram_id, username, first_name, participant_type, 
         participant_id, activation_code, zoom_date, registration_date, 
         language, is_activated, activation_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, row[1:])  # Пропускаем первый id

pg_conn.commit()
print(f"Migrated {len(rows)} participants")
```

## 🛠️ Локальная разработка

При разработке локально бот автоматически использует SQLite:

```python
# В database.py
DATABASE_URL = os.getenv("DATABASE_URL")  # На Render есть, локально нет
USE_POSTGRES = DATABASE_URL is not None    # False локально

if USE_POSTGRES:
    # PostgreSQL
else:
    # SQLite (файл summit_bot.db)
```

Это удобно для тестирования!

## 📊 Мониторинг БД

### В Render Dashboard:

1. Откройте вашу PostgreSQL БД
2. Смотрите метрики:
   - **Connections** - количество подключений
   - **Storage** - используемое место
   - **CPU / Memory** - нагрузка

### Free Plan лимиты:

- Хранилище: 1 GB
- Connections: 100
- Автоматические бэкапы: НЕТ (только на платном)

⚠️ **Важно**: На Free плане нет автоматических бэкапов! Рекомендую периодически делать экспорт данных через админ-панель бота.

## 🔒 Безопасность

- ✅ Используйте Internal Database URL (внутри Render)
- ✅ Не публикуйте DATABASE_URL в коде
- ✅ SSL подключение включено по умолчанию
- ✅ Пароль генерируется автоматически Render

## 🆘 Troubleshooting

### Ошибка: "could not connect to server"

1. Проверьте, что PostgreSQL БД запущена (статус в Dashboard)
2. Проверьте DATABASE_URL в Environment Variables
3. Проверьте, что используете Internal Database URL, а не External

### Ошибка: "relation does not exist"

Таблицы не созданы. Бот должен создать их автоматически при первом запуске.

1. Перезапустите бота
2. Проверьте логи на ошибки

### База данных полная (1 GB лимит)

1. Экспортируйте старые данные через `/admin`
2. Удалите старые записи вручную через SQL Shell
3. Или перейдите на платный план ($7/месяц за 10 GB)

## 💡 Советы

1. **Регулярные экспорты**: Делайте экспорт данных через админ-панель хотя бы раз в неделю
2. **Мониторинг**: Следите за Storage в Dashboard
3. **Тестирование**: Локально используйте SQLite для быстрых тестов
4. **Апгрейд**: При росте базы переходите на платный план

---

**🐘 PostgreSQL настроен! Теперь у вас надёжное хранение данных!**

