#!/usr/bin/env python3
"""
init_data.py - Initialize sample data for ThreatLens

This script fetches sample data from configured sources and saves it to data/items.csv
"""

import os
import sys
from tqdm import tqdm

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collector import collect_all_sources
from nlp_pipeline import batch_analyze
from utils import deduplicate_items, save_items_csv


def main():
    """Main function to initialize sample data"""
    print("=" * 60)
    print("ThreatLens - Data Initialization")
    print("=" * 60)
    print()
    
    # Step 1: Collect data from all sources
    print("Step 1: Collecting data from sources...")
    print("-" * 60)
    items = collect_all_sources()
    print(f"✓ Collected {len(items)} items")
    print()
    
    # Step 2: Deduplicate items
    print("Step 2: Deduplicating items...")
    print("-" * 60)
    unique_items = deduplicate_items(items)
    print(f"✓ {len(unique_items)} unique items (removed {len(items) - len(unique_items)} duplicates)")
    print()
    
    # Step 3: Analyze with NLP
    print("Step 3: Analyzing items with NLP...")
    print("-" * 60)
    analyzed_items = []
    for item in tqdm(unique_items, desc="Analyzing"):
        try:
            from nlp_pipeline import analyze_text
            analyzed_item = analyze_text(item)
            analyzed_items.append(analyzed_item)
        except Exception as e:
            print(f"Error analyzing item: {e}")
            # Add with defaults
            item['severity'] = 'unknown'
            item['entities'] = {'ORG': [], 'PRODUCT': [], 'CVE': [], 'IP': [], 'HASH': []}
            item['summary'] = item.get('description', '')[:200]
            analyzed_items.append(item)
    
    print(f"✓ Analyzed {len(analyzed_items)} items")
    print()
    
    # Step 4: Save to CSV
    print("Step 4: Saving data to CSV...")
    print("-" * 60)
    save_items_csv(analyzed_items, 'data/items.csv')
    print()
    
    # Display summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    from utils import get_summary_statistics
    stats = get_summary_statistics(analyzed_items)
    
    print(f"Total items: {stats['total_items']}")
    print()
    
    print("By Severity:")
    for severity, count in sorted(stats['by_severity'].items(), 
                                  key=lambda x: {'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'unknown': 0}.get(x[0], 0),
                                  reverse=True):
        print(f"  {severity.capitalize()}: {count}")
    print()
    
    print("By Source:")
    for source, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count}")
    print()
    
    if stats['date_range']:
        print("Date Range:")
        print(f"  Earliest: {stats['date_range']['earliest'].strftime('%Y-%m-%d %H:%M')}")
        print(f"  Latest: {stats['date_range']['latest'].strftime('%Y-%m-%d %H:%M')}")
        print()
    
    print("=" * 60)
    print("✓ Initialization complete!")
    print()
    print("Next steps:")
    print("  1. Run the Streamlit app: streamlit run app.py")
    print("  2. Access the dashboard at http://localhost:8501")
    print("=" * 60)


if __name__ == '__main__':
    main()
