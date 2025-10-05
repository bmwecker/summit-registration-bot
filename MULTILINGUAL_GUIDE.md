# 🌍 Многоязычный бот - Инструкция

Ваш бот `@AlephBetForesightSummitbot` теперь поддерживает **три языка**:
- 🇷🇺 Русский (ru)
- 🇬🇧 English (en)
- 🇮🇱 עברית (he)

---

## 🎯 Как это работает

### Автоматическое определение языка

Язык определяется через **параметр start** в URL с вашего сайта:

**Русская кнопка:**
```
https://t.me/AlephBetForesightSummitbot?start=ru
```

**English button:**
```
https://t.me/AlephBetForesightSummitbot?start=en
```

**כפתור עברי:**
```
https://t.me/AlephBetForesightSummitbot?start=he
```

Бот автоматически:
1. Определит язык из URL
2. Сохранит его в базе данных
3. Будет использовать этот язык для всех сообщений

---

## 🔄 Смена языка

Пользователь может сменить язык в любой момент:

### Во время регистрации:
- Кнопка **"🌍 Change Language / Сменить язык"**

### После регистрации:
- Команда `/menu`
- Кнопка **"🌍 Change Language / Сменить язык"**

---

## 🌐 Интеграция с сайтом Tilda

### Пример 1: Три отдельные кнопки

#### HTML/CSS для Tilda Zero Block:

```html
<!-- Русская кнопка -->
<a href="https://t.me/AlephBetForesightSummitbot?start=ru" 
   target="_blank" 
   class="summit-btn summit-btn-ru">
   🇷🇺 Регистрация на русском
</a>

<!-- English button -->
<a href="https://t.me/AlephBetForesightSummitbot?start=en" 
   target="_blank" 
   class="summit-btn summit-btn-en">
   🇬🇧 Register in English
</a>

<!-- כפתור עברי -->
<a href="https://t.me/AlephBetForesightSummitbot?start=he" 
   target="_blank" 
   class="summit-btn summit-btn-he">
   🇮🇱 הרשמה בעברית
</a>

<style>
.summit-btn {
  display: inline-block;
  padding: 15px 30px;
  margin: 10px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  font-size: 16px;
  transition: transform 0.2s;
}

.summit-btn:hover {
  transform: scale(1.05);
}

.summit-btn-ru {
  background: linear-gradient(135deg, #0039A6 0%, #D52B1E 100%);
  color: white;
}

.summit-btn-en {
  background: linear-gradient(135deg, #012169 0%, #C8102E 100%);
  color: white;
}

.summit-btn-he {
  background: linear-gradient(135deg, #0038B8 0%, #FFFFFF 100%);
  color: #0038B8;
}
</style>
```

### Пример 2: Автоматическая кнопка по языку страницы

Если ваш сайт на Tilda переключается между языками, используйте JavaScript:

```javascript
<script>
// Определяем язык страницы Tilda
var currentLang = document.documentElement.lang || 'ru';
var langMap = {
  'ru': 'ru',
  'en': 'en',
  'he': 'he',
  'iw': 'he' // Hebrew alternative code
};

var botLang = langMap[currentLang] || 'ru';
var botUrl = 'https://t.me/AlephBetForesightSummitbot?start=' + botLang;

// Устанавливаем URL для кнопки
document.getElementById('summit-reg-btn').href = botUrl;
</script>

<a id="summit-reg-btn" 
   href="https://t.me/AlephBetForesightSummitbot?start=ru" 
   target="_blank" 
   class="summit-btn">
   Зарегистрироваться / Register / הירשם
</a>
```

---

## 📊 База данных

### Новое поле: `language`

В таблице `participants` добавлено поле:
- `language TEXT DEFAULT 'ru'` - хранит выбранный язык пользователя

### Методы базы данных:

```python
# Получить язык пользователя
language = db.get_user_language(user_id)

# Установить язык пользователя
db.set_user_language(user_id, 'en')
```

---

## 📝 Структура файлов

```
summit-registration-bot/
├── bot.py                      # Многоязычный бот (новый!)
├── bot_old_russian_only.py     # Резервная копия (только русский)
├── bot_multilang.py            # Исходник многоязычной версии
├── database.py                 # БД с поддержкой языков
├── languages.py                # Все тексты на трёх языках
├── requirements.txt
└── ...
```

---

## 🔧 Добавление нового языка

Если нужно добавить ещё один язык (например, французский):

### 1. Добавьте переводы в `languages.py`:

```python
TEXTS = {
    'ru': { ... },
    'en': { ... },
    'he': { ... },
    'fr': {  # Новый язык!
        'welcome': '🕊️ Bienvenue à l\'inscription au sommet!...',
        'btn_individual': '🔘 Je suis avec mon peuple',
        # ... все остальные ключи
    }
}

LANGUAGE_NAMES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English',
    'he': '🇮🇱 עברית',
    'fr': '🇫🇷 Français'  # Добавить в меню
}
```

### 2. Используйте параметр start:

```
https://t.me/AlephBetForesightSummitbot?start=fr
```

Вот и всё! Бот автоматически подхватит новый язык.

---

## 🚀 Деплой на Render

Все изменения уже готовы к деплою! Просто загрузите код на GitHub:

```powershell
git add .
git commit -m "Added multilingual support (ru, en, he)"
git push
```

Render автоматически обновит бота (~2 минуты).

---

## ✅ Тестирование

### Тест 1: Русский язык
```
https://t.me/AlephBetForesightSummitbot?start=ru
```
✅ Все сообщения на русском

### Тест 2: English
```
https://t.me/AlephBetForesightSummitbot?start=en
```
✅ All messages in English

### Тест 3: עברית
```
https://t.me/AlephBetForesightSummitbot?start=he
```
✅ כל ההודעות בעברית

### Тест 4: Смена языка
1. Запустить бота с любым языком
2. Нажать "🌍 Change Language"
3. Выбрать другой язык
✅ Интерфейс сменился

### Тест 5: Сохранение языка
1. Зарегистрироваться на одном языке
2. Закрыть бота
3. Открыть снова - `/menu`
✅ Язык сохранился

---

## 🎨 Примеры кнопок для сайта

### Минималистичные:

```html
<div style="text-align: center;">
  <a href="https://t.me/AlephBetForesightSummitbot?start=ru" 
     style="display:inline-block; margin:5px; padding:10px 20px; 
            background:#0088cc; color:white; border-radius:5px; 
            text-decoration:none;">
    🇷🇺 Русский
  </a>
  <a href="https://t.me/AlephBetForesightSummitbot?start=en" 
     style="display:inline-block; margin:5px; padding:10px 20px; 
            background:#0088cc; color:white; border-radius:5px; 
            text-decoration:none;">
    🇬🇧 English
  </a>
  <a href="https://t.me/AlephBetForesightSummitbot?start=he" 
     style="display:inline-block; margin:5px; padding:10px 20px; 
            background:#0088cc; color:white; border-radius:5px; 
            text-decoration:none;">
    🇮🇱 עברית
  </a>
</div>
```

### С градиентом:

```html
<a href="https://t.me/AlephBetForesightSummitbot?start=ru" 
   style="display:inline-block; padding:15px 30px; margin:10px;
          background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color:white; border-radius:25px; text-decoration:none;
          font-weight:bold; box-shadow:0 4px 15px rgba(0,0,0,0.2);">
  🇷🇺 Регистрация
</a>
```

---

## 📞 Поддержка RTL для иврита

Telegram автоматически поддерживает RTL (right-to-left) для иврита!

Тексты на иврите в `languages.py` отображаются справа налево автоматически.

---

## 🔍 Отладка

### Проблема: Язык не меняется

**Решение:** Проверьте логи:
```python
logger.info(f"User {user.id} language: {language}")
```

### Проблема: Иврит отображается неправильно

**Решение:** Убедитесь, что файл `languages.py` сохранён в UTF-8.

### Проблема: Кнопки на английском, текст на русском

**Решение:** Проверьте, что все ключи в TEXTS['en'] совпадают с TEXTS['ru'].

---

## 📈 Статистика по языкам

Добавьте админ-команду для просмотра статистики:

```python
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ADMIN_ID = YOUR_TELEGRAM_ID  # Замените!
    
    if update.effective_user.id != ADMIN_ID:
        return
    
    participants = db.get_all_participants()
    
    lang_stats = {'ru': 0, 'en': 0, 'he': 0}
    for p in participants:
        lang = p.get('language', 'ru')
        lang_stats[lang] = lang_stats.get(lang, 0) + 1
    
    text = f"""📊 Статистика регистраций:

Всего: {len(participants)}
🇷🇺 Русский: {lang_stats['ru']}
🇬🇧 English: {lang_stats['en']}
🇮🇱 עברית: {lang_stats['he']}
"""
    
    await update.message.reply_text(text)

# Добавьте в main():
application.add_handler(CommandHandler("admin", admin_stats))
```

---

## 🎯 Итоги

✅ **Один бот** вместо трёх  
✅ **Три языка**: русский, английский, иврит  
✅ **Автоопределение** языка из URL  
✅ **Смена языка** в любой момент  
✅ **Сохранение** выбора в БД  
✅ **Полная поддержка** RTL для иврита  
✅ **Легко добавить** новые языки  

---

## 📚 Дополнительно

- Все тексты в одном файле: `languages.py`
- Легко редактировать переводы
- Можно передать переводчику только `languages.py`
- Логика бота не зависит от языка

**Удачи с Aleph Bet Foresight Summit! 🕊️**
