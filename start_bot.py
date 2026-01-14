# start_bot.py
import os
import sys

# تأكد من أن المسار الحالي مضاف
sys.path.append('.')

from telegram_bot import main

if __name__ == "__main__":
    print("🚀 بدء تشغيل بوت السحوبات...")
    main()
