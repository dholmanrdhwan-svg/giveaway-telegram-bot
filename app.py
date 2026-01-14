"""
Flask Application for Render Deployment
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Get port from environment variable (Render provides this)
PORT = int(os.environ.get('PORT', 5000))

# ============ ROUTES ============

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'status': 'active',
        'message': 'Flask app is running on Render',
        'port': PORT
    })

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test API endpoint"""
    return jsonify({
        'message': 'API is working',
        'method': request.method
    })

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============ APPLICATION START ============

if __name__ == '__main__':
    # This is the corrected line - make sure PORT is an integer
    app.run(
        host='0.0.0.0',  # Important for Render
        port=PORT,        # Use PORT from environment
        debug=False,      # Set to False in production
        threaded=True     # Better for handling multiple requests
    )            }
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
