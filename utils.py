"""
Helpers for config loading and logging.
"""

import yaml
import logging
from typing import Any, Dict

def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def setup_logging(level=logging.INFO):
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")
    return logging.getLogger("cti")
