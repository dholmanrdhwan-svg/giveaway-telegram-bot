from flask import Flask, jsonify
import os

app = Flask(__name__)
PORT = int(os.environ.get('PORT', 5000))

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Giveaway Bot Dashboard",
        "endpoints": {
            "/": "Home",
            "/health": "Health check",
            "/stats": "Bot statistics"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/stats')
def stats():
    # إحصائيات البوت (يمكن تطويرها)
    return jsonify({
        "active_giveaways": 0,
        "total_participants": 0,
        "status": "bot_running"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
