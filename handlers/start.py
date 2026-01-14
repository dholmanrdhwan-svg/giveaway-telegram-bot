"""
Handlers لأوامر البداية والمساعدة
"""
from telegram import Update
from telegram.ext import ContextTypes
import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /start"""
    user = update.effective_user
    
    welcome_msg = f"مرحباً {user.first_name}!\n\n{config.MESSAGES['welcome']}"
    
    await update.message.reply_text(welcome_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /help"""
    help_text = """
🤖 **أوامر البوت:**

🎰 **للمستخدمين:**
/start - بدء استخدام البوت
/newgiveaway - إنشاء سحب جديد (للمشرفين)
/giveaways - عرض السحوبات النشطة
/help - عرض هذه الرسالة

🛠 **للمشرفين:**
/admin - لوحة التحكم
/broadcast - إرسال رسالة للجميع

📞 **للتواصل والدعم:**
@username
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')
