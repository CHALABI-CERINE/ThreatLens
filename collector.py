"""
collector.py - Data collection functions for ThreatLens

Functions to fetch threat intelligence data from RSS feeds and CVE APIs.
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser as date_parser
import yaml
from typing import List, Dict, Optional
import time


def load_config() -> Dict:
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def fetch_rss(url: str, source_name: str = "RSS Feed") -> List[Dict]:
    """
    Fetch items from an RSS feed.
    
    Args:
        url: RSS feed URL
        source_name: Name of the source for identification
        
    Returns:
        List of dictionaries containing feed items
    """
    items = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Extract published date
            published = None
            if hasattr(entry, 'published'):
                try:
                    published = date_parser.parse(entry.published)
                except (ValueError, TypeError):
                    published = datetime.now()
            elif hasattr(entry, 'updated'):
                try:
                    published = date_parser.parse(entry.updated)
                except (ValueError, TypeError):
                    published = datetime.now()
            else:
                published = datetime.now()
            
            # Extract description/summary
            description = ""
            if hasattr(entry, 'summary'):
                description = entry.summary
            elif hasattr(entry, 'description'):
                description = entry.description
            
            # Clean HTML from description
            soup = BeautifulSoup(description, 'html.parser')
            description = soup.get_text(strip=True)
            
            item = {
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', ''),
                'description': description,
                'published': published,
                'source': source_name,
                'type': 'rss'
            }
            items.append(item)
    except Exception as e:
        print(f"Error fetching RSS from {url}: {e}")
    
    return items


def fetch_latest_cves_from_circl(max_results: int = 50) -> List[Dict]:
    """
    Fetch latest CVEs from CIRCL API.
    
    Args:
        max_results: Maximum number of CVEs to fetch
        
    Returns:
        List of dictionaries containing CVE information
    """
    items = []
    config = load_config()
    circl_url = config.get('cve_api', {}).get('circl_url', 'https://cve.circl.lu/api/last')
    
    try:
        response = requests.get(circl_url, timeout=10)
        response.raise_for_status()
        cves = response.json()
        
        for cve in cves[:max_results]:
            cve_id = cve.get('id', 'Unknown')
            summary = cve.get('summary', 'No summary available')
            published = cve.get('Published', '')
            
            # Parse published date
            try:
                published_date = datetime.strptime(published, '%Y-%m-%dT%H:%M:%S')
            except (ValueError, TypeError):
                published_date = datetime.now()
            
            # Get CVSS score if available
            cvss = cve.get('cvss', 0.0)
            
            item = {
                'title': cve_id,
                'link': f"https://cve.circl.lu/cve/{cve_id}",
                'description': summary,
                'published': published_date,
                'source': 'CIRCL CVE',
                'type': 'cve',
                'cvss': cvss
            }
            items.append(item)
    except Exception as e:
        print(f"Error fetching CVEs from CIRCL: {e}")
    
    return items


def fetch_article_text(url: str, max_length: int = 5000) -> str:
    """
    Fetch full article text from a URL.
    
    Args:
        url: Article URL
        max_length: Maximum length of text to return
        
    Returns:
        Extracted article text
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            script.decompose()
        
        # Get text from article or main content
        article = soup.find('article') or soup.find('main') or soup.find('body')
        if article:
            text = article.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
        
        # Limit length
        return text[:max_length]
    except Exception as e:
        print(f"Error fetching article text from {url}: {e}")
        return ""


def collect_all_sources() -> List[Dict]:
    """
    Collect data from all configured sources.
    
    Returns:
        List of all collected items
    """
    all_items = []
    config = load_config()
    
    # Fetch from RSS sources
    rss_sources = config.get('rss_sources', [])
    for source in rss_sources:
        print(f"Fetching from {source['name']}...")
        items = fetch_rss(source['url'], source['name'])
        all_items.extend(items)
        time.sleep(1)  # Be polite with rate limiting
    
    # Fetch from CVE API
    print("Fetching CVEs from CIRCL...")
    max_cves = config.get('cve_api', {}).get('max_cves', 50)
    cve_items = fetch_latest_cves_from_circl(max_cves)
    all_items.extend(cve_items)
    
    return all_items
