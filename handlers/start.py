"""
Handlers لأوامر البداية والمساعدة
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import MESSAGES, ADMIN_IDS
from datetime import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /start"""
    user = update.effective_user
    
    welcome_msg = f"مرحباً {user.first_name}!\n\n{MESSAGES['welcome']}"
    
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
/myid - عرض معرفك

🛠 **للمشرفين:**
/admin - لوحة التحكم
/broadcast - إرسال رسالة للجميع

⏰ **السحوبات:**
- يمكن للمشرفين إنشاء سحوبات جديدة
- يمكن للجميع الانضمام للسحوبات النشطة
- يتم اختيار الفائزين عشوائياً بعد انتهاء المدة
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /myid - للحصول على معرف المستخدم"""
    user = update.effective_user
    
    is_admin = "✅ (أدمن)" if user.id in ADMIN_IDS else "❌ (مستخدم عادي)"
    
    await update.message.reply_text(
        f"🆔 **معلومات حسابك:**\n\n"
        f"👤 الاسم: {user.first_name}\n"
        f"📛 المعرف: @{user.username if user.username else 'غير معروف'}\n"
        f"🔢 الرقم: `{user.id}` {is_admin}\n\n"
        f"📋 **لتصبح أدمن، أضف هذا الرقم في Render:**\n"
        f"`ADMIN_IDS={user.id}`",
        parse_mode='Markdown'
    )
