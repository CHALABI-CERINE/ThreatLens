"""
Minimal spaCy-based NLP pipeline.
"""

import spacy
from typing import List, Dict

class NLPPipeline:
    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except Exception:
            raise RuntimeError(f"Unable to load spaCy model '{model_name}'")

    def process(self, texts: List[str]) -> List[Dict]:
        docs = list(self.nlp.pipe(texts))
        outputs = []
        for doc in docs:
            outputs.append({
                "text": doc.text,
                "ents": [{"text": ent.text, "label": ent.label_} for ent in doc.ents],
                "tokens": [t.text for t in doc[:50]]
            })
        return outputs
