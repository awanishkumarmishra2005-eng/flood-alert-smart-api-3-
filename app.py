from flask import Flask, jsonify, request
from models.alert import db, Alert
from services.risk_engine import calculate_risk
from services.duplicate_detector 
import detect_duplicate
import os
import uuid

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///flood_alerts.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


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
        "status": "healthy"
    })


@app.get("/api/alerts")
def get_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()

    return jsonify({
        "count": len(alerts),
        "alerts": [alert.to_dict() for alert in alerts]
    })


@app.post("/api/alerts")
def create_alert():
    data = request.get_json(silent=True) or {}

    message = data.get("message")
    location = data.get("location")

    if not message or not location:
        return jsonify({
            "error": "message and location are required"
        }), 400

    severity = data.get("severity", "CRITICAL").upper()
    water_level = data.get("water_level")
    affected_people = data.get("affected_people", 0)

    risk = calculate_risk(
        severity=severity,
        water_level=water_level,
        affected_people=affected_people,
        message=message
    )

    alert = Alert(
        id=str(uuid.uuid4()),
        message=message,
        location=location,
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        severity=severity,
        water_level=water_level,
        affected_people=affected_people,
        risk_score=risk["score"],
        risk_level=risk["level"]
    )

    db.session.add(alert)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "SOS alert created successfully",
        "alert": alert.to_dict(),
        "risk_assessment": risk
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
