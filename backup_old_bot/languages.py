"""
Multilingual text support for Summit Registration Bot
Supports: Russian (ru), English (en), Hebrew (he)
"""

TEXTS = {
    'ru': {
        # Welcome and main messages
        'welcome': '🕊️ Добро пожаловать на регистрацию саммита!\n\nПожалуйста, выберите, кто вы:',
        'already_registered': '✡️ Шалом, {name}!\n\nВы уже зарегистрированы.\n📜 Номер вашего сертификата: №{cert_number}\n\nИспользуйте /menu для доступа к информации.',
        'select_option': '🙏 Пожалуйста, выберите один из вариантов, чтобы продолжить:',
        
        # Participant types
        'btn_individual': '🔘 Я со своим народом',
        'btn_organization': '🔘 Наша организация со своим народом',
        
        # Greetings after type selection
        'greeting_individual': (
            '✡️ Шалом! Поздравляем — вы со своим народом!\n\n'
            '🎉 Вы приглашены на Zoom-встречу с оргкомитетом для новичков, '
            'где познакомитесь с организаторами.\n\n'
            'Для вашего удобства вы можете выбрать любой день встречи, '
            'но важно попасть на неё в течение 6 рабочих дней.'
        ),
        'greeting_organization': (
            '✡️ Шалом! Ваша организация со своим народом!\n\n'
            '🎉 Ваша команда приглашена на Zoom-встречу с оргкомитетом '
            'для новых партнёров и представителей общин.\n\n'
            'Для вашего удобства можно выбрать любой день встречи '
            'в течение 6 рабочих дней.'
        ),
        
        # Date selection
        'choose_date': '📅 Выберите удобную дату для Zoom-встречи:',
        'meeting_scheduled': '✅ Отлично! Встреча назначена на {date}',
        
        # Days of week
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        
        # Certificate
        'certificate_caption': (
            '🎫 Ваш номер сертификата участника: №{cert_number}\n'
            '📲 QR-код для активации сертификата\n\n'
            '⚠️ Для активации сертификата необходимо присутствовать на Zoom-встрече.\n'
            'После активации можно выбрать форму участия в саммите.'
        ),
        
        # Info menu
        'info_prompt': 'Чтобы получить ключевую информацию, нажмите одну из кнопок:',
        'btn_types': '🔹 Виды участия',
        'btn_summit': '🔹 О саммите',
        'btn_finish': '✅ Завершить',
        
        # Info texts
        'info_types': (
            '📋 *Виды участия в саммите*\n\n'
            '1️⃣ *Онлайн-участие (частное лицо)*\n'
            '   • Доступ ко всем онлайн-трансляциям\n'
            '   • Участие в общих чатах\n'
            '   • Сертификат участника\n\n'
            '2️⃣ *Офлайн-участие (частное лицо)*\n'
            '   • Личное присутствие на мероприятии\n'
            '   • Все преимущества онлайн-участия\n'
            '   • Networking с другими участниками\n'
            '   • Памятные подарки\n\n'
            '3️⃣ *Организационное участие*\n'
            '   • Представление вашей общины/организации\n'
            '   • Возможность выступления\n'
            '   • Партнёрские материалы\n'
            '   • Особые условия для команды\n\n'
            '💡 Окончательный выбор формы участия можно будет сделать '
            'после Zoom-встречи с оргкомитетом.'
        ),
        'info_summit': (
            '🌟 *О саммите*\n\n'
            'Саммит — это уникальное мероприятие, объединяющее представителей '
            'еврейских общин, организаций и всех, кто связан со своим народом.\n\n'
            '*Цели саммита:*\n'
            '• Укрепление связей между общинами\n'
            '• Обмен опытом и лучшими практиками\n'
            '• Обсуждение актуальных вопросов\n'
            '• Создание новых партнёрств\n'
            '• Культурное обогащение\n\n'
            '*Почему это важно для вас?*\n'
            '• Возможность найти единомышленников\n'
            '• Доступ к уникальной информации и ресурсам\n'
            '• Укрепление еврейской идентичности\n'
            '• Вклад в развитие общины\n\n'
            '📅 Саммит проводится ежегодно и собирает сотни участников '
            'со всего мира.'
        ),
        
        # Completion
        'registration_complete': (
            '✅ Регистрация завершена!\n\n'
            'Мы отправим вам напоминание о Zoom-встрече за день до мероприятия.\n\n'
            'Используйте команду /menu для доступа к информации в любое время.\n\n'
            'До встречи! 🕊️'
        ),
        
        # Menu command
        'not_registered': 'Вы еще не зарегистрированы. Используйте команду /start для регистрации.',
        'menu_title': '📱 Меню участника саммита:',
        'btn_my_certificate': '📜 Мой сертификат',
        'certificate_info': (
            '🎫 Ваш номер сертификата: №{cert_number}\n'
            '📅 Дата Zoom-встречи: {date}\n'
            '⚠️ Для активации сертификата необходимо присутствовать на встрече.'
        ),
        
        # Cancel
        'registration_cancelled': 'Регистрация отменена. Используйте /start для начала регистрации.',
        
        # Language
        'btn_language': '🌍 Change Language / Сменить язык',
        'choose_language': '🌍 Выберите язык / Choose language / בחר שפה:',
        'language_changed': '✅ Язык изменён на русский'
    },
    
    'en': {
        # Welcome and main messages
        'welcome': '🕊️ Welcome to the Summit registration!\n\nPlease choose who you are:',
        'already_registered': '✡️ Shalom, {name}!\n\nYou are already registered.\n📜 Your certificate number: №{cert_number}\n\nUse /menu to access information.',
        'select_option': '🙏 Please select one of the options to continue:',
        
        # Participant types
        'btn_individual': '🔘 I\'m with my people',
        'btn_organization': '🔘 Our organization is with our people',
        
        # Greetings after type selection
        'greeting_individual': (
            '✡️ Shalom! Congratulations — you\'re with your people!\n\n'
            '🎉 You are invited to a Zoom meeting with the organizing committee for newcomers, '
            'where you will meet the organizers.\n\n'
            'For your convenience, you can choose any meeting day, '
            'but it\'s important to attend within 6 business days.'
        ),
        'greeting_organization': (
            '✡️ Shalom! Your organization is with your people!\n\n'
            '🎉 Your team is invited to a Zoom meeting with the organizing committee '
            'for new partners and community representatives.\n\n'
            'For your convenience, you can choose any meeting day '
            'within 6 business days.'
        ),
        
        # Date selection
        'choose_date': '📅 Choose a convenient date for the Zoom meeting:',
        'meeting_scheduled': '✅ Excellent! Meeting scheduled for {date}',
        
        # Days of week
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        
        # Certificate
        'certificate_caption': (
            '🎫 Your participant certificate number: №{cert_number}\n'
            '📲 QR code for certificate activation\n\n'
            '⚠️ To activate the certificate, you must attend the Zoom meeting.\n'
            'After activation, you can choose your participation format in the summit.'
        ),
        
        # Info menu
        'info_prompt': 'To get key information, press one of the buttons:',
        'btn_types': '🔹 Types of Participation',
        'btn_summit': '🔹 About the Summit',
        'btn_finish': '✅ Finish',
        
        # Info texts
        'info_types': (
            '📋 *Types of Summit Participation*\n\n'
            '1️⃣ *Online Participation (Individual)*\n'
            '   • Access to all online broadcasts\n'
            '   • Participation in general chats\n'
            '   • Participant certificate\n\n'
            '2️⃣ *Offline Participation (Individual)*\n'
            '   • Personal attendance at the event\n'
            '   • All online participation benefits\n'
            '   • Networking with other participants\n'
            '   • Commemorative gifts\n\n'
            '3️⃣ *Organizational Participation*\n'
            '   • Representation of your community/organization\n'
            '   • Speaking opportunities\n'
            '   • Partnership materials\n'
            '   • Special conditions for your team\n\n'
            '💡 The final choice of participation format can be made '
            'after the Zoom meeting with the organizing committee.'
        ),
        'info_summit': (
            '🌟 *About the Summit*\n\n'
            'The Summit is a unique event that brings together representatives of '
            'Jewish communities, organizations, and all who are connected with their people.\n\n'
            '*Summit Goals:*\n'
            '• Strengthening ties between communities\n'
            '• Sharing experiences and best practices\n'
            '• Discussing current issues\n'
            '• Creating new partnerships\n'
            '• Cultural enrichment\n\n'
            '*Why is this important for you?*\n'
            '• Opportunity to find like-minded people\n'
            '• Access to unique information and resources\n'
            '• Strengthening Jewish identity\n'
            '• Contributing to community development\n\n'
            '📅 The Summit is held annually and brings together hundreds of participants '
            'from around the world.'
        ),
        
        # Completion
        'registration_complete': (
            '✅ Registration complete!\n\n'
            'We will send you a reminder about the Zoom meeting one day before the event.\n\n'
            'Use the /menu command to access information at any time.\n\n'
            'See you soon! 🕊️'
        ),
        
        # Menu command
        'not_registered': 'You are not registered yet. Use /start to register.',
        'menu_title': '📱 Summit Participant Menu:',
        'btn_my_certificate': '📜 My Certificate',
        'certificate_info': (
            '🎫 Your certificate number: №{cert_number}\n'
            '📅 Zoom meeting date: {date}\n'
            '⚠️ To activate the certificate, you must attend the meeting.'
        ),
        
        # Cancel
        'registration_cancelled': 'Registration cancelled. Use /start to begin registration.',
        
        # Language
        'btn_language': '🌍 Change Language / Сменить язык',
        'choose_language': '🌍 Choose language / Выберите язык / בחר שפה:',
        'language_changed': '✅ Language changed to English'
    },
    
    'he': {
        # Welcome and main messages
        'welcome': '🕊️ ברוכים הבאים לרישום לפסגה!\n\nאנא בחר מי אתה:',
        'already_registered': '✡️ שלום, {name}!\n\nאתה כבר רשום.\n📜 מספר התעודה שלך: №{cert_number}\n\nהשתמש ב-/menu לגישה למידע.',
        'select_option': '🙏 אנא בחר באחת מהאפשרויות כדי להמשיך:',
        
        # Participant types
        'btn_individual': '🔘 אני עם העם שלי',
        'btn_organization': '🔘 הארגון שלנו עם העם שלנו',
        
        # Greetings after type selection
        'greeting_individual': (
            '✡️ שלום! ברכות - אתה עם העם שלך!\n\n'
            '🎉 אתה מוזמן לפגישת Zoom עם הוועדה המארגנת למצטרפים חדשים, '
            'שם תכיר את המארגנים.\n\n'
            'לנוחותך, תוכל לבחור כל יום פגישה, '
            'אך חשוב להשתתף תוך 6 ימי עבודה.'
        ),
        'greeting_organization': (
            '✡️ שלום! הארגון שלך עם העם שלך!\n\n'
            '🎉 הצוות שלך מוזמן לפגישת Zoom עם הוועדה המארגנת '
            'לשותפים חדשים ונציגי קהילה.\n\n'
            'לנוחותך, תוכל לבחור כל יום פגישה '
            'תוך 6 ימי עבודה.'
        ),
        
        # Date selection
        'choose_date': '📅 בחר תאריך נוח לפגישת Zoom:',
        'meeting_scheduled': '✅ מצוין! הפגישה נקבעה ל-{date}',
        
        # Days of week
        'monday': 'יום שני',
        'tuesday': 'יום שלישי',
        'wednesday': 'יום רביעי',
        'thursday': 'יום חמישי',
        'friday': 'יום שישי',
        
        # Certificate
        'certificate_caption': (
            '🎫 מספר תעודת המשתתף שלך: №{cert_number}\n'
            '📲 קוד QR להפעלת התעודה\n\n'
            '⚠️ להפעלת התעודה, עליך להשתתף בפגישת Zoom.\n'
            'לאחר ההפעלה, תוכל לבחור את פורמט ההשתתפות שלך בפסגה.'
        ),
        
        # Info menu
        'info_prompt': 'כדי לקבל מידע מרכזי, לחץ על אחד הכפתורים:',
        'btn_types': '🔹 סוגי השתתפות',
        'btn_summit': '🔹 אודות הפסגה',
        'btn_finish': '✅ סיום',
        
        # Info texts
        'info_types': (
            '📋 *סוגי השתתפות בפסגה*\n\n'
            '1️⃣ *השתתפות מקוונת (פרטית)*\n'
            '   • גישה לכל השידורים המקוונים\n'
            '   • השתתפות בצ\'אטים כלליים\n'
            '   • תעודת משתתף\n\n'
            '2️⃣ *השתתפות במקום (פרטית)*\n'
            '   • נוכחות אישית באירוע\n'
            '   • כל יתרונות ההשתתפות המקוונת\n'
            '   • נטוורקינג עם משתתפים אחרים\n'
            '   • מתנות זיכרון\n\n'
            '3️⃣ *השתתפות ארגונית*\n'
            '   • ייצוג הקהילה/ארגון שלך\n'
            '   • הזדמנויות לדבר\n'
            '   • חומרי שותפות\n'
            '   • תנאים מיוחדים לצוות שלך\n\n'
            '💡 הבחירה הסופית של פורמט ההשתתפות ניתן לבצע '
            'לאחר פגישת Zoom עם הוועדה המארגנת.'
        ),
        'info_summit': (
            '🌟 *אודות הפסגה*\n\n'
            'הפסגה היא אירוע ייחודי המאחד נציגים של '
            'קהילות יהודיות, ארגונים וכל מי שקשור לעם שלו.\n\n'
            '*מטרות הפסגה:*\n'
            '• חיזוק הקשרים בין קהילות\n'
            '• שיתוף ניסיון ושיטות עבודה מומלצות\n'
            '• דיון בנושאים עכשוויים\n'
            '• יצירת שותפויות חדשות\n'
            '• העשרה תרבותית\n\n'
            '*למה זה חשוב לך?*\n'
            '• הזדמנות למצוא אנשים בעלי דעות דומות\n'
            '• גישה למידע ומשאבים ייחודיים\n'
            '• חיזוק הזהות היהודית\n'
            '• תרומה לפיתוח הקהילה\n\n'
            '📅 הפסגה מתקיימת מדי שנה ומאחדת מאות משתתפים '
            'מרחבי העולם.'
        ),
        
        # Completion
        'registration_complete': (
            '✅ הרישום הושלם!\n\n'
            'נשלח לך תזכורת על פגישת Zoom יום אחד לפני האירוע.\n\n'
            'השתמש בפקודה /menu לגישה למידע בכל עת.\n\n'
            'נתראה בקרוב! 🕊️'
        ),
        
        # Menu command
        'not_registered': 'אתה עדיין לא רשום. השתמש ב-/start כדי להירשם.',
        'menu_title': '📱 תפריט משתתף הפסגה:',
        'btn_my_certificate': '📜 התעודה שלי',
        'certificate_info': (
            '🎫 מספר התעודה שלך: №{cert_number}\n'
            '📅 תאריך פגישת Zoom: {date}\n'
            '⚠️ להפעלת התעודה, עליך להשתתף בפגישה.'
        ),
        
        # Cancel
        'registration_cancelled': 'הרישום בוטל. השתמש ב-/start כדי להתחיל רישום.',
        
        # Language
        'btn_language': '🌍 Change Language / Сменить язык',
        'choose_language': '🌍 בחר שפה / Choose language / Выберите язык:',
        'language_changed': '✅ השפה שונתה לעברית'
    }
}

# Language names for display
LANGUAGE_NAMES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English',
    'he': '🇮🇱 עברית'
}

# Day of week mapping
WEEKDAYS = {
    0: {'ru': 'Понедельник', 'en': 'Monday', 'he': 'יום שני'},
    1: {'ru': 'Вторник', 'en': 'Tuesday', 'he': 'יום שלישי'},
    2: {'ru': 'Среда', 'en': 'Wednesday', 'he': 'יום רביעי'},
    3: {'ru': 'Четверг', 'en': 'Thursday', 'he': 'יום חמישי'},
    4: {'ru': 'Пятница', 'en': 'Friday', 'he': 'יום שישי'}
}

def get_text(language: str, key: str, **kwargs) -> str:
    """
    Get text in specified language
    
    Args:
        language: Language code (ru, en, he)
        key: Text key
        **kwargs: Format parameters
    
    Returns:
        Formatted text in specified language
    """
    if language not in TEXTS:
        language = 'ru'  # Default to Russian
    
    text = TEXTS[language].get(key, TEXTS['ru'].get(key, f'[Missing: {key}]'))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text

def get_weekday(weekday_num: int, language: str) -> str:
    """Get weekday name in specified language"""
    if language not in ['ru', 'en', 'he']:
        language = 'ru'
    return WEEKDAYS.get(weekday_num, {}).get(language, '')

