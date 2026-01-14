import os
import sys
import threading
import signal
from flask import Flask, jsonify, request
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# الحصول على المنفذ من متغير البيئة
PORT = int(os.environ.get('PORT', 5000))

# متغيرات البوت
bot_thread = None
bot_instance = None
bot_running = False

# ============ إدارة البوت ============

def run_bot():
    """
    تشغيل البوت في خيط منفصل
    """
    global bot_instance, bot_running
    
    try:
        logger.info("جاري تشغيل البوت...")
        
        # استيراد وبدء البوت (اضبط بناءً على ملفاتك)
        try:
            # جرب استيراد من telegram_bot.py أولاً
            from telegram_bot import main as bot_main
            logger.info("تم تحميل البوت من telegram_bot.py")
        except ImportError:
            try:
                # جرب bot.py إذا telegram_bot.py غير موجود
                from bot import main as bot_main
                logger.info("تم تحميل البوت من bot.py")
            except ImportError:
                # جرب start_bot.py
                from start_bot import main as bot_main
                logger.info("تم تحميل البوت من start_bot.py")
        
        # تشغيل البوت
        bot_running = True
        bot_instance = bot_main()
        
    except Exception as e:
        logger.error(f"خطأ في تشغيل البوت: {e}")
        bot_running = False

def stop_bot():
    """
    إيقاف البوت بشكل آمن
    """
    global bot_running
    bot_running = False
    # يمكن إضافة منطق لإيقاف البوت هنا إذا كان يدعم ذلك
    logger.info("تم طلب إيقاف البوت")

# ============ API Endpoints ============

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'service': 'Giveaway Bot & Web Service',
        'bot_status': 'running' if bot_running else 'stopped',
        'endpoints': {
            '/': 'Home page',
            '/health': 'Health check',
            '/bot/start': 'Start bot (POST)',
            '/bot/stop': 'Stop bot (POST)',
            '/bot/status': 'Bot status',
            '/admin': 'Admin panel'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'bot': 'running' if bot_running else 'stopped',
        'web': 'running'
    })

@app.route('/bot/start', methods=['POST'])
def start_bot():
    global bot_thread
    
    if bot_running:
        return jsonify({'status': 'error', 'message': 'البوت يعمل بالفعل'}), 400
    
    # بدء البوت في خيط جديد
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'تم بدء تشغيل البوت',
        'bot_thread': bot_thread.is_alive()
    })

@app.route('/bot/stop', methods=['POST'])
def stop_bot_endpoint():
    if not bot_running:
        return jsonify({'status': 'error', 'message': 'البوت غير نشط'}), 400
    
    stop_bot()
    return jsonify({'status': 'success', 'message': 'تم إيقاف البوت'})

@app.route('/bot/status')
def bot_status():
    return jsonify({
        'running': bot_running,
        'thread_alive': bot_thread.is_alive() if bot_thread else False,
        'timestamp': os.times().user
    })

@app.route('/admin')
def admin_panel():
    return """
    <html>
        <head><title>Admin Panel</title></head>
        <body>
            <h1>Giveaway Bot Admin</h1>
            <div id="status">جاري التحقق...</div>
            <button onclick="startBot()">تشغيل البوت</button>
            <button onclick="stopBot()">إيقاف البوت</button>
            <script>
                async function checkStatus() {
                    const res = await fetch('/bot/status');
                    const data = await res.json();
                    document.getElementById('status').innerHTML = 
                        `حالة البوت: ${data.running ? '🟢 نشط' : '🔴 متوقف'}`;
                }
                
                async function startBot() {
                    await fetch('/bot/start', {method: 'POST'});
                    setTimeout(checkStatus, 1000);
                }
                
                async function stopBot() {
                    await fetch('/bot/stop', {method: 'POST'});
                    setTimeout(checkStatus, 1000);
                }
                
                // تحديث الحالة كل 5 ثواني
                setInterval(checkStatus, 5000);
                checkStatus();
            </script>
        </body>
    </html>
    """

# ============ إدارة الإغلاق ============

def signal_handler(signum, frame):
    """
    معالج الإشارات للإغلاق الآمن
    """
    logger.info("تلقي إشارة إيقاف...")
    stop_bot()
    sys.exit(0)

# ============ التهيئة والتشغيل ============

if __name__ == '__main__':
    # تسجيل معالجات الإشارات
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # بدء البوت تلقائياً
    logger.info("بدء تشغيل الخدمة...")
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # بدء خادم Flask
    logger.info(f"بدء خادم Flask على المنفذ {PORT}")
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False,
        use_reloader=False  # مهم عند استخدام الخيوط
    )d
