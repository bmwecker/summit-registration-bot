# ⚡ Быстрый старт - Aleph Bet Foresight Summit Bot

## 🚀 За 5 минут

### Шаг 1: Логотип ⭐ ВАЖНО!

**Сохраните файл `aleph-beth.png` в корень проекта!**

Без логотипа бот будет работать, но не покажет красивую картинку при старте.

### Шаг 2: Локальный тест

```bash
# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
echo "TELEGRAM_BOT_TOKEN=ваш_токен" > .env

# Запустить
python bot.py
```

### Шаг 3: Проверка в Telegram

1. Найдите вашего бота: `@AlephBetForesightSummitbot`
2. Отправьте `/start`
3. Выберите язык
4. Проверьте, что всё работает

### Шаг 4: Деплой на Render (уже настроен!)

```bash
# Добавить логотип в git
git add aleph-beth.png

# Закоммитить изменения
git add -A
git commit -m "New bot version with PostgreSQL and admin panel"

# Отправить на GitHub
git push origin main
```

**Render автоматически обновит бота!** 🎉

### Шаг 5: Проверить PostgreSQL

1. Зайдите в Render Dashboard
2. Найдите Background Worker: `summit-registration-bot`
3. Проверьте Environment Variables:
   - ✅ `TELEGRAM_BOT_TOKEN` = ваш токен
   - ✅ `DATABASE_URL` = должна быть (от PostgreSQL)

Если `DATABASE_URL` нет:
1. New → PostgreSQL
2. Создайте БД
3. Скопируйте Internal Database URL
4. Добавьте в Environment Variables вашего Worker

## 🎯 Быстрая проверка функционала

### Как участник:

```
/start → выбрать язык → выбрать дату → получить ID и код
```

### Как админ:

```
/admin → выбрать нужную функцию
```

Ваш ID уже добавлен: `386965305`

## 📋 Что изменилось от старой версии?

| Старое | Новое |
|--------|-------|
| SQLite только | PostgreSQL на Render + SQLite локально |
| ID с 1 | ID с 12000 |
| Нет приветствия | Приветствие от Шломо с логотипом |
| Базовое меню | 6 пунктов + инструкция по Zoom |
| Нет лимитов | Лимит 290 человек на дату |
| Все дни | Исключая Шаббат (пт-сб) |
| Базовая админка | Полная админка с рассылками |

## ❗ Важные моменты

1. **Логотип**: Не забудьте добавить `aleph-beth.png`!
2. **PostgreSQL**: На Render обязательно нужна БД
3. **Админ-ID**: Уже добавлен ваш ID в коде
4. **Backup**: Старые файлы сохранены в `backup_old_bot/`

## 🆘 Если что-то не работает

### Локально:

```bash
# Проверить, что установлено
pip list | grep telegram

# Проверить .env
cat .env

# Посмотреть логи
python bot.py
```

### На Render:

1. Dashboard → Logs
2. Проверить последние сообщения
3. Если ошибка с БД - проверить `DATABASE_URL`

## 📞 Команды для быстрого доступа

- `/start` - Начать работу с ботом
- `/admin` - Админ-панель
- `/cancel` - Отменить текущую операцию

## ✅ Checklist перед деплоем

- [ ] Логотип `aleph-beth.png` добавлен
- [ ] Токен бота в `.env` (локально)
- [ ] Токен бота в Render Environment Variables
- [ ] PostgreSQL создан на Render
- [ ] `DATABASE_URL` добавлен в Environment Variables
- [ ] Код закоммичен и запушен в GitHub
- [ ] Render автоматически задеплоил

## 🎉 Готово!

Бот работает! Теперь можно:
- Тестировать регистрацию
- Проверить админ-панель
- Сделать тестовую рассылку
- Экспортировать данные

---

**Удачного саммита! 🕊️**

