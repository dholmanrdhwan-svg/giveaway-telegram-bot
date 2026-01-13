import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # إعدادات البوت
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # إعدادات قاعدة البيانات
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///giveaway.db')
    
    # إعدادات الويب هوك
    USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'true').lower() == 'true'
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    PORT = int(os.getenv('PORT', 10000))
    
    # القنوات الإلزامية
    MANDATORY_CHANNELS = [
        {
            'username': '@YourChannel',
            'title': 'القناة الرسمية',
            'id': -1001234567890
        }
    ]
    
    # رسائل البوت
    MESSAGES = {
        'welcome': "🎉 مرحباً بك في بوت السحوبات!",
        'help': "🆘 للمساعدة اضغط /help",
        'error': "❌ حدث خطأ، حاول لاحقاً"
    }

config = Config()
