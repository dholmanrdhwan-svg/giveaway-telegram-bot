"""
الملف الرئيسي لبوت تليجرام للجيف أواي (السحوبات)
"""
import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# استيراد handlers
from handlers.start import start, help_command
from handlers.giveaway import (
    start_giveaway,
    create_giveaway,
    process_giveaway_title,
    process_giveaway_description,
    process_giveaway_winners,
    process_giveaway_duration,
    list_giveaways,
    join_giveaway,
    cancel_giveaway
)
from handlers.admin import admin_panel, broadcast_message

# متغيرات المحادثة
GIVEAWAY_TITLE, GIVEAWAY_DESC, GIVEAWAY_WINNERS, GIVEAWAY_DURATION = range(4)

def main() -> None:
    """بدء تشغيل البوت"""
    
    # الحصول على توكن البوت من المتغيرات البيئية
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        logger.error("❌ لم يتم العثور على TELEGRAM_BOT_TOKEN في المتغيرات البيئية")
        raise ValueError("يجب تعيين TELEGRAM_BOT_TOKEN في ملف .env")
    
    logger.info("🚀 بدء تشغيل بوت الجيف أواي...")
    
    # إنشاء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("giveaways", list_giveaways))
    application.add_handler(CommandHandler("admin", admin_panel))
    
    # محادثة إنشاء سحب جديد
    giveaway_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newgiveaway', start_giveaway)],
        states={
            GIVEAWAY_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_giveaway_title)],
            GIVEAWAY_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_giveaway_description)],
            GIVEAWAY_WINNERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_giveaway_winners)],
            GIVEAWAY_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_giveaway_duration)],
        },
        fallbacks=[CommandHandler('cancel', cancel_giveaway)]
    )
    
    application.add_handler(giveaway_conv_handler)
    application.add_handler(CallbackQueryHandler(join_giveaway, pattern='^join_'))
    application.add_handler(CommandHandler('broadcast', broadcast_message))
    
    # بدء البوت
    logger.info("✅ البوت يعمل الآن...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
