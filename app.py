# app.py - المحدث
from flask import Flask, request, jsonify
import os
import threading
import logging
from datetime import datetime

from database import db

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
PORT = int(os.getenv('PORT', 10000))

def run_telegram_bot():
    """تشغيل بوت التليجرام"""
    try:
        if BOT_TOKEN:
            logger.info("🚀 بدء تشغيل بوت التليجرام...")
            
            # استيراد وتشغيل البوت
            from telegram_bot import main
            main()
            
        else:
            logger.warning("⚠️ BOT_TOKEN غير محدد")
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")

@app.route('/')
def home():
    # جلب إحصائيات من قاعدة البيانات
    stats = {
        'users': 0,
        'giveaways': 0,
        'entries': 0
    }
    
    try:
        # يمكنك إضافة استعلامات لجلب الإحصائيات الحقيقية هنا
        pass
    except Exception as e:
        logger.error(f"❌ خطأ في جلب الإحصائيات: {e}")
    
    return f'''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>بوت السحوبات التليجرام</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 700px;
                width: 100%;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
            }}
            .stat-box {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                min-width: 150px;
            }}
            .stat-number {{
                font-size: 32px;
                font-weight: bold;
                color: #667eea;
            }}
            .stat-label {{
                color: #666;
                margin-top: 10px;
            }}
            .info-box {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                border-right: 5px solid #667eea;
                text-align: right;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #333; margin-bottom: 10px;">🤖 بوت السحوبات التليجرام</h1>
            <p style="color: #666; margin-bottom: 30px;">نظام متكامل لإدارة السحوبات الذاتية</p>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{stats['users']}</div>
                    <div class="stat-label">👥 مستخدم</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats['giveaways']}</div>
                    <div class="stat-label">🎁 سحب</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats['entries']}</div>
                    <div class="stat-label">📝 مشاركة</div>
                </div>
            </div>
            
            <div class="info-box">
                <h3>✅ البوت يعمل بنجاح</h3>
                <p>• نظام قاعدة البيانات: {"✅ نشط" if db.connection_pool else "⚠️ SQLite"}</p>
                <p>• بوت التليجرام: {"✅ نشط" if BOT_TOKEN else "❌ غير نشط"}</p>
                <p>• تاريخ التشغيل: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
            </div>
            
            <div style="margin-top: 30px;">
                <h3>🚀 الميزات المتوفرة:</h3>
                <p>✅ إنشاء سحوبات تلقائية</p>
                <p>✅ قاعدة بيانات مستخدمين</p>
                <p>✅ إحصائيات متقدمة</p>
                <p>🔄 قيد التطوير: نظام النجوم والمدفوعات</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    db_status = "healthy" if db.connection_pool else "sqlite"
    
    return jsonify({
        "status": "healthy",
        "database": db_status,
        "bot": bool(BOT_TOKEN),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/stats')
def api_stats():
    """واجهة برمجية للإحصائيات"""
    try:
        # يمكنك إضافة استعلامات قاعدة البيانات هنا
        return jsonify({
            "status": "success",
            "data": {
                "users": 0,
                "giveaways": 0,
                "active_giveaways": 0,
                "total_winners": 0
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # بدء البوت في thread منفصل
    if BOT_TOKEN:
        bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
        bot_thread.start()
        logger.info("✅ بدء تشغيل البوت في الخلفية")
    
    logger.info(f"🌐 بدء خادم Flask على المنفذ {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)                max-width: 500px;
                width: 100%;
            }
            .success-icon {
                font-size: 80px;
                color: #4CAF50;
                margin-bottom: 20px;
            }
            h1 {
                color: #333;
                margin-bottom: 15px;
                font-size: 28px;
            }
            p {
                color: #666;
                margin-bottom: 25px;
                line-height: 1.6;
                font-size: 18px;
            }
            .status {
                display: inline-block;
                background: #4CAF50;
                color: white;
                padding: 10px 25px;
                border-radius: 50px;
                font-weight: bold;
                margin-top: 20px;
            }
            .info {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                margin-top: 25px;
                border-right: 5px solid #667eea;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">✅</div>
            <h1>بوت السحوبات يعمل بنجاح!</h1>
            <p>تم نشر البوت على Render وجاهز للاستخدام.</p>
            <div class="info">
                <p>🚀 يمكنك الآن إضافة البوت على تيليجرام وإرسال /start</p>
            </div>
            <div class="status">الحالة: نشط ✅</div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "Telegram Giveaway Bot",
        "timestamp": "2024-12-14T10:00:00Z",
        "version": "2.0.0"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        logger.info(f"📩 Webhook received: {data}")
        return jsonify({"status": "ok", "message": "تم استلام البيانات"})
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    logger.info(f"🚀 Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Telegram Giveaway Bot",
        "timestamp": datetime.now().isoformat(),
        "message": "✅ البوت يعمل بنجاح!"
    })

# مسار الفحص الصحي
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# مسار ويبهوك تيليجرام
@app.route('/webhook/<token>', methods=['POST'])
def telegram_webhook(token):
    try:
        data = request.get_json()
        logger.info(f"📩 رسالة واردة: {data}")
        
        # هنا سيتم معالجة رسائل التليجرام
        return jsonify({"status": "received"}), 200
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
