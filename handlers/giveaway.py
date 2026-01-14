"""
Handlers للسحوبات
"""
import json
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import config

# تخزين مؤقت للبيانات (يمكن استبداله بقاعدة بيانات)
temp_giveaway_data = {}
active_giveaways = []
participants = {}

async def start_giveaway(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """بدء إنشاء سحب جديد"""
    user_id = update.effective_user.id
    
    # التحقق إذا كان المستخدم أدمن
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text("⚠️ هذا الأمر للمشرفين فقط!")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "🎁 **إنشاء سحب جديد**\n\n"
        "أرسل عنوان الجائزة (مثال: هاتف iPhone 14):"
    )
    
    return config.GIVEAWAY_TITLE

async def process_giveaway_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """معالجة عنوان السحب"""
    title = update.message.text
    user_id = update.effective_user.id
    
    # حفظ العنوان مؤقتاً
    if user_id not in temp_giveaway_data:
        temp_giveaway_data[user_id] = {}
    
    temp_giveaway_data[user_id]['title'] = title
    
    await update.message.reply_text(
        "📝 **الآن أرسل وصف الجائزة:**\n"
        "(مثال: هاتف iPhone 14 Pro Max 256GB جديد بالكامل)"
    )
    
    return config.GIVEAWAY_DESC

async def process_giveaway_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """معالجة وصف السحب"""
    description = update.message.text
    user_id = update.effective_user.id
    
    temp_giveaway_data[user_id]['description'] = description
    
    await update.message.reply_text(
        "👥 **كم عدد الفائزين؟**\n"
        "(أدخل رقماً من 1 إلى 100):"
    )
    
    return config.GIVEAWAY_WINNERS

async def process_giveaway_winners(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """معالجة عدد الفائزين"""
    try:
        winners = int(update.message.text)
        user_id = update.effective_user.id
        
        if winners < 1 or winners > config.MAX_WINNERS:
            await update.message.reply_text(
                f"⚠️ الرقم يجب أن يكون بين 1 و {config.MAX_WINNERS}.\n"
                "أعد إدخال عدد الفائزين:"
            )
            return config.GIVEAWAY_WINNERS
        
        temp_giveaway_data[user_id]['winners'] = winners
        
        await update.message.reply_text(
            "⏰ **كم مدة السحب بالساعات؟**\n"
            "(أدخل رقماً، مثال: 24 لـ 24 ساعة):"
        )
        
        return config.GIVEAWAY_DURATION
        
    except ValueError:
        await update.message.reply_text("⚠️ يرجى إدخال رقم صحيح. أعد المحاولة:")
        return config.GIVEAWAY_WINNERS

async def process_giveaway_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """معالجة مدة السحب وإنشاؤه"""
    try:
        duration_hours = int(update.message.text)
        user_id = update.effective_user.id
        
        if duration_hours < 1:
            await update.message.reply_text("⚠️ المدة يجب أن تكون ساعة على الأقل. أعد المحاولة:")
            return config.GIVEAWAY_DURATION
        
        # جمع بيانات السحب
        giveaway = temp_giveaway_data[user_id]
        giveaway['duration'] = duration_hours
        giveaway['creator_id'] = user_id
        giveaway['creator_name'] = update.effective_user.first_name
        giveaway['created_at'] = datetime.now()
        giveaway['ends_at'] = datetime.now() + timedelta(hours=duration_hours)
        giveaway['id'] = len(active_giveaways) + 1
        giveaway['participants'] = []
        
        # حفظ السحب في القائمة النشطة
        active_giveaways.append(giveaway)
        
        # حذف البيانات المؤقتة
        if user_id in temp_giveaway_data:
            del temp_giveaway_data[user_id]
        
        # إنشاء زر للانضمام
        keyboard = [
            [InlineKeyboardButton("🎯 انضم للسحب", callback_data=f"join_{giveaway['id']}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # إرسال رسالة السحب
        giveaway_msg = (
            f"🎉 **سحب جديد!**\n\n"
            f"🎁 **الجائزة:** {giveaway['title']}\n"
            f"📝 **الوصف:** {giveaway['description']}\n"
            f"👥 **عدد الفائزين:** {giveaway['winners']}\n"
            f"⏰ **ينتهي في:** {giveaway['ends_at'].strftime('%Y-%m-%d %H:%M')}\n"
            f"👤 **المنشئ:** {giveaway['creator_name']}\n\n"
            f"📊 **المشاركون:** 0"
        )
        
        await update.message.reply_text(giveaway_msg, reply_markup=reply_markup, parse_mode='Markdown')
        
        # إرسال رسالة نجاح للمنشئ
        success_msg = config.MESSAGES['giveaway_created'].format(
            title=giveaway['title'],
            description=giveaway['description'],
            winners=giveaway['winners'],
            duration=giveaway['duration']
        )
        await update.message.reply_text(success_msg)
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text("⚠️ يرجى إدخال رقم صحيح. أعد المحاولة:")
        return config.GIVEAWAY_DURATION

async def join_giveaway(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة انضمام المستخدم للسحب"""
    query = update.callback_query
    await query.answer()
    
    giveaway_id = int(query.data.split('_')[1])
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    
    # البحث عن السحب
    giveaway = None
    for g in active_giveaways:
        if g['id'] == giveaway_id:
            giveaway = g
            break
    
    if not giveaway:
        await query.edit_message_text("❌ هذا السحب لم يعد موجوداً.")
        return
    
    # التحقق إذا انتهى السحب
    if datetime.now() > giveaway['ends_at']:
        await query.edit_message_text("⏰ انتهى وقت هذا السحب.")
        return
    
    # التحقق إذا كان المستخدم منضم بالفعل
    if user_id in giveaway['participants']:
        await query.answer("⚠️ لقد انضممت بالفعل لهذا السحب!", show_alert=True)
        return
    
    # إضافة المستخدم للمشاركين
    giveaway['participants'].append(user_id)
    
    # تحديث رسالة السحب
    updated_msg = (
        f"🎉 **سحب جديد!**\n\n"
        f"🎁 **الجائزة:** {giveaway['title']}\n"
        f"📝 **الوصف:** {giveaway['description']}\n"
        f"👥 **عدد الفائزين:** {giveaway['winners']}\n"
        f"⏰ **ينتهي في:** {giveaway['ends_at'].strftime('%Y-%m-%d %H:%M')}\n"
        f"👤 **المنشئ:** {giveaway['creator_name']}\n\n"
        f"📊 **المشاركون:** {len(giveaway['participants'])}"
    )
    
    await query.edit_message_text(updated_msg, reply_markup=query.message.reply_markup, parse_mode='Markdown')
    await query.answer("🎊 لقد انضممت للسحب! حظاً موفقاً!", show_alert=True)

async def list_giveaways(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض السحوبات النشطة"""
    if not active_giveaways:
        await update.message.reply_text(config.MESSAGES['no_active_giveaways'])
        return
    
    message = "🎰 **السحوبات النشطة:**\n\n"
    
    for idx, giveaway in enumerate(active_giveaways, 1):
        time_left = giveaway['ends_at'] - datetime.now()
        hours_left = int(time_left.total_seconds() // 3600)
        minutes_left = int((time_left.total_seconds() % 3600) // 60)
        
        message += (
            f"{idx}. **{giveaway['title']}**\n"
            f"   👥 المشاركون: {len(giveaway['participants'])}/{giveaway['winners']}\n"
            f"   ⏰ وقت متبقي: {hours_left}س {minutes_left}د\n"
            f"   🆔 الرقم: {giveaway['id']}\n\n"
        )
    
    message += "\nللانضمام للسحب، اضغط على زر 'انضم للسحب' في رسالة السحب."
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def cancel_giveaway(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """إلغاء إنشاء السحب"""
    user_id = update.effective_user.id
    
    if user_id in temp_giveaway_data:
        del temp_giveaway_data[user_id]
    
    await update.message.reply_text("❌ تم إلغاء إنشاء السحب.")
    return ConversationHandler.END
