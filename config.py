"""
إعدادات وتكوين البوت
"""
import os
from dotenv import load_dotenv

load_dotenv()

# توكن البوت
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ يرجى تعيين TELEGRAM_BOT_TOKEN في ملف .env")

# معرف المطور
ADMIN_IDS = [int(x.strip()) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]

# إعدادات قاعدة البيانات
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///giveaway.db')

# إعدادات التطبيق
BOT_USERNAME = None  # سيتم تعبئته تلقائياً

# إعدادات السحب
MAX_WINNERS = 100
MIN_DURATION_MINUTES = 1
MAX_DURATION_DAYS = 30

# نصوغ رسائل البوت
MESSAGES = {
    'welcome': "🎉 أهلاً بك في بوت السحوبات!\n\n"
               "استخدم الأوامر التالية:\n"
               "/start - بدء الاستخدام\n"
               "/newgiveaway - إنشاء سحب جديد\n"
               "/giveaways - عرض السحوبات النشطة\n"
               "/help - المساعدة",
    
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
