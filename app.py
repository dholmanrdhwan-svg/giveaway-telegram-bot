from flask import Flask, jsonify, request
import os
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>بوت السحوبات التليجرام</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 500px;
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
