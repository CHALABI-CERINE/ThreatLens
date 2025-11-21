"""
nlp_pipeline.py - NLP processing pipeline for ThreatLens

Functions for entity extraction, severity classification, and text summarization.
"""

import yaml
from typing import List, Dict, Set
import re


def load_config() -> Dict:
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def extract_entities(text: str) -> Dict[str, Set[str]]:
    """
    Extract named entities from text using spaCy.
    Falls back to simple pattern matching if spaCy is not available.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with entity types as keys and sets of entities as values
    """
    entities = {
        'ORG': set(),
        'PRODUCT': set(),
        'CVE': set(),
        'IP': set(),
        'HASH': set()
    }
    
    try:
        import spacy
        try:
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(text)
            
            # Extract organizations
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['ORG'].add(ent.text)
                elif ent.label_ == 'PRODUCT':
                    entities['PRODUCT'].add(ent.text)
        except (OSError, Exception):
            pass  # Fall back to pattern matching
    except ImportError:
        pass  # Fall back to pattern matching
    
    # Pattern matching for CVEs
    cve_pattern = r'CVE-\d{4}-\d{4,}'
    cves = re.findall(cve_pattern, text, re.IGNORECASE)
    entities['CVE'].update(cves)
    
    # Pattern matching for IP addresses
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = re.findall(ip_pattern, text)
    entities['IP'].update(ips)
    
    # Pattern matching for hashes (MD5, SHA1, SHA256)
    hash_patterns = [
        r'\b[a-fA-F0-9]{32}\b',  # MD5
        r'\b[a-fA-F0-9]{40}\b',  # SHA1
        r'\b[a-fA-F0-9]{64}\b',  # SHA256
    ]
    for pattern in hash_patterns:
        hashes = re.findall(pattern, text)
        entities['HASH'].update(hashes)
    
    # Convert sets to lists for JSON serialization
    return {k: list(v) for k, v in entities.items()}


def simple_severity_classify(text: str) -> str:
    """
    Classify severity of a threat based on keywords.
    
    Args:
        text: Input text (title + description)
        
    Returns:
        Severity level: 'critical', 'high', 'medium', 'low', or 'unknown'
    """
    text_lower = text.lower()
    config = load_config()
    keywords = config.get('severity_keywords', {})
    
    # Check for critical keywords first
    for keyword in keywords.get('critical', []):
        if keyword.lower() in text_lower:
            return 'critical'
    
    # Check for high severity
    for keyword in keywords.get('high', []):
        if keyword.lower() in text_lower:
            return 'high'
    
    # Check for medium severity
    for keyword in keywords.get('medium', []):
        if keyword.lower() in text_lower:
            return 'medium'
    
    # Check for low severity
    for keyword in keywords.get('low', []):
        if keyword.lower() in text_lower:
            return 'low'
    
    return 'unknown'


def summarize(text: str, max_length: int = 200) -> str:
    """
    Create a simple summary of the text.
    Uses NLTK for sentence tokenization if available, otherwise uses simple splitting.
    
    Args:
        text: Input text
        max_length: Maximum length of summary in characters
        
    Returns:
        Summary text
    """
    if not text or len(text) <= max_length:
        return text
    
    try:
        import nltk
        # Try to use NLTK for sentence tokenization
        try:
            sentences = nltk.sent_tokenize(text)
        except LookupError:
            # Download punkt if not available
            try:
                nltk.download('punkt', quiet=True)
                sentences = nltk.sent_tokenize(text)
            except (LookupError, OSError):
                # Fall back to simple splitting
                sentences = text.split('. ')
    except ImportError:
        # NLTK not available, use simple splitting
        sentences = text.split('. ')
    
    # Build summary from first sentences
    summary = ""
    for sentence in sentences:
        if len(summary) + len(sentence) <= max_length:
            summary += sentence + ". "
        else:
            break
    
    # If no sentences fit, just truncate
    if not summary:
        summary = text[:max_length] + "..."
    
    return summary.strip()


def analyze_text(item: Dict) -> Dict:
    """
    Perform full NLP analysis on an item.
    
    Args:
        item: Dictionary containing 'title' and 'description'
        
    Returns:
        Original item with added NLP fields
    """
    # Combine title and description for analysis
    full_text = f"{item.get('title', '')} {item.get('description', '')}"
    
    # Extract entities
    entities = extract_entities(full_text)
    item['entities'] = entities
    
    # Classify severity
    severity = simple_severity_classify(full_text)
    item['severity'] = severity
    
    # Create summary
    summary = summarize(item.get('description', ''), max_length=200)
    item['summary'] = summary
    
    return item


def batch_analyze(items: List[Dict]) -> List[Dict]:
    """
    Analyze a batch of items.
    
    Args:
        items: List of items to analyze
        
    Returns:
        List of analyzed items
    """
    analyzed_items = []
    for item in items:
        try:
            analyzed_item = analyze_text(item)
            analyzed_items.append(analyzed_item)
        except Exception as e:
            print(f"Error analyzing item: {e}")
            # Add with default values
            item['entities'] = {'ORG': [], 'PRODUCT': [], 'CVE': [], 'IP': [], 'HASH': []}
            item['severity'] = 'unknown'
            item['summary'] = item.get('description', '')[:200]
            analyzed_items.append(item)
    
    return analyzed_items
