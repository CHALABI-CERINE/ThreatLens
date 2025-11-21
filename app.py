"""
Minimal Flask app exposing simple endpoints for ingest, process and health.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import load_config, setup_logging
from collector import Collector
from nlp_pipeline import NLPPipeline
from alerts import check_alerts
import json

app = Flask(__name__)
CORS(app)
logger = setup_logging()

cfg = load_config()

collector = Collector(cfg.get("collector", {}).get("sources", []))
nlp = NLPPipeline(cfg.get("nlp", {}).get("model", "en_core_web_sm"))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/ingest", methods=["POST"])
def ingest():
    payload = request.json or {}
    texts = [payload.get("text")] if payload.get("text") else []
    return jsonify({"received": len(texts)}), 201

@app.route("/collect", methods=["GET"])
def collect():
    items = collector.fetch()
    return jsonify({"count": len(items), "items": items})

@app.route("/process", methods=["POST"])
def process():
    req = request.json or {}
    texts = req.get("texts", [])
    results = nlp.process(texts)
    return jsonify({"results": results})

@app.route("/alerts", methods=["POST"])
def alerts_endpoint():
    req = request.json or {}
    items = req.get("items", [])
    threshold = cfg.get("alerts", {}).get("threshold", 0.8)
    alerts = check_alerts(items, threshold)
    return jsonify({"alerts": alerts})

if __name__ == "__main__":
    app.run(host=cfg.get("app", {}).get("host", "0.0.0.0"), port=cfg.get("app", {}).get("port", 8080), debug=cfg.get("app", {}).get("debug", False))
