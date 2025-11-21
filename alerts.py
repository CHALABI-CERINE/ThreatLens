"""
alerts.py - Alert generation for ThreatLens

Functions to generate alerts based on severity and keywords.
"""

from typing import List, Dict
from datetime import datetime, timedelta


def generate_alerts(items: List[Dict], severity_threshold: str = 'high', 
                   days_back: int = 7) -> List[Dict]:
    """
    Generate alerts from items based on severity and recency.
    
    Args:
        items: List of analyzed items with severity classification
        severity_threshold: Minimum severity level to generate alerts
                          ('critical', 'high', 'medium', 'low')
        days_back: Only consider items from the last N days
        
    Returns:
        List of alert dictionaries
    """
    # Define severity levels (higher number = more severe)
    severity_levels = {
        'critical': 4,
        'high': 3,
        'medium': 2,
        'low': 1,
        'unknown': 0
    }
    
    threshold_level = severity_levels.get(severity_threshold, 3)
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    alerts = []
    
    for item in items:
        # Check severity
        item_severity = item.get('severity', 'unknown')
        item_level = severity_levels.get(item_severity, 0)
        
        if item_level < threshold_level:
            continue
        
        # Check date
        published = item.get('published')
        if published:
            if isinstance(published, str):
                try:
                    from dateutil import parser
                    published = parser.parse(published)
                except:
                    published = datetime.now()
            
            if published < cutoff_date:
                continue
        
        # Create alert
        alert = {
            'id': f"alert_{len(alerts) + 1}",
            'title': item.get('title', 'Unknown'),
            'description': item.get('summary', item.get('description', '')),
            'severity': item_severity,
            'source': item.get('source', 'Unknown'),
            'link': item.get('link', ''),
            'published': published,
            'entities': item.get('entities', {}),
            'type': item.get('type', 'unknown')
        }
        
        alerts.append(alert)
    
    # Sort by severity (critical first) then by date (newest first)
    alerts.sort(key=lambda x: (
        -severity_levels.get(x['severity'], 0),
        -(x['published'].timestamp() if x['published'] else 0)
    ))
    
    return alerts


def filter_alerts_by_keywords(alerts: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Filter alerts by keywords in title or description.
    
    Args:
        alerts: List of alert dictionaries
        keywords: List of keywords to search for (case-insensitive)
        
    Returns:
        Filtered list of alerts
    """
    if not keywords:
        return alerts
    
    filtered = []
    for alert in alerts:
        text = f"{alert.get('title', '')} {alert.get('description', '')}".lower()
        
        for keyword in keywords:
            if keyword.lower() in text:
                filtered.append(alert)
                break
    
    return filtered


def get_alert_statistics(alerts: List[Dict]) -> Dict:
    """
    Calculate statistics about alerts.
    
    Args:
        alerts: List of alert dictionaries
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        'total': len(alerts),
        'by_severity': {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'unknown': 0
        },
        'by_type': {},
        'by_source': {}
    }
    
    for alert in alerts:
        # Count by severity
        severity = alert.get('severity', 'unknown')
        stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
        
        # Count by type
        alert_type = alert.get('type', 'unknown')
        stats['by_type'][alert_type] = stats['by_type'].get(alert_type, 0) + 1
        
        # Count by source
        source = alert.get('source', 'unknown')
        stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
    
    return stats


def format_alert_message(alert: Dict) -> str:
    """
    Format an alert as a text message.
    
    Args:
        alert: Alert dictionary
        
    Returns:
        Formatted alert message
    """
    severity_emoji = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢',
        'unknown': '⚪'
    }
    
    emoji = severity_emoji.get(alert.get('severity', 'unknown'), '⚪')
    
    message = f"{emoji} **{alert.get('severity', 'unknown').upper()}** - {alert.get('title', 'Unknown')}\n\n"
    message += f"**Source:** {alert.get('source', 'Unknown')}\n"
    
    if alert.get('published'):
        published = alert['published']
        if isinstance(published, datetime):
            message += f"**Published:** {published.strftime('%Y-%m-%d %H:%M')}\n"
    
    message += f"\n{alert.get('description', 'No description available')}\n"
    
    if alert.get('link'):
        message += f"\n[Read more]({alert['link']})"
    
    # Add entities if available
    entities = alert.get('entities', {})
    if any(entities.values()):
        message += "\n\n**Entities detected:**\n"
        for entity_type, entity_list in entities.items():
            if entity_list:
                message += f"- **{entity_type}:** {', '.join(entity_list[:5])}\n"
    
    return message
