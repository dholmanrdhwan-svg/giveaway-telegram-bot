# config.py
import os

class Config:
    # الإعدادات الأساسية
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    PORT = int(os.getenv('PORT', 10000))
    
    # إعدادات الأمان
    MAX_ENTRIES_PER_USER = 50
    MAX_GIVEAWAYS_PER_DAY = 5
    REQUEST_TIMEOUT = 30
    
    # رسائل البوت (نصوص عربية)
    MESSAGES = {
        'welcome': "🎉 أهلاً بك في بوت السحوبات!",
        'help': "🆘 للمساعدة، ارسل /help",
        'error': "❌ حدث خطأ، يرجى المحاولة لاحقاً"
    }
    
    # المنتجات (للنجوم)
    PRODUCTS = {
        'comment': {'stars': 20, 'name': 'تعليق على منشور'},
        'boost': {'stars': 50, 'name': 'تعزيز القناة'}
    }

config = Config()
