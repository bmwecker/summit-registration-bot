const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const { Pool } = require('pg');
require('dotenv').config();

// Подключение к PostgreSQL
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.DATABASE_URL.includes('localhost') ? false : { rejectUnauthorized: false }
});

// Константы
const MAX_PARTICIPANTS_PER_DATE = 290;

// Видео для разных языков (Dropbox с dl=1 для прямого скачивания)
const WELCOME_VIDEOS = {
    ru: 'https://www.dropbox.com/scl/fi/044kdmis462chkfy7kpcn/4.mp4?rlkey=wyap66tnu3j3i8yuvp8n7wtid&st=84gh8wbh&dl=1',
    he: 'https://www.dropbox.com/scl/fi/044kdmis462chkfy7kpcn/4.mp4?rlkey=wyap66tnu3j3i8yuvp8n7wtid&st=lrigyksz&dl=1',
    en: 'https://www.dropbox.com/scl/fi/ma2ha4gu39l95o59519u8/.mp4?rlkey=594fye1i0p8rabbzmm6mcz5yt&st=dincgr4p&dl=1'
};

// Ссылки на страницы "Система лидерства Торы" для каждого языка
const TORAH_LEADERSHIP_PAGES = {
    ru: 'https://liderstvo-tory-diqyh3c.gamma.site/',
    en: 'https://torovoe-liderstvo-wbc7m7i.gamma.site/',
    he: 'https://tora-i-tsifrovaya-epokha-h98jv9r.gamma.site/'
};

// Тексты ТОЧНО как в Telegram боте (из languages.py)
const TEXTS = {
    ru: {
        welcome: '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1️⃣ Русский 🇷🇺\n2️⃣ English 🇬🇧\n3️⃣ עברית 🇮🇱',
        greeting: '✡️ Поздравляем — вы со своим народом!\nШалом! Меня зовут Шломо\n\n🎉 Вы приглашены на Zoom-встречу с оргкомитетом для знакомства с организаторами. Также на ней, вы сможете выбрать ту миссию, которая Вам по душе!\n\nКогда Вы хотите присоединиться к ZOOM встрече? Сегодня, завтра или послезавтра?',
        choose_date: '📅 Выберите удобную дату для Zoom-встречи:',
        date_full: '❌ К сожалению, на эту дату все места заняты. Пожалуйста, выберите другую дату.',
        meeting_confirmed: 'Отлично! Мы будем очень рады Вас видеть на нашей первой встрече!',
        id_and_code: '🎫 Ваш ID: №{participant_id}\n📲 Уникальный код для активации ID: {activation_code}\n\n⚠️ Для активации Вашего ID необходимо присутствовать на Zoom-встрече.\nПосле активации можно выбрать форму участия в саммите.',
        main_menu: '📱 Главное меню:\n\n1️⃣ Напомнить номер ID\n2️⃣ Напомнить код активации\n3️⃣ Напомнить дату встречи\n4️⃣ Перенести встречу\n5️⃣ Как активировать ID?\n6️⃣ Изменить язык\n7️⃣ Дополнительные материалы\n\n_Отправьте номер (1-7) или команду (MENU, HELP)_',
        torah_leadership_intro: '🌐 **Система лидерства Торы в цифровую эпоху**\n\nПознакомьтесь с моделью управления, данной Б-гом через Итро Моше Рабейну:',
        materials_menu: '📚 **Дополнительные материалы:**\n\nОтправьте номер:\n1️⃣ Видео\n2️⃣ Система лидерства Торы\n3️⃣ Вернуться в меню',
        your_id: '📜 Ваш ID: №{participant_id}',
        your_code: '🔑 Ваш код активации: {activation_code}',
        your_date: '📅 Ваша дата Zoom-встречи: {zoom_date}',
        how_to_activate: '❓ **Как активировать ID?**\n\nВ день ZOOM встречи, Вы получите ссылку на онлайн встречу, и точное время её проведения, на которой Вы должны будете отправить свой уникальный код в общий чат.\n\nПо окончанию ZOOM встречи Ваш ID будет активирован.',
        help: '📖 Справка\n\nДоступные команды:\n• START - начать регистрацию\n• MENU - главное меню\n• 1-6 - выбрать пункт меню\n• HELP - эта справка',
        today: 'Сегодня',
        tomorrow: 'Завтра',
        day_after_tomorrow: 'Послезавтра'
    },
    en: {
        welcome: '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1️⃣ Русский 🇷🇺\n2️⃣ English 🇬🇧\n3️⃣ עברית 🇮🇱',
        greeting: '✡️ Congratulations — you are with your people!\nShalom! My name is Shlomo\n\n🎉 You are invited to a Zoom meeting with the organizing committee to meet the organizers. You will also be able to choose the mission that suits you!\n\nWhen would you like to join the ZOOM meeting? Today, tomorrow, or the day after tomorrow?',
        choose_date: '📅 Choose a convenient date for the Zoom meeting:',
        date_full: '❌ Unfortunately, all places for this date are taken. Please choose another date.',
        meeting_confirmed: 'Great! We will be very happy to see you at our first meeting!',
        id_and_code: '🎫 Your ID: №{participant_id}\n📲 Unique activation code: {activation_code}\n\n⚠️ You must attend the Zoom meeting to activate your ID.\nAfter activation, you can choose your form of participation in the summit.',
        main_menu: '📱 Main menu:\n\n1️⃣ Remind ID number\n2️⃣ Remind activation code\n3️⃣ Remind meeting date\n4️⃣ Reschedule meeting\n5️⃣ How to activate ID?\n6️⃣ Change language\n7️⃣ Additional Materials\n\n_Send number (1-7) or command (MENU, HELP)_',
        torah_leadership_intro: '🌐 **Torah Leadership System in the Digital Age**\n\nDiscover the management model given by G-d through Yitro to Moshe Rabbeinu:',
        materials_menu: '📚 **Additional Materials:**\n\nSend number:\n1️⃣ Video\n2️⃣ Torah Leadership System\n3️⃣ Back to menu',
        your_id: '📜 Your ID: №{participant_id}',
        your_code: '🔑 Your activation code: {activation_code}',
        your_date: '📅 Your Zoom meeting date: {zoom_date}',
        how_to_activate: '❓ **How to activate ID?**\n\nOn the day of the ZOOM meeting, you will receive a link to the online meeting and the exact time it will take place. You must send your unique code to the general chat.\n\nAfter the ZOOM meeting is over, your ID will be activated.',
        help: '📖 Help\n\nAvailable commands:\n• START - start registration\n• MENU - main menu\n• 1-6 - select menu item\n• HELP - this help',
        today: 'Today',
        tomorrow: 'Tomorrow',
        day_after_tomorrow: 'Day after tomorrow'
    },
    he: {
        welcome: '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1️⃣ Русский 🇷🇺\n2️⃣ English 🇬🇧\n3️⃣ עברית 🇮🇱',
        greeting: '✡️ !ברוכים הבאים — אתם עם העם שלכם\n!שלום! שמי שלמה\n\n🎉 אתם מוזמנים לפגישת Zoom עם הוועדה המארגנת כדי להכיר את המארגנים. תוכלו גם לבחור את המשימה המתאימה לכם!\n\nמתי תרצו להצטרף לפגישת ZOOM? היום, מחר או מחרתיים?',
        choose_date: '📅 :בחרו תאריך נוח לפגישת Zoom',
        date_full: '❌ למרבה הצער, כל המקומות לתאריך זה תפוסים. אנא בחרו תאריך אחר.',
        meeting_confirmed: '!מצוין! נשמח מאוד לראותכם בפגישה הראשונה שלנו',
        id_and_code: '🎫 ה-ID שלך: №{participant_id}\n📲 :קוד הפעלה ייחודי {activation_code}\n\n⚠️ עליך להשתתף בפגישת Zoom כדי להפעיל את ה-ID שלך.\n.לאחר ההפעלה, תוכל לבחור את צורת ההשתתפות שלך בפסגה',
        main_menu: '📱 :תפריט ראשי\n\n1️⃣ הזכר מספר ID\n2️⃣ הזכר קוד הפעלה\n3️⃣ הזכר תאריך פגישה\n4️⃣ קבע מחדש פגישה\n5️⃣ ?כיצד להפעיל ID\n6️⃣ שנה שפה\n7️⃣ חומרים נוספים\n\n_(MENU ,HELP) שלח מספר (1-7) או פקודה_',
        torah_leadership_intro: '🌐 **מערכת המנהיגות של התורה בעידן הדיגיטלי**\n\nהכר את מודל הניהול שניתן על ידי הקב"ה דרך יתרו למשה רבינו:',
        materials_menu: '📚 **חומרים נוספים:**\n\n:שלח מספר\n1️⃣ וידאו\n2️⃣ מערכת המנהיגות של התורה\n3️⃣ חזור לתפריט',
        your_id: '📜 ה-ID שלך: №{participant_id}',
        your_code: '🔑 קוד ההפעלה שלך: {activation_code}',
        your_date: '📅 תאריך פגישת Zoom שלך: {zoom_date}',
        how_to_activate: '❓ **?כיצד להפעיל ID**\n\nביום פגישת ZOOM, תקבל קישור לפגישה המקוונת והשעה המדויקת שבה היא תתקיים. עליך לשלוח את הקוד הייחודי שלך לצ\'אט הכללי.\n\n.בתום פגישת ZOOM, ה-ID שלך יופעל',
        help: '📖 עזרה\n\n:פקודות זמינות\n• START - התחל רישום\n• MENU - תפריט ראשי\n• 1-6 - בחר פריט תפריט\n• HELP - עזרה זו',
        today: 'היום',
        tomorrow: 'מחר',
        day_after_tomorrow: 'מחרתיים'
    }
};

// Названия дней недели
const WEEKDAY_NAMES = {
    ru: ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
    en: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    he: ['יום שני', 'יום שלישי', 'יום רביעי', 'יום חמישי', 'יום שישי', 'שבת', 'יום ראשון']
};

// Состояние пользователей (в памяти)
const userStates = new Map();

// Генерация telegram_id из номера WhatsApp
function whatsappToTelegramId(phoneNumber) {
    const cleanNumber = phoneNumber.replace(/\D/g, '');
    return -2000000000000000 + parseInt(cleanNumber.slice(-14));
}

// Получение следующих трёх дней (пропуск пятницы и субботы)
function getNextThreeDays() {
    const days = [];
    let current = new Date();
    
    while (days.length < 3) {
        const dayOfWeek = current.getDay();
        // Пропускаем пятницу (5) и субботу (6)
        if (dayOfWeek !== 5 && dayOfWeek !== 6) {
            days.push(new Date(current));
        }
        current.setDate(current.getDate() + 1);
    }
    
    return days;
}

// Форматирование даты для отображения
function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
}

// Форматирование даты для базы данных (YYYY-MM-DD)
function formatDateForDB(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Получение дня недели
function getWeekdayName(date, language) {
    const dayIndex = date.getDay();
    // В JavaScript воскресенье = 0, понедельник = 1, ... суббота = 6
    // Нужно сдвинуть, чтобы понедельник = 0
    const adjustedIndex = dayIndex === 0 ? 6 : dayIndex - 1;
    return WEEKDAY_NAMES[language][adjustedIndex];
}

// Получение количества участников на дату
async function getParticipantsCount(date) {
    try {
        const result = await pool.query(
            'SELECT COUNT(*) FROM participants WHERE zoom_date = $1',
            [date]
        );
        return parseInt(result.rows[0].count);
    } catch (error) {
        console.error('[WHATSAPP] Error getting participants count:', error);
        return 0;
    }
}

// Создание пользователя в базе
async function createUser(telegramId, username, firstName, language, phoneNumber) {
    try {
        const participantId = await getNextParticipantId();
        const activationCode = Math.floor(100000 + Math.random() * 900000).toString();
        
        await pool.query(
            `INSERT INTO participants 
            (telegram_id, username, first_name, participant_type, language, participant_id, activation_code, email, is_activated, registration_date) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
            [telegramId, username, firstName, 'whatsapp_participant', language, participantId, activationCode, phoneNumber, false, new Date()]
        );
        
        console.log(`[WHATSAPP] User created: ID=${participantId}, Code=${activationCode}`);
        return { participantId, activationCode };
    } catch (error) {
        console.error('[WHATSAPP] Error creating user:', error);
        return null;
    }
}

// Получение следующего participant_id
async function getNextParticipantId() {
    try {
        const result = await pool.query(
            'SELECT MAX(participant_id) as max_id FROM participants'
        );
        const maxId = result.rows[0].max_id || 12000;
        return maxId + 1;
    } catch (error) {
        console.error('[WHATSAPP] Error getting next participant_id:', error);
        return 12000 + Math.floor(Math.random() * 1000);
    }
}

// Получение пользователя
async function getUser(telegramId) {
    try {
        const result = await pool.query(
            'SELECT * FROM participants WHERE telegram_id = $1',
            [telegramId]
        );
        return result.rows[0] || null;
    } catch (error) {
        console.error('[WHATSAPP] Error getting user:', error);
        return null;
    }
}

// Обновление языка
async function updateLanguage(telegramId, language) {
    try {
        await pool.query(
            'UPDATE participants SET language = $1 WHERE telegram_id = $2',
            [language, telegramId]
        );
    } catch (error) {
        console.error('[WHATSAPP] Error updating language:', error);
    }
}

// Обновление даты
async function updateZoomDate(telegramId, date) {
    try {
        await pool.query(
            'UPDATE participants SET zoom_date = $1 WHERE telegram_id = $2',
            [date, telegramId]
        );
    } catch (error) {
        console.error('[WHATSAPP] Error updating zoom date:', error);
    }
}

// Отправка списка дат
function getDatesMessage(language) {
    const dates = getNextThreeDays();
    const texts = TEXTS[language];
    const relative = [texts.today, texts.tomorrow, texts.day_after_tomorrow];
    const emojis = ['1️⃣', '2️⃣', '3️⃣'];
    
    let message = texts.greeting + '\n\n' + texts.choose_date + '\n\n';
    
    for (let i = 0; i < dates.length; i++) {
        const weekday = getWeekdayName(dates[i], language);
        const formatted = formatDate(dates[i]);
        message += `${emojis[i]} ${relative[i]} (${weekday}) - ${formatted}\n`;
    }
    
    return message;
}

// Инициализация клиента
function initWhatsAppBot(qrCallback, readyCallback) {
    const client = new Client({
        authStrategy: new LocalAuth({ dataPath: './whatsapp_session' }),
        puppeteer: {
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        }
    });

    client.on('qr', qr => {
        console.log('[WHATSAPP] QR code received');
        if (qrCallback) qrCallback(qr);
    });

    client.on('ready', () => {
        console.log('[WHATSAPP] Bot is ready!');
        if (readyCallback) readyCallback();
    });

    client.on('authenticated', () => {
        console.log('[WHATSAPP] Authenticated successfully');
    });

    client.on('auth_failure', msg => {
        console.error('[WHATSAPP] Authentication failure:', msg);
    });

    client.on('disconnected', reason => {
        console.log('[WHATSAPP] Client disconnected:', reason);
    });

    client.on('message', async msg => {
        try {
            const phoneNumber = msg.from;
            const body = msg.body.trim();
            
            if (!body) return; // Игнорируем пустые сообщения
            
            const telegramId = whatsappToTelegramId(phoneNumber);
            let user = await getUser(telegramId);
            let state = userStates.get(phoneNumber) || { step: 'start' };
            const bodyLower = body.toLowerCase().trim();
            
            console.log(`[WHATSAPP] From: ${phoneNumber}, Message: "${body}", State: ${state.step}, User exists: ${!!user}`);
            
            // Команда START
            if (bodyLower === 'start' || bodyLower === 'старт') {
                if (user) {
                    // Если пользователь уже есть - показываем меню
                    const texts = TEXTS[user.language || 'ru'];
                    const menuText = texts.main_menu
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code)
                        .replace('{zoom_date}', user.zoom_date ? formatDate(new Date(user.zoom_date)) : 'не выбрана');
                    await msg.reply(menuText);
                    userStates.set(phoneNumber, { step: 'registered', language: user.language });
                } else {
                    // Новый пользователь - выбор языка
                    await msg.reply(TEXTS.ru.welcome);
                    userStates.set(phoneNumber, { step: 'choosing_language' });
                }
                console.log(`[WHATSAPP] START processed`);
                return;
            }
            
            // Если пользователя нет и это НЕ START - показываем welcome
            if (!user && state.step === 'start') {
                await msg.reply(TEXTS.ru.welcome);
                userStates.set(phoneNumber, { step: 'choosing_language' });
                console.log(`[WHATSAPP] New user, showing welcome`);
                return;
            }
            
            // Выбор языка - ТОЛЬКО если state.step === 'choosing_language'
            if (state.step === 'choosing_language') {
                let language = null;
                
                if (body === '1' || bodyLower === 'ru' || bodyLower === 'russian' || bodyLower === 'русский') {
                    language = 'ru';
                } else if (body === '2' || bodyLower === 'en' || bodyLower === 'english' || bodyLower === 'английский') {
                    language = 'en';
                } else if (body === '3' || bodyLower === 'he' || bodyLower === 'hebrew' || bodyLower === 'иврит' || body.includes('עברית')) {
                    language = 'he';
                }
                
                if (language) {
                    console.log(`[WHATSAPP] Language selected: ${language}`);
                    
                    if (!user) {
                        // Создаем нового пользователя
                        const contact = await msg.getContact();
                        const firstName = contact.pushname || contact.name || phoneNumber;
                        await createUser(telegramId, phoneNumber, firstName, language, phoneNumber);
                        user = await getUser(telegramId);
                    } else {
                        await updateLanguage(telegramId, language);
                        user.language = language;
                    }
                    
                    // Отправляем список дат
                    const datesMessage = getDatesMessage(language);
                    await msg.reply(datesMessage);
                    userStates.set(phoneNumber, { step: 'choosing_date', language });
                    console.log(`[WHATSAPP] Dates sent`);
                    return;
                } else {
                    // Не распознали язык
                    await msg.reply(TEXTS.ru.help);
                    return;
                }
            }
            
            // Выбор даты - ТОЛЬКО если state.step === 'choosing_date'
            if (state.step === 'choosing_date' && ['1', '2', '3'].includes(body)) {
                const dateIndex = parseInt(body) - 1;
                const dates = getNextThreeDays();
                
                if (dateIndex >= 0 && dateIndex < dates.length) {
                    const selectedDate = formatDateForDB(dates[dateIndex]);
                    const count = await getParticipantsCount(selectedDate);
                    
                    if (count >= MAX_PARTICIPANTS_PER_DATE) {
                        const texts = TEXTS[user.language || 'ru'];
                        await msg.reply(texts.date_full);
                        const datesMessage = getDatesMessage(user.language || 'ru');
                        await msg.reply(datesMessage);
                        return;
                    }
                    
                    await updateZoomDate(telegramId, selectedDate);
                    user = await getUser(telegramId);
                    
                    const texts = TEXTS[user.language || 'ru'];
                    
                    // 1. Отправляем подтверждение
                    await msg.reply(texts.meeting_confirmed);
                    
                    // 2. Отправляем ID и код
                    const idMessage = texts.id_and_code
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code);
                    await msg.reply(idMessage);
                    
                    // 3. Отправляем видео
                    const videoUrl = WELCOME_VIDEOS[user.language] || WELCOME_VIDEOS['ru'];
                    try {
                        const media = await MessageMedia.fromUrl(videoUrl);
                        await client.sendMessage(msg.from, media);
                        console.log(`[WHATSAPP] Welcome video sent for language: ${user.language}`);
                    } catch (error) {
                        console.error(`[WHATSAPP] Failed to send video: ${error}`);
                    }
                    
                    // 4. Отправляем ссылку на страницу "Система лидерства Торы"
                    const torahPageUrl = TORAH_LEADERSHIP_PAGES[user.language] || TORAH_LEADERSHIP_PAGES['ru'];
                    const torahIntro = texts.torah_leadership_intro;
                    await msg.reply(`${torahIntro}\n\n${torahPageUrl}`);
                    
                    // Отправляем меню
                    const menuText = texts.main_menu
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code)
                        .replace('{zoom_date}', formatDate(dates[dateIndex]));
                    await msg.reply(menuText);
                    
                    userStates.set(phoneNumber, { step: 'registered', language: user.language });
                    console.log(`[WHATSAPP] Date selected: ${selectedDate}`);
                    return;
                }
            }
            
            // Обработка меню (пункты 1-6) - только для зарегистрированных
            if (user && state.step === 'registered' && ['1', '2', '3', '4', '5', '6', '7'].includes(body)) {
                const texts = TEXTS[user.language || 'ru'];
                const menuChoice = parseInt(body);
                
                if (menuChoice === 1) {
                    // Напомнить ID
                    const text = texts.your_id.replace('{participant_id}', user.participant_id);
                    await msg.reply(text);
                    console.log(`[WHATSAPP] Reminded ID`);
                    return;
                }
                
                if (menuChoice === 2) {
                    // Напомнить код активации
                    const text = texts.your_code.replace('{activation_code}', user.activation_code);
                    await msg.reply(text);
                    console.log(`[WHATSAPP] Reminded activation code`);
                    return;
                }
                
                if (menuChoice === 3) {
                    // Напомнить дату встречи
                    const dateText = user.zoom_date ? formatDate(new Date(user.zoom_date)) : 'не выбрана';
                    const text = texts.your_date.replace('{zoom_date}', dateText);
                    await msg.reply(text);
                    console.log(`[WHATSAPP] Reminded meeting date`);
                    return;
                }
                
                if (menuChoice === 4) {
                    // Перенести встречу - показать даты заново
                    const datesMessage = getDatesMessage(user.language);
                    await msg.reply(datesMessage);
                    userStates.set(phoneNumber, { step: 'choosing_date', language: user.language });
                    console.log(`[WHATSAPP] Rescheduling meeting`);
                    return;
                }
                
                if (menuChoice === 5) {
                    // Как активировать ID
                    await msg.reply(texts.how_to_activate);
                    console.log(`[WHATSAPP] Showed activation info`);
                    return;
                }
                
                if (menuChoice === 6) {
                    // Изменить язык
                    await msg.reply(TEXTS.ru.welcome);
                    userStates.set(phoneNumber, { step: 'choosing_language' });
                    console.log(`[WHATSAPP] Changing language`);
                    return;
                }
                
                if (menuChoice === 7) {
                    // Дополнительные материалы
                    await msg.reply(texts.materials_menu);
                    userStates.set(phoneNumber, { step: 'materials_menu', language: user.language });
                    console.log(`[WHATSAPP] Showing materials menu`);
                    return;
                }
            }
            
            // Обработка подменю "Дополнительные материалы"
            if (user && state.step === 'materials_menu' && ['1', '2', '3'].includes(body)) {
                const texts = TEXTS[user.language || 'ru'];
                const materialsChoice = parseInt(body);
                
                if (materialsChoice === 1) {
                    // Показать видео
                    const videoUrl = WELCOME_VIDEOS[user.language] || WELCOME_VIDEOS['ru'];
                    try {
                        const media = await MessageMedia.fromUrl(videoUrl);
                        await client.sendMessage(msg.from, media);
                        console.log(`[WHATSAPP] Sent video from materials menu`);
                    } catch (error) {
                        console.error(`[WHATSAPP] Failed to send video: ${error}`);
                    }
                    
                    // Возвращаем в главное меню
                    const menuText = sendMainMenu(user, texts);
                    await msg.reply(menuText);
                    userStates.set(phoneNumber, { step: 'registered', language: user.language });
                    return;
                }
                
                if (materialsChoice === 2) {
                    // Показать страницу Торы
                    const torahPageUrl = TORAH_LEADERSHIP_PAGES[user.language] || TORAH_LEADERSHIP_PAGES['ru'];
                    const torahIntro = texts.torah_leadership_intro;
                    await msg.reply(`${torahIntro}\n\n${torahPageUrl}`);
                    console.log(`[WHATSAPP] Sent Torah page from materials menu`);
                    
                    // Возвращаем в главное меню
                    const menuText = sendMainMenu(user, texts);
                    await msg.reply(menuText);
                    userStates.set(phoneNumber, { step: 'registered', language: user.language });
                    return;
                }
                
                if (materialsChoice === 3) {
                    // Вернуться в меню
                    const menuText = sendMainMenu(user, texts);
                    await msg.reply(menuText);
                    userStates.set(phoneNumber, { step: 'registered', language: user.language });
                    console.log(`[WHATSAPP] Back to main menu from materials`);
                    return;
                }
            }
            
            // Команда MENU
            if (bodyLower === 'menu' || bodyLower === 'меню' || bodyLower.includes('תפריט')) {
                if (user) {
                    const texts = TEXTS[user.language || 'ru'];
                    const menuText = texts.main_menu
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code)
                        .replace('{zoom_date}', user.zoom_date ? formatDate(new Date(user.zoom_date)) : 'не выбрана');
                    await msg.reply(menuText);
                } else {
                    await msg.reply(TEXTS.ru.welcome);
                    userStates.set(phoneNumber, { step: 'choosing_language' });
                }
                return;
            }
            
            // Команда HELP
            if (bodyLower === 'help' || bodyLower === 'помощь' || bodyLower.includes('עזרה')) {
                const texts = TEXTS[user ? user.language : 'ru'] || TEXTS.ru;
                await msg.reply(texts.help);
                return;
            }
            
            // Если ничего не распознали - показываем help
            const texts = TEXTS[user ? user.language : 'ru'] || TEXTS.ru;
            await msg.reply(texts.help);
            
        } catch (error) {
            console.error('[WHATSAPP] Error handling message:', error);
        }
    });

    client.initialize();
    return client;
}

module.exports = { initWhatsAppBot, pool };
