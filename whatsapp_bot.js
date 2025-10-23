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

// Тексты на разных языках
const TEXTS = {
    ru: {
        welcome: '🕊️ Добро пожаловать в Aleph Bet Foresight Summit!\n\nВыберите язык / Choose language / בחר שפה:\n\n1️⃣ Русский (RU)\n2️⃣ English (EN)\n3️⃣ עברית (HE)',
        greeting: '✡️ Добро пожаловать!\nПривет! Меня зовут Шломо\n\n🎉 Вы приглашены на Zoom-встречу с организационным комитетом, чтобы познакомиться с организаторами. А также Вы сможете выбрать наиболее подходящую для Вас задачу!\n\nКогда Вы хотели бы присоединиться к встрече в ZOOM? Сегодня, завтра или послезавтра?\n\n📅 Выберите удобную дату для встречи в Zoom:',
        date_full: '⚠️ К сожалению, на эту дату все места заняты. Пожалуйста, выберите другую дату.',
        confirmation: '🎫 Ваш ID: №{participant_id}\n📲 Уникальный код активации: {activation_code}\n\n⚠️ Для активации вашего ID необходимо принять участие во встрече в Zoom в выбранную вами дату: {date}\n\n📞 Встреча состоится в 19:00 по московскому времени\n🔗 Ссылка на Zoom будет отправлена вам в день встречи\n\n💡 Сохраните этот код! Он понадобится для активации вашего профиля на сайте.',
        menu: '📱 Главное меню\n\n🎫 Ваш ID: №{participant_id}\n🔑 Ваш код активации: {activation_code}\n📅 Дата встречи: {date}\n\nДля изменения данных или получения инструкций - напишите нам!',
        help: '📖 Помощь\n\nДоступные команды:\n• START - начать регистрацию\n• RU / EN / HE - выбрать язык\n• 1 / 2 / 3 - выбрать дату\n• MENU - главное меню\n• HELP - эта справка'
    },
    en: {
        welcome: '🕊️ Welcome to Aleph Bet Foresight Summit!\n\nChoose language / Выберите язык / בחר שפה:\n\n1️⃣ Русский (RU)\n2️⃣ English (EN)\n3️⃣ עברית (HE)',
        greeting: '✡️ Greetings!\nHello! My name is Shlomo\n\n🎉 You are invited to a Zoom meeting with the organizing committee to get to know the organizers. You will also be able to choose the task that suits you best!\n\nWhen would you like to join the ZOOM meeting? Today, tomorrow or the day after tomorrow?\n\n📅 Choose a convenient date for the Zoom meeting:',
        date_full: '⚠️ Unfortunately, all places for this date are taken. Please choose another date.',
        confirmation: '🎫 Your ID: №{participant_id}\n📲 Unique activation code: {activation_code}\n\n⚠️ To activate your ID, you must participate in the Zoom meeting on your chosen date: {date}\n\n📞 The meeting will take place at 19:00 Moscow time\n🔗 The Zoom link will be sent to you on the day of the meeting\n\n💡 Save this code! You will need it to activate your profile on the website.',
        menu: '📱 Main menu\n\n🎫 Your ID: №{participant_id}\n🔑 Your activation code: {activation_code}\n📅 Meeting date: {date}\n\nTo change data or get instructions - write to us!',
        help: '📖 Help\n\nAvailable commands:\n• START - start registration\n• RU / EN / HE - choose language\n• 1 / 2 / 3 - choose date\n• MENU - main menu\n• HELP - this help'
    },
    he: {
        welcome: '🕊️ !ברוכים הבאים ל-Aleph Bet Foresight Summit\n\nבחר שפה / Choose language / Выберите язык:\n\n1️⃣ Русский (RU)\n2️⃣ English (EN)\n3️⃣ עברית (HE)',
        greeting: '✡️ !ברכות - אתה עם העם שלך\n!שלום! שמי שלמה\n\n🎉 אתה מוזמן לפגישת Zoom עם הוועדה המארגנת כדי להכיר את המארגנים. כמו כן, תוכל לבחור את המשימה המתאימה לך ביותר!\n\nמתי תרצה להצטרף לפגישת ZOOM? היום, מחר או מחרתיים?\n\n📅 :בחר תאריך נוח לפגישת Zoom',
        date_full: '⚠️ למרבה הצער, כל המקומות לתאריך זה תפוסים. אנא בחר תאריך אחר.',
        confirmation: '🎫 ה-ID שלך: №{participant_id}\n📲 קוד הפעלה ייחודי: {activation_code}\n\n⚠️ להפעלת ה-ID שלך, עליך להשתתף בפגישת Zoom בתאריך שבחרת: {date}\n\n📞 הפגישה תתקיים בשעה 19:00 לפי שעון מוסקבה\n🔗 קישור ל-Zoom יישלח אליך ביום הפגישה\n\n💡 !שמור את הקוד הזה! תצטרך אותו כדי להפעיל את הפרופיל שלך באתר.',
        menu: '📱 תפריט ראשי\n\n🎫 ה-ID שלך: №{participant_id}\n🔑 קוד ההפעלה שלך: {activation_code}\n📅 תאריך הפגישה: {date}\n\nאם אתה צריך לשנות נתונים או לקבל הוראות - כתוב לנו!',
        help: '📖 עזרה\n\nפקודות זמינות:\n• START - התחל רישום\n• RU / EN / HE - בחר שפה\n• 1 / 2 / 3 - בחר תאריך\n• MENU - תפריט ראשי\n• HELP - עזרה זו'
    }
};

// Состояние пользователей (в памяти)
const userStates = new Map();

// Функция для генерации telegram_id из номера WhatsApp
function whatsappToTelegramId(phoneNumber) {
    // Очищаем номер от символов
    const cleanNumber = phoneNumber.replace(/\D/g, '');
    // Делаем отрицательным и уникальным (добавляем префикс -2)
    return -2000000000000000 + parseInt(cleanNumber.slice(-14));
}

// Получение следующих трёх дней
function getNextThreeDays() {
    const days = [];
    const dayNames = {
        ru: ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'],
        en: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        he: ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']
    };
    
    for (let i = 0; i < 3; i++) {
        const date = new Date();
        date.setDate(date.getDate() + i);
        days.push({
            date: date,
            formatted: date.toISOString().split('T')[0],
            names: {
                ru: dayNames.ru[date.getDay()],
                en: dayNames.en[date.getDay()],
                he: dayNames.he[date.getDay()]
            }
        });
    }
    return days;
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
        // Генерируем participant_id и activation_code
        const participantId = await getNextParticipantId();
        const activationCode = Math.floor(100000 + Math.random() * 900000).toString();
        
        await pool.query(
            `INSERT INTO participants 
            (telegram_id, username, first_name, participant_type, language, participant_id, activation_code, phone_number, is_active) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
            [telegramId, username, firstName, 'whatsapp_participant', language, participantId, activationCode, phoneNumber, false]
        );
        
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
async function sendDatesList(phoneNumber, language) {
    const dates = getNextThreeDays();
    const texts = TEXTS[language];
    
    let message = texts.greeting + '\n\n';
    
    for (let i = 0; i < dates.length; i++) {
        const count = await getParticipantsCount(dates[i].formatted);
        const dayLabel = i === 0 ? 
            (language === 'ru' ? 'Сегодня' : language === 'en' ? 'Today' : 'היום') :
            i === 1 ?
            (language === 'ru' ? 'Завтра' : language === 'en' ? 'Tomorrow' : 'מחר') :
            (language === 'ru' ? 'Послезавтра' : language === 'en' ? 'Day after tomorrow' : 'מחרתיים');
        
        message += `${i + 1}️⃣ ${dayLabel} (${dates[i].names[language]}) - ${dates[i].date.toLocaleDateString('ru-RU')} (${count}/${MAX_PARTICIPANTS_PER_DATE})\n`;
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
            
            console.log(`[WHATSAPP] Message from ${phoneNumber}: ${body}`);
            
            const telegramId = whatsappToTelegramId(phoneNumber);
            let user = await getUser(telegramId);
            let state = userStates.get(phoneNumber) || { step: 'start' };
            
            const bodyLower = body.toLowerCase();
            
            // Команда START
            if (bodyLower === 'start' || bodyLower === 'старт' || !user) {
                const texts = TEXTS.ru;
                await msg.reply(texts.welcome);
                userStates.set(phoneNumber, { step: 'choosing_language' });
                return;
            }
            
            // Выбор языка
            if (state.step === 'choosing_language' || bodyLower === 'ru' || bodyLower === 'en' || bodyLower === 'he' || ['1', '2', '3'].includes(body)) {
                let language = null;
                
                if (body === '1' || bodyLower === 'ru' || bodyLower === 'russian' || bodyLower === 'русский') {
                    language = 'ru';
                } else if (body === '2' || bodyLower === 'en' || bodyLower === 'english' || bodyLower === 'английский') {
                    language = 'en';
                } else if (body === '3' || bodyLower === 'he' || bodyLower === 'hebrew' || bodyLower === 'иврит' || body.includes('עברית')) {
                    language = 'he';
                }
                
                if (language && state.step === 'choosing_language') {
                    if (!user) {
                        // Создаем нового пользователя
                        const contact = await msg.getContact();
                        const firstName = contact.pushname || contact.name || phoneNumber;
                        const result = await createUser(telegramId, phoneNumber, firstName, language, phoneNumber);
                        user = await getUser(telegramId);
                    } else {
                        await updateLanguage(telegramId, language);
                        user.language = language;
                    }
                    
                    const datesMessage = await sendDatesList(phoneNumber, language);
                    await msg.reply(datesMessage);
                    userStates.set(phoneNumber, { step: 'choosing_date', language });
                    return;
                }
            }
            
            // Выбор даты
            if (state.step === 'choosing_date' && ['1', '2', '3'].includes(body)) {
                const dateIndex = parseInt(body) - 1;
                const dates = getNextThreeDays();
                
                if (dateIndex >= 0 && dateIndex < dates.length) {
                    const selectedDate = dates[dateIndex].formatted;
                    const count = await getParticipantsCount(selectedDate);
                    
                    if (count >= MAX_PARTICIPANTS_PER_DATE) {
                        const texts = TEXTS[user.language || 'ru'];
                        await msg.reply(texts.date_full);
                        const datesMessage = await sendDatesList(phoneNumber, user.language || 'ru');
                        await msg.reply(datesMessage);
                        return;
                    }
                    
                    await updateZoomDate(telegramId, selectedDate);
                    user = await getUser(telegramId);
                    
                    const texts = TEXTS[user.language || 'ru'];
                    const confirmation = texts.confirmation
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code)
                        .replace('{date}', selectedDate);
                    
                    await msg.reply(confirmation);
                    
                    const menuText = texts.menu
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code)
                        .replace('{date}', user.zoom_date || 'не выбрана');
                    
                    await msg.reply(menuText);
                    userStates.set(phoneNumber, { step: 'registered', language: user.language });
                    return;
                }
            }
            
            // Команда MENU
            if (bodyLower === 'menu' || bodyLower === 'меню' || bodyLower.includes('תפריט')) {
                if (user) {
                    const texts = TEXTS[user.language || 'ru'];
                    const menuText = texts.menu
                        .replace('{participant_id}', user.participant_id)
                        .replace('{activation_code}', user.activation_code)
                        .replace('{date}', user.zoom_date || 'не выбрана');
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
            
            // Если не распознали команду
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

