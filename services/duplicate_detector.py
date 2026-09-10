from datetime import datetime, timedelta
from difflib import SequenceMatcher


def text_similarity(text1, text2):
    return SequenceMatcher(
        None,
        text1.lower().strip(),
        text2.lower().strip()
    ).ratio()


def detect_duplicate(
    message,
    location,
    severity,
    existing_alerts
):
    now = datetime.utcnow()

    for alert in existing_alerts:
        if not alert.created_at:
            continue

        # Only compare recent alerts
        if now - alert.created_at > timedelta(hours=24):
            continue

        # Location should match closely
        location_match = (
            location.lower().strip()
            == alert.location.lower().strip()
        )

        # Compare message similarity
        similarity = text_similarity(
            message,
            alert.message
        )

        # Same location + similar message = possible duplicate
        if location_match and similarity >= 0.70:
            return {
                "is_duplicate": True,
                "duplicate_of": alert.id,
                "confidence": round(similarity * 100),
                "reason": "Recent alert from the same location has a similar report."
            }

    return {
        "is_duplicate": False,
        "duplicate_of": None,
        "confidence": 0,
        "reason": None
    }
