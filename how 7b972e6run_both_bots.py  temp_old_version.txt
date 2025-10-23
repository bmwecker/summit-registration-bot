"""
Запуск Telegram и Email ботов параллельно
"""

import asyncio
import threading
import logging
import sys
import time

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_telegram_bot():
    """Запуск Telegram-бота"""
    try:
        logger.info("🤖 Starting Telegram bot...")
        from bot import main
        main()
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")
        sys.exit(1)


def run_email_bot():
    """Запуск Email-бота"""
    try:
        logger.info("📧 Starting Email bot...")
        from email_bot import start_email_bot
        start_email_bot()
    except Exception as e:
        logger.error(f"Email bot error: {e}")
        # Email-бот опционален, не падаем если он не настроен
        if "IMAP not configured" in str(e) or "not configured" in str(e).lower():
            logger.warning("📧 Email bot not configured - skipping")
        else:
            raise


def main():
    """Главная функция - запуск обоих ботов"""
    logger.info("🚀 Starting Aleph Bet Foresight Summit Bots...")
    logger.info("=" * 60)
    
    # Проверяем настройки Email
    import os
    imap_configured = bool(os.getenv("IMAP_USER") and os.getenv("IMAP_PASSWORD"))
    
    if imap_configured:
        logger.info("✅ Email bot configured - starting both bots")
        
        # Запускаем Email-бот в отдельном потоке
        email_thread = threading.Thread(
            target=run_email_bot,
            name="EmailBot",
            daemon=True  # Завершится когда главный процесс закончится
        )
        email_thread.start()
        logger.info("📧 Email bot thread started")
        
        # Небольшая задержка для инициализации Email-бота
        time.sleep(2)
    else:
        logger.warning("⚠️ Email bot not configured (IMAP settings missing)")
        logger.info("📱 Starting Telegram bot only...")
    
    # Запускаем Telegram-бота в главном потоке
    logger.info("🤖 Starting Telegram bot in main thread...")
    run_telegram_bot()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Bots stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

