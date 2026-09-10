from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "system": "Smart Flood Alert & Emergency Response System",
        "status": "online",
        "message": "API is running successfully"
    })


@app.get("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
