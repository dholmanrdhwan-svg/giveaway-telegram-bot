import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🔄 إنشاء روليت", callback_data="create_giveaway")],
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")],
        [InlineKeyboardButton("📜 الشروط والأحكام", callback_data="terms")],
        [InlineKeyboardButton("🛠️ الدعم الفني", callback_data="support")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
    🎉 *مرحباً {user.first_name}!*
    
    *بوت السحوبات الذاتي* 🤖
    
    يمكنك إنشاء سحوبات في قناتك أو مجموعتك بسهولة.
    
    *✨ المميزات:*
    ✅ إنشاء سحب تلقائي
    ✅ شروط متعددة
    ✅ سجل إداري
    ✅ حماية من الغش
    
    اختر من القائمة:
    """
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج ضغطات الأزرار"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "create_giveaway":
        await query.edit_message_text("🚀 جارٍ إنشاء سحب جديد...")
    elif query.data == "stats":
        await query.edit_message_text("📊 الإحصائيات قريباً...")
    elif query.data == "terms":
        await query.edit_message_text("""
        📜 *الشروط والأحكام*
        
        1. يمنع النشاط غير القانوني
        2. تسليم الجوائز مسؤولية المنشئ
        3. النجوم غير قابلة للاسترجاع
        4. التبرع اختياري
        """, parse_mode='Markdown')
    elif query.data == "support":
        await query.edit_message_text("🛠️ *الدعم الفني*\n\n@YourSupportUsername")

def main():
    """الدالة الرئيسية"""
    if not BOT_TOKEN:
        logger.error("❌ لم يتم تعيين BOT_TOKEN")
        return
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("🤖 بدء تشغيل البوت...")
    application.run_polling()

if __name__ == '__main__':
    main()
