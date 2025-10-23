const express = require('express');
const QRCode = require('qrcode');
const { initWhatsAppBot } = require('./whatsapp_bot');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

let currentQR = null;
let botReady = false;
let whatsappClient = null;

// HTML страница для отображения QR кода
const htmlPage = (qrDataUrl, isReady) => `
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="10">
    <title>WhatsApp Bot QR Code</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .qr-container {
            background: white;
            padding: 20px;
            border-radius: 15px;
            display: inline-block;
            margin: 20px 0;
        }
        .qr-code {
            max-width: 300px;
            width: 100%;
            height: auto;
        }
        .status {
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-weight: bold;
        }
        .status.waiting {
            background: #fff3cd;
            color: #856404;
        }
        .status.ready {
            background: #d4edda;
            color: #155724;
        }
        .instructions {
            text-align: left;
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .instructions ol {
            margin: 10px 0;
            padding-left: 20px;
        }
        .instructions li {
            margin: 10px 0;
            line-height: 1.6;
        }
        .emoji {
            font-size: 24px;
        }
        .refresh-note {
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🟢 WhatsApp Bot</h1>
        <p class="subtitle">Aleph Bet Foresight Summit</p>
        
        ${isReady ? `
            <div class="status ready">
                <span class="emoji">✅</span> Бот подключен и работает!
            </div>
            <p style="margin-top: 20px; color: #666;">
                Теперь можно закрыть эту страницу.<br>
                Бот будет работать автоматически.
            </p>
        ` : qrDataUrl ? `
            <div class="qr-container">
                <img src="${qrDataUrl}" alt="QR Code" class="qr-code">
            </div>
            <div class="status waiting">
                <span class="emoji">⏳</span> Ожидание сканирования...
            </div>
            
            <div class="instructions">
                <strong>📱 Как подключить:</strong>
                <ol>
                    <li>Откройте WhatsApp на телефоне</li>
                    <li>Нажмите <strong>Меню (⋮)</strong> → <strong>Связанные устройства</strong></li>
                    <li>Нажмите <strong>Привязать устройство</strong></li>
                    <li>Отсканируйте QR-код выше</li>
                </ol>
            </div>
            
            <p class="refresh-note">
                Страница обновляется каждые 10 секунд
            </p>
        ` : `
            <div class="status waiting">
                <span class="emoji">⏳</span> Инициализация бота...
            </div>
            <p style="margin-top: 20px; color: #666;">
                QR-код появится через несколько секунд
            </p>
        `}
    </div>
</body>
</html>
`;

// Главная страница с QR кодом
app.get('/', async (req, res) => {
    try {
        let qrDataUrl = null;
        
        if (currentQR && !botReady) {
            qrDataUrl = await QRCode.toDataURL(currentQR);
        }
        
        res.send(htmlPage(qrDataUrl, botReady));
    } catch (error) {
        console.error('[SERVER] Error generating QR page:', error);
        res.status(500).send('<h1>Error generating QR code</h1>');
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: botReady ? 'ready' : 'initializing',
        timestamp: new Date().toISOString()
    });
});

// Запуск сервера
app.listen(PORT, () => {
    console.log(`[SERVER] Server running on port ${PORT}`);
    console.log(`[SERVER] Open http://localhost:${PORT} to see QR code`);
    
    // Инициализация WhatsApp бота
    whatsappClient = initWhatsAppBot(
        (qr) => {
            currentQR = qr;
            console.log('[SERVER] QR code updated');
        },
        () => {
            botReady = true;
            currentQR = null;
            console.log('[SERVER] Bot is ready and connected!');
        }
    );
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('[SERVER] SIGTERM received, shutting down gracefully');
    if (whatsappClient) {
        whatsappClient.destroy();
    }
    process.exit(0);
});

