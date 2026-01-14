"""
Handlers لوظائف الأدمن
"""
from telegram import Update
from telegram.ext import ContextTypes
import config

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """لوحة تحكم الأدمن"""
    user_id = update.effective_user.id
    
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text("⚠️ هذا الأمر للمشرفين فقط!")
        return
    
    stats_message = (
        "🛠 **لوحة تحكم الأدمن**\n\n"
        f"👥 عدد السحوبات النشطة: {len([g for g in active_giveaways])}\n"
        f"📊 إجمالي المشاركات: {sum(len(g['participants']) for g in active_giveaways)}\n\n"
        "**الأوامر المتاحة:**\n"
        "/broadcast - إرسال رسالة للجميع\n"
        "/stats - عرض إحصائيات مفصلة"
    )
    
    await update.message.reply_text(stats_message, parse_mode='Markdown')

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرسال رسالة للجميع"""
    user_id = update.effective_user.id
    
    if user_id not in config.ADMIN_IDS:
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
    
    # في الواقع، هنا يجب إرسال الرسالة لجميع مستخدمي البوت
    # لكن يحتاج حفظ المستخدمين في قاعدة بيانات
    
    await update.message.reply_text(
        f"✅ تم إعداد رسالة البث:\n\n{message}\n\n"
        "⚠️ ملاحظة: هذه النسخة التجريبية تحتاج قاعدة بيانات لحفظ المستخدمين."
    )
