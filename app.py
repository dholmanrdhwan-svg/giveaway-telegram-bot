"""
تطبيق ويب للبوت - يعمل على Render
"""
import os
from flask import Flask, jsonify, request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# الحصول على المنفذ من متغير البيئة
PORT = int(os.environ.get('PORT', 10000))

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'service': 'Giveaway Telegram Bot',
        'description': 'بوت السحوبات على تليجرام',
        'endpoints': {
            '/': 'Home page',
            '/health': 'Health check',
            '/stats': 'Bot statistics',
            '/admin': 'Admin panel (read-only)'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'bot': 'running',
        'timestamp': os.times().user
    })

@app.route('/stats')
def stats():
    """إحصائيات البوت"""
    try:
        from config import active_giveaways
        stats_data = {
            'active_giveaways': len(active_giveaways),
            'total_participants': sum(len(g['participants']) for g in active_giveaways),
            'giveaways': []
        }
        
        for g in active_giveaways:
            stats_data['giveaways'].append({
                'id': g['id'],
                'title': g['title'],
                'participants': len(g['participants']),
                'winners': g['winners'],
                'ends_at': g['ends_at'].isoformat() if 'ends_at' in g else None
            })
        
        return jsonify(stats_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin_panel_web():
    """لوحة تحكم ويب بسيطة"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Giveaway Bot Admin</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
            .stats { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .stat-item { margin: 10px 0; font-size: 16px; }
            .btn { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
            .btn:hover { background: #45a049; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .online { background: #d4edda; color: #155724; }
            .offline { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎁 Giveaway Bot Admin Panel</h1>
            
            <div class="status online">
                ✅ <strong>Status:</strong> Bot is running
            </div>
            
            <div class="stats">
                <h3>📊 Live Statistics</h3>
                <div id="liveStats">Loading...</div>
            </div>
            
            <div>
                <h3>🔧 Quick Actions</h3>
                <a href="/stats" class="btn">View JSON Stats</a>
                <a href="/health" class="btn">Health Check</a>
                <button onclick="refreshStats()" class="btn">Refresh Stats</button>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <h3>ℹ️ Information</h3>
                <p>This is the web dashboard for the Giveaway Telegram Bot.</p>
                <p>To manage giveaways, use the bot directly on Telegram:</p>
                <ul>
                    <li><code>/newgiveaway</code> - Create new giveaway</li>
                    <li><code>/giveaways</code> - List active giveaways</li>
                    <li><code>/admin</code> - Telegram admin panel</li>
                </ul>
            </div>
        </div>
        
        <script>
            async function loadStats() {
                try {
                    const response = await fetch('/stats');
                    const data = await response.json();
                    
                    let html = `
                        <div class="stat-item">🎰 Active Giveaways: <strong>${data.active_giveaways || 0}</strong></div>
                        <div class="stat-item">👥 Total Participants: <strong>${data.total_participants || 0}</strong></div>
                    `;
                    
                    if (data.giveaways && data.giveaways.length > 0) {
                        html += '<div class="stat-item"><h4>Current Giveaways:</h4><ul>';
                        data.giveaways.forEach(g => {
                            html += `<li>${g.title} (${g.participants}/${g.winners} participants)</li>`;
                        });
                        html += '</ul></div>';
                    }# أضف في نهاية app.py
import threading
import subprocess
import sys

def run_bot():
    """تشغيل البوت في خيط منفصل"""
    try:
        print("🚀 بدء تشغيل البوت...")
        subprocess.run([sys.executable, "bot.py"])
    except Exception as e:
        print(f"❌ خطأ في البوت: {e}")

# بدء البوت في خيط منفصل
if os.environ.get('RUN_BOT', 'true').lower() == 'true':
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
                    
                    document.getElementById('liveStats').innerHTML = html;
                } catch (error) {
                    document.getElementById('liveStats').innerHTML = 'Error loading statistics';
                }
            }
            
            function refreshStats() {
                loadStats();
                alert('Statistics refreshed!');
            }
            
            // Load stats on page load and every 30 seconds
            loadStats();
            setInterval(loadStats, 30000);
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    logger.info(f"🚀 Starting web server on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
