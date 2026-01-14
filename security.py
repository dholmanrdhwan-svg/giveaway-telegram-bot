# security.py
import hmac
import hashlib
import os

SECRET_KEY = os.getenv('SECRET_KEY', '').encode()

def sign_data(data: str) -> str:
    """توقيع البيانات"""
    return hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()

def verify_signature(data: str, signature: str) -> bool:
    """التحقق من التوقيع"""
    expected = sign_data(data)
    return hmac.compare_digest(expected, signature)
