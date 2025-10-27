"""
Многоязычная поддержка для бота Aleph Bet Foresight Summit
Русский, Английский, Иврит
"""

TEXTS = {
    'ru': {
        # Приветствие
        'welcome_choose_lang': '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:',
        
        # Основное приветствие от Шломо
        'greeting': (
            '✡️ Поздравляем — вы со своим народом!\n'
            'Шалом! Меня зовут Шломо\n\n'
            '🎉 Вы приглашены на Zoom-встречу с оргкомитетом для знакомства с организаторами. '
            'Также на ней, вы сможете выбрать ту миссию, которая Вам по душе!\n\n'
            'Когда Вы хотите присоединиться к ZOOM встрече? Сегодня, завтра или послезавтра?'
        ),
        
        # Выбор даты
        'choose_date': '📅 Выберите удобную дату для Zoom-встречи:',
        'date_full': '❌ К сожалению, на эту дату все места заняты. Пожалуйста, выберите другую дату.',
        'meeting_confirmed': 'Отлично! Мы будем очень рады Вас видеть на нашей первой встрече!',
        
        # Дни недели
        'today': 'Сегодня',
        'tomorrow': 'Завтра',
        'day_after_tomorrow': 'Послезавтра',
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        
        # ID и код
        'id_and_code': (
            '🎫 Ваш ID: №{participant_id}\n'
            '📲 Уникальный код для активации ID: {activation_code}\n\n'
            '⚠️ Для активации Вашего ID необходимо присутствовать на Zoom-встрече.\n'
            'После активации можно выбрать форму участия в саммите.'
        ),
        
        # Меню
        'main_menu': '📱 Главное меню:',
        'btn_remind_id': '📜 Напомнить номер ID',
        'btn_remind_code': '🔑 Напомнить код активации',
        'btn_remind_date': '📅 Напомнить дату встречи',
        'btn_reschedule': '🔄 Перенести встречу',
        'btn_change_language': '🌍 Изменить язык',
        'btn_how_activate': '❓ Как активировать ID?',
        'btn_materials': '📚 Дополнительные материалы',
        'btn_back_to_menu': '🔙 Меню',
        'btn_instruction': '📖 Инструкция',
        'btn_video': '🎬 Видео',
        'btn_torah_page': '🌐 Система лидерства Торы',
        
        # Напоминания
        'your_id': '📜 Ваш ID: №{participant_id}',
        'your_code': '🔑 Ваш код активации: {activation_code}',
        'your_date': '📅 Ваша дата Zoom-встречи: {zoom_date}',
        
        # Активация
        'how_to_activate': (
            '❓ **Как активировать ID?**\n\n'
            'В день ZOOM встречи, Вы получите ссылку на онлайн встречу, и точное время её проведения, '
            'на которой Вы должны будете отправить свой уникальный код в общий чат.\n\n'
            'По окончанию ZOOM встречи Ваш ID будет активирован.\n\n'
            'Если Вы используете ZOOM в первый раз, то Вы можете ознакомиться с инструкцией:'
        ),
        
        # Инструкция по Zoom (БОЛЬШАЯ!)
        'zoom_instruction': '''📖 **ИНСТРУКЦИЯ ПО ZOOM**

**Что нужно сделать — кратко:**

1. Кликните по присланной ссылке на встречу (или вставьте её в браузер).
2. Разрешите браузеру открыть Zoom и скачайте и установите приложение, если будет предложено.
3. При входе укажите ваше имя (как хотите, чтобы вас видели).
4. Включите/проверьте микрофон и камеру (если нужно).
5. Найдите кнопку «Чат / Chat» и введите ваш уникальный код — отправьте его в общий чат («All» / «Все»).

**Подробная пошаговая инструкция:**

**A. Вход с компьютера (Windows или Mac)**

1. Откройте письмо/сообщение со ссылкой и кликните по ссылке.

2. Браузер откроет страницу Zoom. Если Zoom не установлен, браузер предложит скачать приложение — нажмите Download & Run / Launch Meeting → начнётся скачивание установщика.

3. **Windows:** запустите скачанный .exe и следуйте мастеру установки.
   **Mac:** откройте .pkg или .dmg и разрешите установку.
   (Если хотите, можно выбрать «Join from your browser» — присоединиться без установки, но функционал иногда урезан.)

4. После установки приложение автоматически откроется и подключит вас к встрече.

5. При подключении появится окно с выбором имени — введите, как вас должно видеть организатор.

6. Разрешите доступ к микрофону и камере, если хотите говорить/показывать видео.

7. Перед началом проверьте звук: в окне обычно есть кнопка Test Speaker & Microphone.

8. Если требуется пароль (Password) — введите его (обычно в письме рядом со ссылкой).

**B. Вход с телефона (Android / iPhone)**

1. Кликните ссылку в письме/сообщении на телефоне. Откроется страница, предложит открыть в приложении Zoom.

2. Если у вас нет приложения — нажмите на ссылку для скачивания: Google Play (Android) или App Store (iPhone). Установите Zoom.

3. Откройте ссылку ещё раз — Zoom откроется и подключит вас к встрече.

4. Введите имя при подключении, разрешите доступ к микрофону/камере.

5. Проверьте, что звук/микрофон работают (в приложении есть кнопки микрофона и камеры внизу экрана).

**Основные элементы управления:**

• **Mute / Unmute** (микрофон): значок микрофона — нажмите, чтобы отключать/включать звук.
• **Start Video / Stop Video** (камера): значок камеры — включить/выключить камеру.
• **Participants** (Участники): список участников.
• **Chat** (Чат): кнопка для открытия боковой панели чата — туда вы отправите код.
• **Reactions / Raise Hand**: если хотите поднять виртуальную руку или поставить реакцию.
• **Leave Meeting**: выйти из встречи.

**Как отправить ваш уникальный код в общий чат:**

1. Нажмите кнопку **Chat** (обычно внизу окна Zoom). Откроется панель чата справа (на телефоне — всплывающее окно).

2. В текстовое поле вставьте или введите ваш код и отправьте — нажмите Enter или кнопку отправки.

**Если что-то не работает — быстрые решения:**

• **Не запускается Zoom / страница висит:** перезапустите браузер и попробуйте снова; если не помогает, скачайте и установите приложение Zoom вручную с официального сайта.

• **Не слышно других / вас не слышно:** проверьте, не нажата ли кнопка Mute; проверьте системные настройки звука; попробуйте подключиться по телефону (звук по телефону).

• **Требует регистрации перед входом:** следуйте форме регистрации — обычно нужно ввести имя и e-mail, затем нажать «Register», и вам пришлют ссылку на вход.

• **Не видите чат:** на компьютере нажмите кнопку Chat внизу; на телефоне нажмите три точки More → Chat.

**Ещё несколько полезных советов:**

• Подключитесь за 5–10 минут до начала, чтобы успеть проверить звук и камеру.
• Если в комнате много людей, держите микрофон выключенным, когда не говорите.
• Если нужно отправить код сразу после захода — то заранее сохраните код в заметках телефона/компьютера, чтобы легко скопировать и вставить.''',
        
        # Ссылки на материалы
        'torah_leadership_intro': '🌐 **Система лидерства Торы в цифровую эпоху**\n\nПознакомьтесь с моделью управления, данной Б-гом через Итро Моше Рабейну:',
        'materials_menu': '📚 **Дополнительные материалы:**\n\nВыберите, что хотите посмотреть:',
        
        # Другое
        'not_registered': 'Вы еще не зарегистрированы. Используйте /start для регистрации.',
        'language_changed': '✅ Язык изменён на русский',
    },
    
    'en': {
        # Welcome
        'welcome_choose_lang': '🕊️ Welcome! Добро пожаловать! ברוכים הבאים!\n\nPlease choose language / Выберите язык / בחר שפה:',
        
        # Main greeting from Shlomo
        'greeting': (
            '✡️ Congratulations — you\'re with your people!\n'
            'Shalom! My name is Shlomo\n\n'
            '🎉 You are invited to a Zoom meeting with the organizing committee to meet the organizers. '
            'Also, you will be able to choose the mission that suits you best!\n\n'
            'When would you like to join the ZOOM meeting? Today, tomorrow, or the day after tomorrow?'
        ),
        
        # Date selection
        'choose_date': '📅 Choose a convenient date for the Zoom meeting:',
        'date_full': '❌ Unfortunately, all spots are filled for this date. Please choose another date.',
        'meeting_confirmed': 'Excellent! We will be very happy to see you at our first meeting!',
        
        # Days of week
        'today': 'Today',
        'tomorrow': 'Tomorrow',
        'day_after_tomorrow': 'Day after tomorrow',
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        
        # ID and code
        'id_and_code': (
            '🎫 Your ID: №{participant_id}\n'
            '📲 Unique activation code: {activation_code}\n\n'
            '⚠️ To activate your ID, you must attend the Zoom meeting.\n'
            'After activation, you can choose your participation format in the summit.'
        ),
        
        # Menu
        'main_menu': '📱 Main menu:',
        'btn_remind_id': '📜 Remind my ID',
        'btn_remind_code': '🔑 Remind activation code',
        'btn_remind_date': '📅 Remind meeting date',
        'btn_reschedule': '🔄 Reschedule meeting',
        'btn_change_language': '🌍 Change language',
        'btn_how_activate': '❓ How to activate ID?',
        'btn_materials': '📚 Additional Materials',
        'btn_back_to_menu': '🔙 Menu',
        'btn_instruction': '📖 Instruction',
        'btn_video': '🎬 Video',
        'btn_torah_page': '🌐 Torah Leadership System',
        
        # Reminders
        'your_id': '📜 Your ID: №{participant_id}',
        'your_code': '🔑 Your activation code: {activation_code}',
        'your_date': '📅 Your Zoom meeting date: {zoom_date}',
        
        # Activation
        'how_to_activate': (
            '❓ **How to activate ID?**\n\n'
            'On the day of the ZOOM meeting, you will receive a link to the online meeting and the exact time, '
            'where you will need to send your unique code to the general chat.\n\n'
            'After the ZOOM meeting ends, your ID will be activated.\n\n'
            'If you are using ZOOM for the first time, you can read the instruction:'
        ),
        
        # Zoom instruction
        'zoom_instruction': '''📖 **ZOOM INSTRUCTION**

**What to do — briefly:**

1. Click on the sent meeting link (or paste it into your browser).
2. Allow the browser to open Zoom and download and install the app if prompted.
3. Enter your name when joining (how you want to be seen).
4. Enable/check your microphone and camera (if needed).
5. Find the «Chat» button and enter your unique code — send it to the general chat («All»).

**Detailed step-by-step instructions:**

**A. Joining from computer (Windows or Mac)**

1. Open the email/message with the link and click on it.

2. Browser will open Zoom page. If Zoom is not installed, browser will suggest downloading — click Download & Run / Launch Meeting.

3. **Windows:** run the downloaded .exe and follow the installation wizard.
   **Mac:** open .pkg or .dmg and allow installation.

4. After installation, the app will automatically open and connect you to the meeting.

5. When connecting, a window will appear for name selection — enter how you want the organizer to see you.

6. Allow access to microphone and camera if you want to speak/show video.

7. Before starting, test your audio: usually there's a Test Speaker & Microphone button.

**B. Joining from phone (Android / iPhone)**

1. Click the link in the email/message on your phone. A page will open suggesting to open in Zoom app.

2. If you don't have the app — click the download link: Google Play (Android) or App Store (iPhone). Install Zoom.

3. Open the link again — Zoom will open and connect you to the meeting.

4. Enter your name when connecting, allow access to microphone/camera.

**Main controls:**

• **Mute / Unmute** (microphone): microphone icon — click to turn sound on/off.
• **Start Video / Stop Video** (camera): camera icon — turn camera on/off.
• **Participants**: participant list.
• **Chat**: button to open chat panel — where you'll send your code.
• **Leave Meeting**: exit the meeting.

**How to send your unique code to general chat:**

1. Click the **Chat** button (usually at the bottom of Zoom window). Chat panel will open on the right.

2. In the text field, paste or enter your code and send — press Enter or send button.

**Useful tips:**

• Connect 5–10 minutes before start to test audio and camera.
• If there are many people, keep microphone muted when not speaking.
• Save your code in phone/computer notes beforehand for easy copying.''',
        
        # Materials links
        'torah_leadership_intro': '🌐 **Torah Leadership System in the Digital Age**\n\nDiscover the management model given by G-d through Yitro to Moshe Rabbeinu:',
        'materials_menu': '📚 **Additional Materials:**\n\nChoose what you want to see:',
        
        # Other
        'not_registered': 'You are not registered yet. Use /start to register.',
        'language_changed': '✅ Language changed to English',
    },
    
    'he': {
        # Welcome
        'welcome_choose_lang': '🕊️ ברוכים הבאים! Welcome! Добро пожаловать!\n\nבחר שפה / Choose language / Выберите язык:',
        
        # Main greeting from Shlomo
        'greeting': (
            '✡️ ברכות - אתה עם העם שלך!\n'
            'שלום! שמי שלמה\n\n'
            '🎉 אתה מוזמן לפגישת Zoom עם הוועדה המארגנת כדי להכיר את המארגנים. '
            'כמו כן, תוכל לבחור את המשימה המתאימה לך ביותר!\n\n'
            'מתי תרצה להצטרף לפגישת ZOOM? היום, מחר או מחרתיים?'
        ),
        
        # Date selection
        'choose_date': '📅 בחר תאריך נוח לפגישת Zoom:',
        'date_full': '❌ למרבה הצער, כל המקומות תפוסים לתאריך זה. אנא בחר תאריך אחר.',
        'meeting_confirmed': 'מצוין! נשמח מאוד לראות אותך בפגישה הראשונה שלנו!',
        
        # Days of week
        'today': 'היום',
        'tomorrow': 'מחר',
        'day_after_tomorrow': 'מחרתיים',
        'monday': 'יום שני',
        'tuesday': 'יום שלישי',
        'wednesday': 'יום רביעי',
        'thursday': 'יום חמישי',
        'friday': 'יום שישי',
        
        # ID and code
        'id_and_code': (
            '🎫 ה-ID שלך: №{participant_id}\n'
            '📲 קוד הפעלה ייחודי: {activation_code}\n\n'
            '⚠️ להפעלת ה-ID שלך, עליך להשתתף בפגישת Zoom.\n'
            'לאחר ההפעלה, תוכל לבחור את פורמט ההשתתפות שלך בפסגה.'
        ),
        
        # Menu
        'main_menu': '📱 תפריט ראשי:',
        'btn_remind_id': '📜 להזכיר את ה-ID',
        'btn_remind_code': '🔑 להזכיר קוד הפעלה',
        'btn_remind_date': '📅 להזכיר תאריך פגישה',
        'btn_reschedule': '🔄 לשנות תאריך פגישה',
        'btn_change_language': '🌍 לשנות שפה',
        'btn_how_activate': '❓ איך להפעיל ID?',
        'btn_materials': '📚 חומרים נוספים',
        'btn_back_to_menu': '🔙 תפריט',
        'btn_instruction': '📖 הוראות',
        'btn_video': '🎬 וידאו',
        'btn_torah_page': '🌐 מערכת המנהיגות של התורה',
        
        # Reminders
        'your_id': '📜 ה-ID שלך: №{participant_id}',
        'your_code': '🔑 קוד ההפעלה שלך: {activation_code}',
        'your_date': '📅 תאריך פגישת Zoom שלך: {zoom_date}',
        
        # Activation
        'how_to_activate': (
            '❓ **איך להפעיל ID?**\n\n'
            'ביום פגישת ZOOM, תקבל קישור לפגישה המקוונת והשעה המדויקת, '
            'שבה תצטרך לשלוח את הקוד הייחודי שלך לצ\'אט הכללי.\n\n'
            'בסיום פגישת ZOOM, ה-ID שלך יופעל.\n\n'
            'אם אתה משתמש ב-ZOOM בפעם הראשונה, תוכל לקרוא את ההוראות:'
        ),
        
        # Zoom instruction
        'zoom_instruction': '''📖 **הוראות ZOOM**

**מה לעשות - בקצרה:**

1. לחץ על הקישור שנשלח לפגישה (או הדבק אותו בדפדפן).
2. אפשר לדפדפן לפתוח את Zoom והורד והתקן את האפליקציה אם יוצע.
3. בכניסה הזן את שמך (איך שתרצה שיראו אותך).
4. הפעל/בדוק מיקרופון ומצלמה (אם צריך).
5. מצא את כפתור «Chat / צ'אט» והזן את הקוד הייחודי שלך — שלח אותו לצ'אט הכללי («All» / «כולם»).

**הוראות מפורטות שלב אחר שלב:**

**א. כניסה ממחשב (Windows או Mac)**

1. פתח את האימייל/הודעה עם הקישור ולחץ עליו.

2. הדפדפן יפתח את עמוד Zoom. אם Zoom לא מותקן, הדפדפן יציע להוריד — לחץ Download & Run / Launch Meeting.

3. **Windows:** הפעל את קובץ ה-.exe שהורד ועקוב אחר אשף ההתקנה.
   **Mac:** פתח .pkg או .dmg ואשר התקנה.

4. לאחר ההתקנה, האפליקציה תיפתח אוטומטית ותחבר אותך לפגישה.

5. בהתחברות, יופיע חלון לבחירת שם — הזן איך תרצה שהמארגן יראה אותך.

6. אפשר גישה למיקרופון ולמצלמה אם תרצה לדבר/להראות וידאו.

**ב. כניסה מטלפון (Android / iPhone)**

1. לחץ על הקישור באימייל/הודעה בטלפון. יפתח עמוד שיציע לפתוח באפליקציית Zoom.

2. אם אין לך את האפליקציה — לחץ על הקישור להורדה: Google Play (Android) או App Store (iPhone). התקן את Zoom.

3. פתח את הקישור שוב — Zoom ייפתח ויחבר אותך לפגישה.

**כיצד לשלוח את הקוד הייחודי שלך לצ'אט הכללי:**

1. לחץ על כפתור **Chat** (בדרך כלל בתחתית חלון Zoom). פאנל הצ'אט ייפתח מימין.

2. בשדה הטקסט, הדבק או הזן את הקוד שלך ושלח — לחץ Enter או כפתור שליחה.

**טיפים שימושיים:**

• התחבר 5–10 דקות לפני ההתחלה כדי לבדוק שמע ומצלמה.
• אם יש הרבה אנשים, שמור על המיקרופון כבוי כשלא מדברים.
• שמור את הקוד שלך בהערות הטלפון/מחשב מראש להעתקה קלה.''',
        
        # Materials links
        'torah_leadership_intro': '🌐 **מערכת המנהיגות של התורה בעידן הדיגיטלי**\n\nהכר את מודל הניהול שניתן על ידי הקב"ה דרך יתרו למשה רבינו:',
        'materials_menu': '📚 **חומרים נוספים:**\n\nבחר מה אתה רוצה לראות:',
        
        # Other
        'not_registered': 'אתה עדיין לא רשום. השתמש ב-/start כדי להירשם.',
        'language_changed': '✅ השפה שונתה לעברית',
    }
}

# Language names for display
LANGUAGE_NAMES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English',
    'he': '🇮🇱 עברית'
}

def get_text(language: str, key: str, **kwargs) -> str:
    """Get text in specified language"""
    if language not in TEXTS:
        language = 'ru'
    
    text = TEXTS[language].get(key, TEXTS['ru'].get(key, f'[Missing: {key}]'))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text

