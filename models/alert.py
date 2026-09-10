from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Alert(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    severity = db.Column(db.String(20), nullable=False, default="HIGH")
    status = db.Column(db.String(20), nullable=False, default="ACTIVE")
    water_level = db.Column(db.String(50), nullable=True)
    affected_people = db.Column(db.Integer, nullable=False, default=0)
    risk_score = db.Column(db.Integer, nullable=True)
    risk_level = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "severity": self.severity,
            "status": self.status,
            "water_level": self.water_level,
            "affected_people": self.affected_people,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }
