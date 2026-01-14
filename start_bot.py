"""
ملف بدء تشغيل البوت الرئيسي
"""
import logging
import time
import sys

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    الدالة الرئيسية للبوت
    """
    logger.info("🎮 بدء تشغيل بوت الجيف أواي...")
    
    try:
        # محاولة استيراد وتشغيل بوت تيليجرام الحقيقي
        from telegram_bot import main as telegram_main
        logger.info("✅ تم العثور على بوت تيليجرام، جاري التشغيل...")
        return telegram_main()
        
    except ImportError:
        logger.warning("⚠️ لم يتم العثور على telegram_bot.py، جاري تشغيل وضع المحاكاة...")
        
        # وضع المحاكاة إذا لم يوجد البوت الحقيقي
        try:
            while True:
                logger.info("🤖 البوت يعمل في وضع المحاكاة...")
                time.sleep(60)  # انتظر دقيقة بين كل عملية
        except KeyboardInterrupt:
            logger.info("🛑 توقف البوت عن العمل")
            return True
            
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")
        return False

if __name__ == "__main__":
    main()
