# ThreatLens - Streamlit POC

ThreatLens est un dashboard Streamlit pour la veille de menaces cyber (Cyber Threat Intelligence).

## Description

Ce POC (Proof of Concept) permet de :
- Collecter des informations de menaces depuis des flux RSS et l'API CVE CIRCL
- Analyser et classifier automatiquement les menaces par NLP (spaCy, NLTK)
- Afficher un dashboard interactif avec filtres et visualisations
- Générer des alertes basées sur des mots-clés de sévérité
- Exporter les données en CSV

## Prérequis

- Python 3.8+
- pip

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/CHALABI-CERINE/ThreatLens.git
cd ThreatLens
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger le modèle spaCy (optionnel mais recommandé)

```bash
python -m spacy download en_core_web_sm
```

### 5. Initialiser les données de démonstration

```bash
python init_data.py
```

Ce script va collecter des données initiales depuis les sources configurées et les sauvegarder dans `data/items.csv`.

## Lancement de l'application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## Utilisation avec Docker

### Construire l'image

```bash
docker-compose build
```

### Lancer le conteneur

```bash
docker-compose up
```

L'application sera accessible à l'adresse : http://localhost:8501

## Structure du projet

- `app.py` : Application Streamlit principale
- `collector.py` : Fonctions de collecte de données (RSS, CVE API)
- `nlp_pipeline.py` : Pipeline d'analyse NLP (extraction d'entités, classification de sévérité, résumé)
- `alerts.py` : Génération d'alertes basées sur des mots-clés
- `utils.py` : Fonctions utilitaires (déduplication, sauvegarde/chargement CSV)
- `init_data.py` : Script d'initialisation des données
- `config.yaml` : Configuration des sources RSS, API CVE et mots-clés de sévérité
- `requirements.txt` : Dépendances Python
- `Dockerfile` : Configuration Docker
- `docker-compose.yml` : Orchestration Docker

## Configuration

Le fichier `config.yaml` contient :
- Les sources RSS à surveiller
- L'URL de l'API CVE (CIRCL)
- Les mots-clés de sévérité pour la classification automatique

Vous pouvez modifier ce fichier pour ajouter vos propres sources et mots-clés.

## Fonctionnalités

1. **Collection de données** : Collecte automatique depuis RSS et API CVE
2. **Analyse NLP** : Extraction d'entités, classification de sévérité, résumé
3. **Dashboard interactif** : Filtres par date, sévérité, recherche textuelle
4. **Visualisations** : Graphiques de distribution de sévérité avec Altair
5. **Alertes** : Détection automatique de menaces critiques
6. **Export** : Export des données filtrées en CSV

## Licence

MIT
