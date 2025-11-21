#!/usr/bin/env python3
"""
app.py - Main Streamlit application for ThreatLens

A dashboard for cyber threat intelligence with collection, analysis, and visualization.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collector import collect_all_sources
from nlp_pipeline import batch_analyze
from alerts import generate_alerts, format_alert_message, get_alert_statistics
from utils import (deduplicate_items, save_items_csv, load_items_csv,
                   filter_items_by_date, filter_items_by_severity, 
                   search_items, get_summary_statistics, merge_and_deduplicate)


# Page configuration
st.set_page_config(
    page_title="ThreatLens - Cyber Threat Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.severity-critical { color: #ff4b4b; font-weight: bold; }
.severity-high { color: #ffa500; font-weight: bold; }
.severity-medium { color: #ffeb3b; font-weight: bold; }
.severity-low { color: #4caf50; font-weight: bold; }
.severity-unknown { color: #9e9e9e; }
.metric-card { 
    padding: 20px; 
    border-radius: 10px; 
    background-color: #f0f2f6;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


def load_data():
    """Load data from CSV file"""
    return load_items_csv('data/items.csv')


def collect_new_data():
    """Collect new data from sources"""
    with st.spinner('Collecting data from sources...'):
        new_items = collect_all_sources()
    
    with st.spinner('Analyzing with NLP...'):
        analyzed_items = batch_analyze(new_items)
    
    # Load existing data and merge
    existing_items = load_data()
    all_items = merge_and_deduplicate(existing_items, analyzed_items)
    
    # Save merged data
    save_items_csv(all_items, 'data/items.csv')
    
    return all_items, len(analyzed_items)


def main():
    """Main application"""
    
    # Title and description
    st.title("🔍 ThreatLens")
    st.markdown("### Cyber Threat Intelligence Dashboard")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data collection
        st.subheader("Data Collection")
        if st.button("🔄 Collect New Data", use_container_width=True):
            all_items, new_count = collect_new_data()
            st.success(f"✓ Collected {new_count} new items!")
            st.rerun()
        
        st.markdown("---")
        
        # Filters
        st.subheader("📊 Filters")
        
        # Date range filter
        date_option = st.selectbox(
            "Date Range",
            ["All Time", "Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom"]
        )
        
        start_date = None
        end_date = None
        
        if date_option == "Last 24 Hours":
            start_date = datetime.now() - timedelta(days=1)
        elif date_option == "Last 7 Days":
            start_date = datetime.now() - timedelta(days=7)
        elif date_option == "Last 30 Days":
            start_date = datetime.now() - timedelta(days=30)
        elif date_option == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("From", value=datetime.now() - timedelta(days=7))
                start_date = datetime.combine(start_date, datetime.min.time())
            with col2:
                end_date = st.date_input("To", value=datetime.now())
                end_date = datetime.combine(end_date, datetime.max.time())
        
        # Severity filter
        severity_options = st.multiselect(
            "Severity",
            ["Critical", "High", "Medium", "Low", "Unknown"],
            default=["Critical", "High", "Medium", "Low", "Unknown"]
        )
        
        # Search box
        search_query = st.text_input("🔍 Search", placeholder="Search in title and description...")
        
        st.markdown("---")
        
        # Export
        st.subheader("📥 Export")
    
    # Load data
    if not os.path.exists('data/items.csv'):
        st.warning("⚠️ No data found. Please run `python init_data.py` first or click 'Collect New Data'.")
        if st.button("Initialize Data Now"):
            all_items, new_count = collect_new_data()
            st.success(f"✓ Initialized with {new_count} items!")
            st.rerun()
        return
    
    items = load_data()
    
    if not items:
        st.warning("⚠️ No data available. Click 'Collect New Data' to fetch threat intelligence.")
        return
    
    # Apply filters
    filtered_items = items.copy()
    
    # Date filter
    if start_date or end_date:
        filtered_items = filter_items_by_date(filtered_items, start_date, end_date)
    
    # Severity filter
    if severity_options:
        filtered_items = filter_items_by_severity(filtered_items, severity_options)
    
    # Search filter
    if search_query:
        filtered_items = search_items(filtered_items, search_query)
    
    # Statistics
    stats = get_summary_statistics(filtered_items)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Threats", stats['total_items'])
    
    with col2:
        critical_count = stats['by_severity'].get('critical', 0)
        st.metric("Critical", critical_count, delta=None if critical_count == 0 else "High Priority")
    
    with col3:
        high_count = stats['by_severity'].get('high', 0)
        st.metric("High Severity", high_count)
    
    with col4:
        sources_count = len(stats['by_source'])
        st.metric("Sources", sources_count)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Threats", "🚨 Alerts", "📊 Analytics", "ℹ️ About"])
    
    with tab1:
        st.subheader("Threat Intelligence Items")
        
        if not filtered_items:
            st.info("No items match the current filters.")
        else:
            # Display items
            for item in filtered_items[:50]:  # Limit to 50 items for performance
                severity = item.get('severity', 'unknown')
                severity_class = f"severity-{severity}"
                
                with st.expander(f"{item.get('title', 'No Title')} - {item.get('source', 'Unknown')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Severity:** <span class='{severity_class}'>{severity.upper()}</span>", 
                                  unsafe_allow_html=True)
                        st.markdown(f"**Source:** {item.get('source', 'Unknown')}")
                        st.markdown(f"**Type:** {item.get('type', 'unknown')}")
                        
                        published = item.get('published')
                        if published:
                            if isinstance(published, str):
                                from dateutil import parser
                                try:
                                    published = parser.parse(published)
                                except:
                                    pass
                            if isinstance(published, datetime):
                                st.markdown(f"**Published:** {published.strftime('%Y-%m-%d %H:%M')}")
                    
                    with col2:
                        if item.get('link'):
                            st.link_button("🔗 View Source", item['link'], use_container_width=True)
                    
                    st.markdown(f"**Description:**")
                    st.write(item.get('summary', item.get('description', 'No description available')))
                    
                    # Show entities
                    entities = item.get('entities', {})
                    if any(entities.values()):
                        st.markdown("**Entities:**")
                        for entity_type, entity_list in entities.items():
                            if entity_list and entity_list != ['']:
                                st.write(f"- **{entity_type}:** {', '.join(str(e) for e in entity_list[:5])}")
            
            if len(filtered_items) > 50:
                st.info(f"Showing 50 of {len(filtered_items)} items. Use filters to narrow down results.")
    
    with tab2:
        st.subheader("Security Alerts")
        
        # Generate alerts
        alerts = generate_alerts(filtered_items, severity_threshold='medium', days_back=30)
        
        if not alerts:
            st.info("No alerts generated for the current filters.")
        else:
            st.success(f"Found {len(alerts)} alerts")
            
            # Alert statistics
            alert_stats = get_alert_statistics(alerts)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Critical Alerts", alert_stats['by_severity'].get('critical', 0))
            with col2:
                st.metric("High Alerts", alert_stats['by_severity'].get('high', 0))
            with col3:
                st.metric("Medium Alerts", alert_stats['by_severity'].get('medium', 0))
            
            st.markdown("---")
            
            # Display alerts
            for alert in alerts[:20]:  # Limit to 20 alerts
                message = format_alert_message(alert)
                st.markdown(message)
                st.markdown("---")
            
            if len(alerts) > 20:
                st.info(f"Showing 20 of {len(alerts)} alerts.")
    
    with tab3:
        st.subheader("Analytics & Visualizations")
        
        if not filtered_items:
            st.info("No data available for analytics.")
        else:
            # Severity distribution chart
            st.markdown("#### Severity Distribution")
            
            severity_data = pd.DataFrame([
                {'Severity': k.capitalize(), 'Count': v}
                for k, v in stats['by_severity'].items()
            ])
            
            if not severity_data.empty:
                chart = alt.Chart(severity_data).mark_bar().encode(
                    x=alt.X('Severity:N', sort=['Critical', 'High', 'Medium', 'Low', 'Unknown']),
                    y='Count:Q',
                    color=alt.Color('Severity:N', 
                                   scale=alt.Scale(
                                       domain=['Critical', 'High', 'Medium', 'Low', 'Unknown'],
                                       range=['#ff4b4b', '#ffa500', '#ffeb3b', '#4caf50', '#9e9e9e']
                                   ))
                ).properties(height=400)
                
                st.altair_chart(chart, use_container_width=True)
            
            # Source distribution
            st.markdown("#### Top Sources")
            
            source_data = pd.DataFrame([
                {'Source': k, 'Count': v}
                for k, v in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True)[:10]
            ])
            
            if not source_data.empty:
                chart = alt.Chart(source_data).mark_bar().encode(
                    y=alt.Y('Source:N', sort='-x'),
                    x='Count:Q',
                    color=alt.value('#1f77b4')
                ).properties(height=400)
                
                st.altair_chart(chart, use_container_width=True)
            
            # Timeline
            if stats.get('date_range'):
                st.markdown("#### Timeline")
                
                # Create timeline data
                timeline_items = [item for item in filtered_items if item.get('published')]
                timeline_df = pd.DataFrame([
                    {
                        'Date': item['published'] if isinstance(item['published'], datetime) 
                               else pd.to_datetime(item['published']),
                        'Severity': item.get('severity', 'unknown').capitalize()
                    }
                    for item in timeline_items
                ])
                
                if not timeline_df.empty:
                    timeline_df['Date'] = pd.to_datetime(timeline_df['Date']).dt.date
                    timeline_agg = timeline_df.groupby(['Date', 'Severity']).size().reset_index(name='Count')
                    
                    chart = alt.Chart(timeline_agg).mark_line(point=True).encode(
                        x='Date:T',
                        y='Count:Q',
                        color=alt.Color('Severity:N',
                                       scale=alt.Scale(
                                           domain=['Critical', 'High', 'Medium', 'Low', 'Unknown'],
                                           range=['#ff4b4b', '#ffa500', '#ffeb3b', '#4caf50', '#9e9e9e']
                                       ))
                    ).properties(height=400)
                    
                    st.altair_chart(chart, use_container_width=True)
    
    with tab4:
        st.subheader("About ThreatLens")
        
        st.markdown("""
        **ThreatLens** is a proof-of-concept (POC) dashboard for cyber threat intelligence.
        
        #### Features:
        - 📡 **Data Collection**: Automatically collects threat intelligence from RSS feeds and CVE APIs
        - 🤖 **NLP Analysis**: Uses spaCy and NLTK for entity extraction and severity classification
        - 🔍 **Filtering**: Advanced filtering by date, severity, and text search
        - 📊 **Visualizations**: Interactive charts with Altair
        - 🚨 **Alerts**: Automatic alert generation for critical threats
        - 📥 **Export**: Export filtered data to CSV
        
        #### Technologies:
        - **Streamlit**: Web application framework
        - **spaCy**: Natural language processing
        - **NLTK**: Text processing
        - **Pandas**: Data manipulation
        - **Altair**: Visualization
        - **BeautifulSoup**: Web scraping
        - **Feedparser**: RSS parsing
        
        #### Data Sources:
        - RSS feeds from major cybersecurity news sites
        - CVE data from CIRCL API
        
        #### Configuration:
        Edit `config.yaml` to customize data sources and severity keywords.
        """)
    
    # Export functionality in sidebar
    with st.sidebar:
        if st.button("📥 Export Filtered Data", use_container_width=True):
            if filtered_items:
                df = pd.DataFrame(filtered_items)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"threatlens_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No data to export")


if __name__ == '__main__':
    main()
