"""
Collector: fetch data from configured sources.
"""

import requests
from typing import List, Dict

class Collector:
    def __init__(self, sources: List[Dict]):
        self.sources = sources

    def fetch(self) -> List[Dict]:
        """Fetch items from all configured sources and return a list of objects."""
        results = []
        for src in self.sources:
            try:
                resp = requests.get(src.get("url"), timeout=10)
                resp.raise_for_status()
                data = resp.json()
                if isinstance(data, list):
                    results.extend(data)
                else:
                    results.append(data)
            except Exception as e:
                print(f"Collector error for {src.get('name')}: {e}")
        return results
