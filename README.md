# 📊 Analyse de Sentiments - Expresso Sénégal

Projet d'analyse de sentiments sur les publications et commentaires Facebook d'Expresso Sénégal, avec **deux modèles d'analyse complémentaires** (TextBlob et BERT) et un dashboard interactif Streamlit.

---

## 🎯 Objectifs

- Scraper les posts et commentaires Facebook d'Expresso Sénégal
- Nettoyer et préparer les données pour l'analyse NLP
- Analyser les sentiments avec deux approches :
  - **TextBlob** : analyse classique basée sur la polarité (rapide, simple)
  - **BERT** : modèle transformer avancé (précis, robuste)
- Visualiser les résultats dans un dashboard interactif
- Générer des recommandations stratégiques pour améliorer la satisfaction client

---

## 🏗️ Architecture du projet

```
nlp-sentiments-telecom/
├── data/                           # Données brutes et traitées
│   ├── facebook_comments.csv       # Commentaires scrapés
│   ├── facebook_expresso_clean.csv # Données nettoyées
│   ├── sentiment_dual.csv          # Résultats des deux modèles
│   └── sentiment_expresso.csv      # Résultats BERT seul
├── src/
│   ├── scraping/                   # Scripts de scraping
│   │   ├── facebook_comments_selenium.py
│   │   ├── facebook_scraping.py
│   │   └── linkedin_scraping.py
│   ├── nlp/                        # Scripts d'analyse NLP
│   │   ├── clean_facebook_data.py
│   │   ├── sentiment_analysis.py   # Analyse BERT
│   │   └── dual_sentiment_analysis.py  # Analyse dual (TextBlob + BERT)
│   ├── app/                        # Dashboard Streamlit
│   │   └── dashboard.py
│   └── utils/                      # Utilitaires
│       └── xlsx_to_csv.py
├── notebooks/                      # Notebooks Jupyter (exemples)
│   └── analyse.ipynb
├── requirements.txt                # Dépendances Python
└── README.md                       # Documentation

```

---

## 🚀 Installation

### 1. Cloner le repository

```bash
cd nlp-sentiments-telecom
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou
.venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger les ressources NLTK (si nécessaire)

```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
```

---

## 📖 Utilisation

### Pipeline complet

#### 1️⃣ **Scraping des données**

```bash
# Scraper les commentaires Facebook avec Selenium
python src/scraping/facebook_comments_selenium.py

# Ou scraper les posts avec BeautifulSoup
python src/scraping/facebook_scraping.py
```

#### 2️⃣ **Nettoyage des données**

```bash
python src/nlp/clean_facebook_data.py
```

#### 3️⃣ **Analyse de sentiments**

**Option A : Analyse dual (TextBlob + BERT)**

```bash
python src/nlp/dual_sentiment_analysis.py
```

Génère un fichier `data/sentiment_dual.csv` avec les résultats des deux modèles.

**Option B : Analyse BERT uniquement**

```bash
python src/nlp/sentiment_analysis.py
```

#### 4️⃣ **Lancer le dashboard Streamlit**

```bash
streamlit run src/app/dashboard.py
```

Le dashboard s'ouvrira dans votre navigateur.

---

## 🎨 Fonctionnalités du dashboard

### 📂 Sélection de la source de données
- Choisissez le fichier CSV à analyser (dans le dossier `data/`)

### 🤖 Choix du modèle d'analyse
- **TextBlob (classique)** : analyse rapide basée sur la polarité
- **BERT (avancé)** : analyse précise avec modèle transformer
- **Comparaison des deux** : visualisation côte à côte avec taux d'accord

### 📊 Visualisations
- Aperçu des posts et sentiments
- Répartition globale des sentiments (graphique circulaire)
- Pourcentages de posts positifs/négatifs
- Score moyen par sentiment
- Exemples de publications par sentiment
- Nuage de mots des critiques négatives
- Segmentation thématique (réseau, service client, offres, boutique)

### 🔀 Comparaison des modèles (si fichier dual)
- Répartition des sentiments pour chaque modèle
- Taux d'accord entre TextBlob et BERT
- Exemples de désaccords (cas où les modèles divergent)

### 💡 Recommandations
- Suggestions stratégiques basées sur l'analyse
- Recommandations automatiques selon les mots-clés récurrents

---

## 🆚 Comparaison des modèles

| Critère | TextBlob | BERT |
|---------|----------|------|
| **Approche** | Polarité lexicale | Transformers (Deep Learning) |
| **Vitesse** | ⚡ Très rapide | 🐢 Plus lent |
| **Précision** | ⭐⭐⭐ Moyenne | ⭐⭐⭐⭐⭐ Excellente |
| **Multilingue** | ❌ Limité | ✅ Oui (BERT multilingue) |
| **Ressources** | 💻 Légères | 🖥️ Plus importantes |
| **Cas d'usage** | Prototypage, analyse rapide | Production, analyses robustes |

### 💡 Quand utiliser chaque modèle ?

- **TextBlob** : pour des analyses rapides, des prototypes, ou quand les ressources sont limitées
- **BERT** : pour des analyses précises, en production, ou quand la qualité prime sur la vitesse
- **Les deux** : pour comparer les résultats, valider les analyses, ou enrichir un rapport

---

## 📦 Dépendances principales

- `streamlit` : dashboard interactif
- `pandas` : manipulation de données
- `plotly` : graphiques interactifs
- `transformers` : modèles Hugging Face (BERT)
- `textblob` : analyse de sentiment classique
- `selenium` : scraping Facebook
- `beautifulsoup4` : parsing HTML
- `nltk` : traitement du langage naturel
- `langdetect` : détection de langue
- `wordcloud` : nuages de mots

---

## 📝 Notes et limitations

- **Scraping Facebook** : nécessite une connexion manuelle (anti-bot de Facebook)
- **Modèle BERT** : peut être lent sur CPU (environ 1 texte/seconde)
- **TextBlob** : moins précis pour les textes en français que BERT multilingue
- **Données** : les résultats dépendent de la qualité et de la quantité des données scrapées

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

---

## 📄 Licence

Ce projet est à but éducatif et non commercial.

---

## 👤 Auteur

Projet réalisé dans le cadre d'une analyse de sentiments sur les réseaux sociaux pour le secteur des télécommunications.

---

## 🎓 Ressources

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [NLTK Documentation](https://www.nltk.org/)
