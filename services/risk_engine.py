def calculate_risk(
    severity,
    water_level=None,
    affected_people=0,
    message=""
):
    score = 0
    factors = []

    severity = (severity or "HIGH").upper()
    water_level = (water_level or "").upper()
    message = (message or "").lower()

    # Severity
    severity_scores = {
        "LOW": 10,
        "MEDIUM": 25,
        "HIGH": 40,
        "CRITICAL": 55
    }

    score += severity_scores.get(severity, 40)
    factors.append(f"Reported severity: {severity}")

    # Water level
    if water_level in ["DANGEROUS", "VERY HIGH"]:
        score += 25
        factors.append("Dangerously high water level")
    elif water_level in ["HIGH"]:
        score += 15
        factors.append("High water level")
    elif water_level in ["MEDIUM"]:
        score += 8
        factors.append("Moderate water level")

    # Affected people
    try:
        people = int(affected_people or 0)
    except (TypeError, ValueError):
        people = 0

    if people >= 100:
        score += 20
        factors.append("Large number of people affected")
    elif people >= 25:
        score += 12
        factors.append("Significant number of people affected")
    elif people > 0:
        score += 5
        factors.append("People reported as affected")

    # Emergency keywords
    emergency_words = [
        "trapped",
        "rescue",
        "danger",
        "drowning",
        "stranded",
        "evacuate",
        "collapsed",
        "urgent"
    ]

    detected = [
        word for word in emergency_words
        if word in message
    ]

    if detected:
        score += min(len(detected) * 5, 15)
        factors.append(
            "Emergency indicators: " + ", ".join(detected)
        )

    score = min(score, 100)

    if score >= 75:
        risk_level = "CRITICAL"
        recommendation = "Immediate emergency response recommended."
    elif score >= 50:
        risk_level = "HIGH"
        recommendation = "Prioritize this alert for rapid response."
    elif score >= 25:
        risk_level = "MEDIUM"
        recommendation = "Monitor and assess the situation."
    else:
        risk_level = "LOW"
        recommendation = "Continue monitoring."

    return {
        "score": score,
        "level": risk_level,
        "factors": factors,
        "recommendation": recommendation
    }
