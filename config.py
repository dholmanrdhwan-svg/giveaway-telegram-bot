"""
إعدادات وتكوين البوت
"""
import os

# توكن البوت
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    print("⚠️ تحذير: TELEGRAM_BOT_TOKEN غير معين")

# معرف المطور
ADMIN_IDS = []
admin_ids_str = os.environ.get('ADMIN_IDS', '')
if admin_ids_str:
    try:
        ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(',') if x.strip()]
    except ValueError:
        print(f"⚠️ تحذير: ADMIN_IDS غير صالحة: {admin_ids_str}")

# إعدادات قاعدة البيانات
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///giveaway.db')

# إعدادات التطبيق
BOT_USERNAME = None  # سيتم تعبئته تلقائياً

# إعدادات السحب
MAX_WINNERS = 100
MIN_DURATION_MINUTES = 1
MAX_DURATION_DAYS = 30

# متغيرات تخزين مؤقتة (تستخدم في handlers)
active_giveaways = []
temp_giveaway_data = {}

# نصوغ رسائل البوت
MESSAGES = {
    'welcome': "🎉 أهلاً بك في بوت السحوبات!\n\n"
               "استخدم الأوامر التالية:\n"
               "/start - بدء الاستخدام\n"
               "/newgiveaway - إنشاء سحب جديد (للمشرفين)\n"
               "/giveaways - عرض السحوبات النشطة\n"
               "/help - المساعدة\n"
               "/myid - عرض معرفك",
    
    'admin_welcome': "🛠 لوحة تحكم الأدمن\n\n"
                    "/broadcast - إرسال رسالة للجميع\n"
                    "/stats - إحصائيات البوت",
    
    'giveaway_created': "✅ تم إنشاء السحب بنجاح!\n\n"
                       "🎁 الجائزة: {title}\n"
                       "📝 الوصف: {description}\n"
                       "👥 عدد الفائزين: {winners}\n"
                       "⏰ المدة: {duration} ساعة",
    
    'join_success': "🎊 لقد انضممت للسحب! حظاً موفقاً!",
    'already_joined': "⚠️ لقد انضممت بالفعل لهذا السحب.",
    'giveaway_ended': "⏰ انتهى هذا السحب.",
    'no_active_giveaways': "📭 لا توجد سحوبات نشطة حالياً."
}
