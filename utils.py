"""
utils.py - Utility functions for ThreatLens

Functions for data deduplication, CSV operations, and other utilities.
"""

import pandas as pd
from typing import List, Dict
from datetime import datetime
import hashlib
import os


def deduplicate_items(items: List[Dict], key_fields: List[str] = None) -> List[Dict]:
    """
    Deduplicate items based on key fields.
    
    Args:
        items: List of item dictionaries
        key_fields: List of fields to use for deduplication (default: ['title', 'link'])
        
    Returns:
        Deduplicated list of items
    """
    if key_fields is None:
        key_fields = ['title', 'link']
    
    seen = set()
    unique_items = []
    
    for item in items:
        # Create a hash based on key fields
        key_values = tuple(str(item.get(field, '')) for field in key_fields)
        item_hash = hashlib.md5(str(key_values).encode()).hexdigest()
        
        if item_hash not in seen:
            seen.add(item_hash)
            unique_items.append(item)
    
    return unique_items


def save_items_csv(items: List[Dict], filepath: str = 'data/items.csv') -> None:
    """
    Save items to a CSV file.
    
    Args:
        items: List of item dictionaries
        filepath: Path to save the CSV file
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if not items:
        print("No items to save")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(items)
    
    # Convert datetime objects to strings
    for col in df.columns:
        if df[col].dtype == 'object' and len(df) > 0:
            # Check if it's a datetime column
            try:
                if isinstance(df[col].iloc[0], datetime):
                    df[col] = df[col].apply(lambda x: x.isoformat() if isinstance(x, datetime) else x)
            except (IndexError, AttributeError):
                pass
    
    # Convert complex types (lists, dicts) to strings
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, (dict, list)) else x)
    
    # Save to CSV
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"Saved {len(items)} items to {filepath}")


def load_items_csv(filepath: str = 'data/items.csv') -> List[Dict]:
    """
    Load items from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of item dictionaries
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        
        # Convert published column back to datetime
        if 'published' in df.columns:
            df['published'] = pd.to_datetime(df['published'], errors='coerce')
        
        # Convert string representations of dicts/lists back
        import ast
        for col in ['entities']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('{') else x)
        
        items = df.to_dict('records')
        print(f"Loaded {len(items)} items from {filepath}")
        return items
    except Exception as e:
        print(f"Error loading items from {filepath}: {e}")
        return []


def merge_and_deduplicate(old_items: List[Dict], new_items: List[Dict]) -> List[Dict]:
    """
    Merge old and new items, removing duplicates.
    
    Args:
        old_items: Existing items
        new_items: New items to add
        
    Returns:
        Merged and deduplicated list
    """
    all_items = old_items + new_items
    return deduplicate_items(all_items)


def filter_items_by_date(items: List[Dict], start_date: datetime = None, 
                        end_date: datetime = None) -> List[Dict]:
    """
    Filter items by date range.
    
    Args:
        items: List of items
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
        
    Returns:
        Filtered list of items
    """
    filtered = []
    
    for item in items:
        published = item.get('published')
        
        if not published:
            continue
        
        # Convert to datetime if string
        if isinstance(published, str):
            try:
                from dateutil import parser
                published = parser.parse(published)
            except (ValueError, TypeError):
                continue
        
        # Apply filters
        if start_date and published < start_date:
            continue
        if end_date and published > end_date:
            continue
        
        filtered.append(item)
    
    return filtered


def filter_items_by_severity(items: List[Dict], severities: List[str]) -> List[Dict]:
    """
    Filter items by severity levels.
    
    Args:
        items: List of items
        severities: List of severity levels to include
        
    Returns:
        Filtered list of items
    """
    if not severities:
        return items
    
    severities_lower = [s.lower() for s in severities]
    return [item for item in items if item.get('severity', '').lower() in severities_lower]


def search_items(items: List[Dict], query: str) -> List[Dict]:
    """
    Search items by text query in title and description.
    
    Args:
        items: List of items
        query: Search query (case-insensitive)
        
    Returns:
        Filtered list of items matching the query
    """
    if not query:
        return items
    
    query_lower = query.lower()
    results = []
    
    for item in items:
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        if query_lower in text:
            results.append(item)
    
    return results


def get_summary_statistics(items: List[Dict]) -> Dict:
    """
    Calculate summary statistics for items.
    
    Args:
        items: List of items
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        'total_items': len(items),
        'by_severity': {},
        'by_source': {},
        'by_type': {},
        'date_range': None
    }
    
    if not items:
        return stats
    
    # Count by severity
    for item in items:
        severity = item.get('severity', 'unknown')
        stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
        
        source = item.get('source', 'unknown')
        stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
        
        item_type = item.get('type', 'unknown')
        stats['by_type'][item_type] = stats['by_type'].get(item_type, 0) + 1
    
    # Get date range
    dates = [item.get('published') for item in items if item.get('published')]
    if dates:
        # Convert strings to datetime if needed
        datetime_dates = []
        for d in dates:
            if isinstance(d, str):
                try:
                    from dateutil import parser
                    datetime_dates.append(parser.parse(d))
                except (ValueError, TypeError):
                    pass
            elif isinstance(d, datetime):
                datetime_dates.append(d)
        
        if datetime_dates:
            stats['date_range'] = {
                'earliest': min(datetime_dates),
                'latest': max(datetime_dates)
            }
    
    return stats
