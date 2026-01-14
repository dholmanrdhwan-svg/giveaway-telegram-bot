# utils.py
from datetime import datetime

def format_date(date_obj):
    """تنسيق التاريخ بالعربية"""
    return date_obj.strftime("%Y-%m-%d %H:%M")

def validate_text(text, min_len=10, max_len=2000):
    """التحقق من صحة النص"""
    return min_len <= len(text) <= max_len
