"""
Handlers لوظائف الأدمن
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS, active_giveaways
from datetime import datetime

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """لوحة تحكم الأدمن"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⚠️ هذا الأمر للمشرفين فقط!")
        return
    
    # إحصائيات
    active_count = len(active_giveaways)
    total_participants = sum(len(g['participants']) for g in active_giveaways)
    
    stats_message = (
        "🛠 **لوحة تحكم الأدمن**\n\n"
        f"📊 **الإحصائيات:**\n"
        f"   👥 عدد السحوبات النشطة: {active_count}\n"
        f"   🎯 إجمالي المشاركات: {total_participants}\n\n"
        f"🔧 **الأوامر المتاحة:**\n"
        f"   /newgiveaway - إنشاء سحب جديد\n"
        f"   /giveaways - عرض جميع السحوبات\n"
        f"   /broadcast - إرسال رسالة للجميع\n\n"
        f"👑 **أنت أدمن** - لديك صلاحيات كاملة"
    )
    
    await update.message.reply_text(stats_message, parse_mode='Markdown')

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرسال رسالة للجميع"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⚠️ هذا الأمر للمشرفين فقط!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 **استخدام أمر البث:**\n"
            "/broadcast <الرسالة>\n\n"
            "مثال:\n"
            "/broadcast مرحباً بالجميع! هناك سحب جديد."
        )
        return
    
    message = ' '.join(context.args)
    
    # في النسخة الحالية، نوضح أن البث يحتاج قاعدة بيانات
    await update.message.reply_text(
        f"✅ **رسالة البث جاهزة:**\n\n"
        f"{message}\n\n"
        f"📝 **ملاحظة:**\n"
        f"هذه النسخة التجريبية تخزن المستخدمين في الذاكرة فقط.\n"
        f"للبث الحقيقي، نحتاج قاعدة بيانات لحفظ جميع المستخدمين."
    )
