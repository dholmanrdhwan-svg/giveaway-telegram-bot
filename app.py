import os
from flask import Flask, jsonify

app = Flask(__name__)
PORT = int(os.environ.get('PORT', 5000))

@app.route('/')
def home():
    return jsonify({"status": "ok", "port": PORT})

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
