# Cyber Threat Intelligence Dashboard

A lightweight framework for collecting threat data, running an NLP pipeline, generating alerts and exposing a small API and dashboard.

Structure
- README.md — this file
- requirements.txt — Python dependencies
- .gitignore — files to ignore
- config.yaml — runtime configuration
- collector.py — data collector
- nlp_pipeline.py — NLP processing
- alerts.py — alerting rules
- utils.py — helpers (config, logging)
- init_data.py — create sample data
- app.py — Flask API
- Dockerfile — Docker image
- docker-compose.yml — compose configuration

Quickstart (local)
1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. python init_data.py
5. python app.py

Docker
- docker-compose up --build

License: Add one as appropriate.