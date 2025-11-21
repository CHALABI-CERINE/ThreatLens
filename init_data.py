"""
Create sample data in data/sample.json
"""

import os
import json

DATA_DIR = "data"
SAMPLE_PATH = os.path.join(DATA_DIR, "sample.json")

SAMPLE = [
    {"id": "1", "text": "This is a test message", "score": 0.5},
    {"id": "2", "text": "Critical error occurred in system", "score": 0.95}
]

def init():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SAMPLE_PATH, "w", encoding="utf-8") as f:
        json.dump(SAMPLE, f, ensure_ascii=False, indent=2)
    print(f"Initial data written to {SAMPLE_PATH}")

if __name__ == "__main__":
    init()
