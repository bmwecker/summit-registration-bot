const { Client, LocalAuth } = require('whatsapp-web.js');
const { Pool } = require('pg');
require('dotenv').config();

// Подключение к PostgreSQL
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.DATABASE_URL.includes('localhost') ? false : { rejectUnauthorized: false }
});

// Константы
const MAX_PARTICIPANTS_PER_DATE = 290;

// Тексты ТОЧНО как в Telegram боте (из languages.py)
const TEXTS = {
    ru: {
        welcome: '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1 - Русский 🇷🇺\n2 - English 🇬🇧\n3 - עברית 🇮🇱',
        greeting: '✡️ Поздравляем — вы со своим народом!\nШалом! Меня зовут Шломо\n\n🎉 Вы приглашены на Zoom-встречу с оргкомитетом для знакомства с организаторами. Также на ней, вы сможете выбрать ту миссию, которая Вам по душе!\n\nКогда Вы хотите присоединиться к ZOOM встрече? Сегодня, завтра или послезавтра?',
        choose_date: '📅 Выберите удобную дату для Zoom-встречи:',
        date_full: '❌ К сожалению, на эту дату все места заняты. Пожалуйста, выберите другую дату.',
        meeting_confirmed: 'Отлично! Мы будем очень рады Вас видеть на нашей первой встрече!',
        id_and_code: '🎫 Ваш ID: №{participant_id}\n📲 Уникальный код для активации ID: {activation_code}\n\n⚠️ Для активации Вашего ID необходимо присутствовать на Zoom-встрече.\nПосле активации можно выбрать форму участия в саммите.',
        main_menu: '📱 Главное меню:\n\n🎫 Ваш ID: №{participant_id}\n🔑 Ваш код активации: {activation_code}\n📅 Дата встречи: {zoom_date}\n\nВы можете написать:\n• MENU - показать это меню\n• HELP - показать справку',
        help: '📖 Справка\n\nДоступные команды:\n• START - начать регистрацию\n• 1 / 2 / 3 - выбрать язык или дату\n• MENU - главное меню\n• HELP - эта справка',
        today: 'Сегодня',
        tomorrow: 'Завтра',
        day_after_tomorrow: 'Послезавтра'
    },
    en: {
        welcome: '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1 - Русский 🇷🇺\n2 - English 🇬🇧\n3 - עברית 🇮🇱',
        greeting: '✡️ Congratulations — you are with your people!\nShalom! My name is Shlomo\n\n🎉 You are invited to a Zoom meeting with the organizing committee to meet the organizers. You will also be able to choose the mission that suits you!\n\nWhen would you like to join the ZOOM meeting? Today, tomorrow, or the day after tomorrow?',
        choose_date: '📅 Choose a convenient date for the Zoom meeting:',
        date_full: '❌ Unfortunately, all places for this date are taken. Please choose another date.',
        meeting_confirmed: 'Great! We will be very happy to see you at our first meeting!',
        id_and_code: '🎫 Your ID: №{participant_id}\n📲 Unique activation code: {activation_code}\n\n⚠️ You must attend the Zoom meeting to activate your ID.\nAfter activation, you can choose your form of participation in the summit.',
        main_menu: '📱 Main menu:\n\n🎫 Your ID: №{participant_id}\n🔑 Your activation code: {activation_code}\n📅 Meeting date: {zoom_date}\n\nYou can write:\n• MENU - show this menu\n• HELP - show help',
        help: '📖 Help\n\nAvailable commands:\n• START - start registration\n• 1 / 2 / 3 - choose language or date\n• MENU - main menu\n• HELP - this help',
        today: 'Today',
        tomorrow: 'Tomorrow',
        day_after_tomorrow: 'Day after tomorrow'
    },
    he: {
        welcome: '🕊️ Добро пожаловать! Welcome! ברוכים הבאים!\n\nПожалуйста, выберите язык / Please choose language / בחר שפה:\n\n1 - Русский 🇷🇺\n2 - English 🇬🇧\n3 - עברית 🇮🇱',
        greeting: '✡️ !ברוכים הבאים — אתם עם העם שלכם\n!שלום! שמי שלמה\n\n🎉 אתם מוזמנים לפגישת Zoom עם הוועדה המארגנת כדי להכיר את המארגנים. תוכלו גם לבחור את המשימה המתאימה לכם!\n\nמתי תרצו להצטרף לפגישת ZOOM? היום, מחר או מחרתיים?',
        choose_date: '📅 :בחרו תאריך נוח לפגישת Zoom',
        date_full: '❌ למרבה הצער, כל המקומות לתאריך זה תפוסים. אנא בחרו תאריך אחר.',
        meeting_confirmed: '!מצוין! נשמח מאוד לראותכם בפגישה הראשונה שלנו',
        id_and_code: '🎫 ה-ID שלך: №{participant_id}\n📲 :קוד הפעלה ייחודי {activation_code}\n\n⚠️ עליך להשתתף בפגישת Zoom כדי להפעיל את ה-ID שלך.\n.לאחר ההפעלה, תוכל לבחור את צורת ההשתתפות שלך בפסגה',
        main_menu: '📱 :תפריט ראשי\n\n🎫 ה-ID שלך: №{participant_id}\n🔑 קוד ההפעלה שלך: {activation_code}\n📅 תאריך הפגישה: {zoom_date}\n\n:אתה יכול לכתוב\n• MENU - הצג תפריט זה\n• HELP - הצג עזרה',
        help: '📖 עזרה\n\n:פקודות זמינות\n• START - התחל רישום\n• 1 / 2 / 3 - בחר שפה או תאריך\n• MENU - תפריט ראשי\n• HELP - עזרה זו',
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
    
    let message = texts.greeting + '\n\n' + texts.choose_date + '\n\n';
    
    for (let i = 0; i < dates.length; i++) {
        const weekday = getWeekdayName(dates[i], language);
        const formatted = formatDate(dates[i]);
        message += `${i + 1} - ${relative[i]} (${weekday}) - ${formatted}\n`;
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
                    
                    // Отправляем ID и код
                    const idMessage = texts.id_and_code
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code);
                    await msg.reply(idMessage);
                    
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
