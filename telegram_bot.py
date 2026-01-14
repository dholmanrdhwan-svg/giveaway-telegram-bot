# telegram_bot.py - المحدث
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram.constants import ParseMode

from database import db
from models import User

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

# حالات المحادثة
SELECT_CHAT_TYPE, ENTER_GIVEAWAY_TEXT, ADD_CONDITIONS, ENTER_WINNER_COUNT, PREVENT_FRAUD = range(5)

# ========== دوال المساعدة ==========

def save_user_from_update(update: Update):
    """حفظ بيانات المستخدم من التحديث"""
    user = update.effective_user
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'language_code': user.language_code
    }
    db.add_or_update_user(user_data)
    return user_data

# ========== معالجات الأوامر ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    save_user_from_update(update)
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🔄 إنشاء روليت", callback_data="create_giveaway")],
        [InlineKeyboardButton("📊 إحصائياتي", callback_data="my_stats")],
        [InlineKeyboardButton("🎯 سحوباتي النشطة", callback_data="my_giveaways")],
        [InlineKeyboardButton("📜 الشروط والأحكام", callback_data="terms")],
        [InlineKeyboardButton("🔐 الخصوصية", callback_data="privacy")],
        [InlineKeyboardButton("🛠️ الدعم الفني", callback_data="support")],
        [InlineKeyboardButton("🔔 إشعارات الفوز", callback_data="toggle_notify")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
🎉 *مرحباً {user.first_name}!*

*بوت السحوبات الذاتي* 🤖

✨ *المميزات:*
✅ إنشاء سحوبات تلقائية
✅ شروط مشاركة متعددة
✅ سجل إداري متكامل
✅ حماية من الغش والاختراق

📊 *إحصائياتك:*
• السحوبات المنشأة: 0
• المشاركات: 0
• مرات الفوز: 0

اختر من القائمة:
"""
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /stats"""
    user_id = update.effective_user.id
    stats = db.get_user_stats(user_id)
    
    if stats:
        stats_text = f"""
📊 *إحصائيات {update.effective_user.first_name}*

*السحوبات:*
• المنشأة: {stats['giveaways_created']}
• المشاركة فيها: {stats['entries_count']}
• مرات الفوز: {stats['wins_count']}

*الحساب:*
• تاريخ الانضمام: {stats['user_since'].strftime('%Y-%m-%d') if stats['user_since'] else 'جديد'}
• الإشعارات: {"✅ مفعلة" if db.get_user(user_id)['notify_on_win'] else "❌ معطلة"}

📈 *نصيحة:* شارك في المزيد من السحوبات لزيادة فرص الفوز!
"""
    else:
        stats_text = "📊 جاري تحميل إحصائياتك..."
    
    await update.message.reply_text(
        stats_text,
        parse_mode=ParseMode.MARKDOWN
    )

# ========== معالجات إنشاء السحب ==========

async def start_giveaway_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء عملية إنشاء سحب"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("✏️ تسجيل قناة", callback_data="register_channel"),
            InlineKeyboardButton("✏️ تسجيل قروب", callback_data="register_group")
        ],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🔄 *إنشاء روليت جديد*\n\n"
        "اختر نوع المجموعة التي تريد إنشاء السحب فيها:\n\n"
        "⚠️ *ملاحظة مهمة:*\n"
        "يجب أن يكون البوت مشرفاً في القناة أو المجموعة.",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return SELECT_CHAT_TYPE

async def handle_chat_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة اختيار نوع المجموعة"""
    query = update.callback_query
    await query.answer()
    
    chat_type = "قناة" if query.data == "register_channel" else "مجموعة"
    
    # حفظ نوع المجموعة في context
    context.user_data['chat_type'] = chat_type
    
    await query.edit_message_text(
        f"✅ تم اختيار {chat_type}\n\n"
        "📝 *الخطوة التالية:*\n"
        "أرسل لي الآن نص السحب أو الروليت.\n\n"
        "📌 *ملاحظات:*\n"
        "• يمكنك استخدام التنسيق (عريض، مائل، إلخ)\n"
        "• يمنع إضافة روابط URL\n"
        "• الحد الأقصى: 2000 حرف",
        parse_mode=ParseMode.MARKDOWN
    )
    
    return ENTER_GIVEAWAY_TEXT

async def receive_giveaway_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استقبال نص السحب"""
    text = update.message.text
    
    # التحقق من النص
    if len(text) < 10:
        await update.message.reply_text(
            "❌ النص قصير جداً. يرجى إدخال وصف مفصل للسحب (10 أحرف على الأقل)."
        )
        return ENTER_GIVEAWAY_TEXT
    
    if len(text) > 2000:
        await update.message.reply_text(
            "❌ النص طويل جداً. الحد الأقصى 2000 حرف."
        )
        return ENTER_GIVEAWAY_TEXT
    
    # حفظ النص
    context.user_data['giveaway_text'] = text
    
    # عرض شاشة الشروط
    keyboard = [
        [InlineKeyboardButton("➕ إضافة شرط", callback_data="add_condition")],
        [InlineKeyboardButton("⏩ تخطي الشروط", callback_data="skip_conditions")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="cancel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚡ *شروط المشاركة*\n\n"
        "هل تريد إضافة شروط للمشاركة في السحب؟\n\n"
        "📌 *الخيارات:*\n"
        "• الاشتراك في قناة\n"
        "• التصويت لمتسابق\n"
        "• تعزيز القناة\n"
        "• للمستخدمين المميزين فقط\n\n"
        "يمكنك إضافة أكثر من شرط.",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return ADD_CONDITIONS

async def handle_conditions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة اختيار الشروط"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "skip_conditions":
        context.user_data['conditions'] = []
        
        await query.edit_message_text(
            "✅ تم تخطي الشروط\n\n"
            "🎯 *الخطوة التالية:*\n"
            "أرسل عدد الفائزين (رقم بين 1 و 100):",
            parse_mode=ParseMode.MARKDOWN
        )
        return ENTER_WINNER_COUNT
    
    elif query.data == "add_condition":
        keyboard = [
            [InlineKeyboardButton("📢 اشتراك في قناة", callback_data="condition_channel")],
            [InlineKeyboardButton("⭐ للمستخدمين المميزين فقط", callback_data="condition_premium")],
            [InlineKeyboardButton("🔄 رجوع", callback_data="back_to_conditions")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📋 *اختر نوع الشرط:*\n\n"
            "1. 📢 **اشتراك في قناة:**\n"
            "   يجب على المشارك الاشتراك في قناة محددة\n\n"
            "2. ⭐ **المستخدمين المميزين:**\n"
            "   للمشتركين في Telegram Premium فقط",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return ADD_CONDITIONS

async def handle_winner_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة عدد الفائزين"""
    text = update.message.text
    
    if not text.isdigit():
        await update.message.reply_text(
            "❌ الرقم غير صالح. يرجى إدخال رقم فقط (مثال: 3):"
        )
        return ENTER_WINNER_COUNT
    
    winner_count = int(text)
    
    if winner_count < 1 or winner_count > 100:
        await update.message.reply_text(
            "❌ الرقم خارج النطاق. يرجى إدخال رقم بين 1 و 100:"
        )
        return ENTER_WINNER_COUNT
    
    context.user_data['winner_count'] = winner_count
    
    keyboard = [
        [InlineKeyboardButton("✅ نعم، منع الغش", callback_data="prevent_fraud_yes")],
        [InlineKeyboardButton("❌ لا، الثقة كاملة", callback_data="prevent_fraud_no")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_winners")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🛡️ *منع الغش والاختراق*\n\n"
        "هل تريد تفعيل نظام منع الغش؟\n\n"
        "✅ *نعم:*\n"
        "• إعادة التحقق من الشروط وقت السحب\n"
        "• منع المشاركات المزيفة\n\n"
        "❌ *لا:*\n"
        "• أسرع ولكن أقل أماناً\n"
        "• يعتمد على التحقق الأولي فقط",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return PREVENT_FRAUD

async def finish_giveaway_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إنهاء إنشاء السحب"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "prevent_fraud_yes":
        context.user_data['prevent_fraud'] = True
    else:
        context.user_data['prevent_fraud'] = False
    
    # إنشاء السحب في قاعدة البيانات
    giveaway_data = {
        'chat_id': 0,  # سيتم تعيينه لاحقاً
        'creator_id': update.effective_user.id,
        'text': context.user_data['giveaway_text'],
        'conditions': context.user_data.get('conditions', []),
        'winner_count': context.user_data['winner_count'],
        'prevent_fraud': context.user_data['prevent_fraud']
    }
    
    giveaway_id = db.create_giveaway(giveaway_data)
    
    if giveaway_id:
        success_message = f"""
✅ *تم إنشاء السحب بنجاح!*

🎁 **تفاصيل السحب:**
• رقم السحب: `{giveaway_id}`
• عدد الفائزين: {context.user_data['winner_count']}
• الحماية: {"✅ مفعلة" if context.user_data['prevent_fraud'] else "❌ معطلة"}

📝 **الخطوات التالية:**
1. أضف البوت مشرفاً في قناتك/مجموعتك
2. أعد توجيه رسالة من القناة للبوت
3. سيتم نشر السحب تلقائياً

🔧 *لاحظ:* هذه نسخة تجريبية، ستصبح جميع الميزات فعالة قريباً!
"""
    else:
        success_message = "❌ حدث خطأ في إنشاء السحب. يرجى المحاولة لاحقاً."
    
    keyboard = [
        [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")],
        [InlineKeyboardButton("🔄 إنشاء سحب جديد", callback_data="create_giveaway")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        success_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return ConversationHandler.END

# ========== معالجات الأزرار العامة ==========

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة ضغطات الأزرار العامة"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "my_stats":
        user_id = query.from_user.id
        stats = db.get_user_stats(user_id)
        
        if stats:
            stats_text = f"""
📊 *إحصائياتك الشخصية*

*السحوبات:*
• المنشأة: {stats['giveaways_created']}
• المشاركة فيها: {stats['entries_count']}
• مرات الفوز: {stats['wins_count']}

*نسبة الفوز:* {stats['wins_count']/max(stats['entries_count'], 1)*100:.1f}%

🎯 *تلميح:* كلما شاركت أكثر، زادت فرص فوزك!
"""
        else:
            stats_text = "📊 لم تشارك في أي سحوبات بعد!"
        
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "toggle_notify":
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        if user:
            new_state = not user['notify_on_win']
            db.update_user_notify(user_id, new_state)
            
            status = "✅ مفعل" if new_state else "❌ معطل"
            await query.answer(f"تم تحديث إشعارات الفوز: {status}")
        else:
            await query.answer("❌ لم يتم العثور على حسابك")

# ========== إعداد Conversation Handler ==========

def setup_conversation_handler():
    """إعداد معالج المحادثة لإنشاء السحب"""
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(start_giveaway_creation, pattern="^create_giveaway$")],
        states={
            SELECT_CHAT_TYPE: [
                CallbackQueryHandler(handle_chat_selection, pattern="^(register_channel|register_group)$"),
                CallbackQueryHandler(lambda u, c: ConversationHandler.END, pattern="^main_menu$")
            ],
            ENTER_GIVEAWAY_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_giveaway_text)
            ],
            ADD_CONDITIONS: [
                CallbackQueryHandler(handle_conditions, pattern="^(add_condition|skip_conditions)$"),
                CallbackQueryHandler(lambda u, c: ConversationHandler.END, pattern="^cancel$")
            ],
            ENTER_WINNER_COUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_winner_count)
            ],
            PREVENT_FRAUD: [
                CallbackQueryHandler(finish_giveaway_creation, pattern="^(prevent_fraud_yes|prevent_fraud_no)$"),
                CallbackQueryHandler(lambda u, c: ConversationHandler.END, pattern="^back_to_winners$")
            ]
        },
        fallbacks=[CallbackQueryHandler(lambda u, c: ConversationHandler.END, pattern="^main_menu$")],
        allow_reentry=True
    )

# ========== الدالة الرئيسية ==========

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN غير محدد")
        return
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("help", stats_command))
    
    # إضافة معالج المحادثة
    application.add_handler(setup_conversation_handler())
    
    # إضافة معالج الأزرار العامة
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^(my_stats|toggle_notify|my_giveaways|terms|privacy|support)$"))
    
    # إضافة معالج للرجوع للقائمة الرئيسية
    application.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    
    logger.info("🤖 بدء تشغيل البوت...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
