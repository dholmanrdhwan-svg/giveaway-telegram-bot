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

# استيراد الإعدادات
from config import TELEGRAM_BOT_TOKEN, ADMIN_IDS, MESSAGES
import handlers.start as start_handlers
import handlers.giveaway as giveaway_handlers
import handlers.admin as admin_handlers

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# متغيرات المحادثة
GIVEAWAY_TITLE, GIVEAWAY_DESC, GIVEAWAY_WINNERS, GIVEAWAY_DURATION = range(4)

def main() -> None:
    """بدء تشغيل البوت"""
    
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ لم يتم العثور على TELEGRAM_BOT_TOKEN")
        raise ValueError("يجب تعيين TELEGRAM_BOT_TOKEN في متغيرات Render")
    
    logger.info("🚀 بدء تشغيل بوت الجيف أواي...")
    
    # إنشاء التطبيق
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start_handlers.start))
    application.add_handler(CommandHandler("help", start_handlers.help_command))
    application.add_handler(CommandHandler("myid", start_handlers.get_id))
    application.add_handler(CommandHandler("giveaways", giveaway_handlers.list_giveaways))
    application.add_handler(CommandHandler("admin", admin_handlers.admin_panel))
    
    # محادثة إنشاء سحب جديد
    giveaway_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newgiveaway', giveaway_handlers.start_giveaway)],
        states={
            GIVEAWAY_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, giveaway_handlers.process_giveaway_title)],
            GIVEAWAY_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, giveaway_handlers.process_giveaway_description)],
            GIVEAWAY_WINNERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, giveaway_handlers.process_giveaway_winners)],
            GIVEAWAY_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, giveaway_handlers.process_giveaway_duration)],
        },
        fallbacks=[CommandHandler('cancel', giveaway_handlers.cancel_giveaway)]
    )
    
    application.add_handler(giveaway_conv_handler)
    application.add_handler(CallbackQueryHandler(giveaway_handlers.join_giveaway, pattern='^join_'))
    application.add_handler(CommandHandler('broadcast', admin_handlers.broadcast_message))
    
    # بدء البوت
    logger.info("✅ البوت يعمل الآن...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
