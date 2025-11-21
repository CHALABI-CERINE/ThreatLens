"""
Simple alerting logic.
"""

from typing import List, Dict

def check_alerts(items: List[Dict], threshold: float) -> List[Dict]:
    alerts = []
    for it in items:
        score = it.get("score", 0)
        if score >= threshold:
            alerts.append({
                "id": it.get("id"),
                "score": score,
                "message": f"Alert: item {it.get('id')} score {score}"
            })
    return alerts
