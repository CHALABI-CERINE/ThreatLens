# ThreatLens
# ThreatLens: A Big Data–Powered Cyber Threat Intelligence Dashboard

## Description

Utiliser le Big Data pour surveiller les menaces cybersécurité en temps réel, en collectant et analysant automatiquement des flux d’information (CVE, blogs, réseaux sociaux) grâce au traitement du langage naturel. L’outil permet d’identifier les attaques émergentes, de classifier les menaces par gravité, et de générer des alertes ou des rapports synthétiques via une interface interactive.

## Présentation du projet

Développer un outil pour automatiser la veille sur les menaces cybersécurité. Cet outil permet non seulement de comprendre les enjeux liés à la cybersécurité moderne, mais aussi d’acquérir des compétences techniques en collecte, traitement et visualisation de données à grande échelle. Il s’inscrit dans une démarche de veille technologique appliquée au domaine de la sécurité informatique.

## Implémentation des fonctionnalités

L’implémentation se fera de manière modulaire, en intégrant progressivement les composants techniques nécessaires à la veille automatisée :

-   **Collecte des données :** utilisation de bibliothèques comme Scrapy, BeautifulSoup ou des API spécialisées pour extraire des informations depuis des flux RSS, des bases CVE, des blogs techniques ou des réseaux sociaux.
-   **Filtrage et classification :** application de modèles de traitement du langage naturel (spaCy, NLTK) pour identifier les mots-clés, classer les menaces par type, gravité ou cible, et éliminer les doublons ou les contenus non pertinents.
-   **Analyse automatique :** détection de tendances, résumé des textes techniques, extraction de menaces émergentes à l’aide d’algorithmes NLP et éventuellement de modèles de machine learning.
-   **Génération d’alertes et de rapports :** création de synthèses claires et exploitables, avec possibilité d’envoi automatique ou de visualisation dans l’interface.
-   **Intégration dans l’interface web :** affichage des résultats dans une page interactive (via Flask ou Streamlit), avec filtres, graphiques, tableaux de bord et alertes en temps réel.

## Interface utilisateur

L’interface sera une page web interactive développée avec Flask ou Streamlit, permettant à l’utilisateur de :

-   Saisir des critères de recherche : mots-clés, type de menace, période
-   Filtrer les résultats par gravité ou source
-   Consulter des tableaux de bord dynamiques : cartes de menaces, graphiques temporels, diagrammes circulaires
-   Accéder aux alertes critiques avec date, type et résumé
-   Naviguer facilement grâce à une barre latérale et une interface épurée

## Etapes du projet

1.  **Analyse des besoins et définition des fonctionnalités**
    -   Compréhension du processus de veille : Identifier les sources pertinentes (CVE, blogs spécialisés, réseaux sociaux), les types de menaces à surveiller, et les formats de diffusion.
    -   Collecte automatisée : Scraping de flux RSS, intégration d’API pour récupérer des bulletins de sécurité, tweets, articles techniques, etc.
    -   Filtrage et tri des informations : Utilisation de mots-clés, modèles NLP ou algorithmes de machine learning pour classifier les menaces par type, gravité ou cible.
    -   Analyse automatique : Extraction de tendances, résumé des textes, détection de menaces émergentes à l’aide d’outils de traitement de langage naturel.
    -   Diffusion automatisée : Génération de tableaux de bord, envoi d’alertes ou de rapports synthétiques.
2.  **Choix des technologies**
    -   **Langages de programmation :** Python + ?
    -   **Outils et bibliothèques :**
        -   Web scraping : BeautifulSoup, Scrapy, ou Selenium
        -   Analyse des données : pandas, numpy, scikit-learn
        -   Traitement de texte : spaCy, NLTK
        -   Interface et diffusion : Flask ou Streamlit

## Ressources
*   [CodezUp – Real-Time Threat Intelligence Dashboard](https://www.codezup.com/real-time-threat-intelligence-dashboard-using-python-and-dash/)
*   [SOCRadar – Top Free Threat Intelligence Tools](https://socradar.io/top-free-threat-intelligence-tools-to-use-in-2022/)
*   [GitHub – Awesome Threat Intelligence](https://github.com/hslatman/awesome-threat-intelligence)
*   [Top 10 Cybersecurity Dashboard Templates With Samples and Examples](https://www.slideteam.net/blog/top-10-cybersecurity-dashboard-templates-with-samples-and-examples)
*   [Top 10 Best Free Cyber Threat Intelligence Sources and Tools in 2025](https://cybersecuritynews.com/threat-intelligence-sources/)
*   [Web Scraping avec BeautifulSoup – Alucare](https://alucare.fr/cours/web-scraping-python-beautifulsoup/)
*   [Scrapy pour le scraping avancé – DataCamp](https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python)
*   [Traitement NLP avec spaCy – Cours interactif](https://course.spacy.io/)
*   [NLP avec spaCy et NLTK – Krafter](https://www.krafter.fr/nlp-spacy-nltk/)
*   [Créer une interface avec Streamlit – Docstring](https://docstring.fr/blog/creer-une-application-web-avec-streamlit/)
*   [Structurer un projet Python – MonCoachData](https://moncoachdata.com/blog/comment-bien-structurer-un-projet-python/)
