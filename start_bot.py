import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Bot starting...")
    
    # محاكاة عمل البوت فقط
    try:
        while True:
            logger.info("Bot is running in simulation mode")
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    
    return True

if __name__ == "__main__":
    main()            return True
            
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")
        return False

if __name__ == "__main__":
    main()
