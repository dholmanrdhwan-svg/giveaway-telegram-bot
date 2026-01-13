```python
import os
import logging
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# مسار الصفحة الرئيسية
@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Telegram Giveaway Bot",
import os
import logging
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# مسار الصفحة الرئيسية
@app.route('/')
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
