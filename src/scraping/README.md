# 🕷️ Module de Scraping - NLP Sentiments Télécom

Ce module contient les scripts pour récupérer les données des réseaux sociaux des opérateurs télécom au Sénégal.

## 📁 Structure

```
src/scraping/
├── facebook_scraping.py      # Scraping Facebook (facebook-scraper)
├── linkedin_scraping.py      # Scraping LinkedIn (Selenium)
├── generate_sample_data.py   # Génération de données d'exemple
└── _schema.py               # Schémas de données
```

## 🚀 Scripts Disponibles

### 1. LinkedIn Scraping (Selenium) ✅ RECOMMANDÉ

**Fichier:** `linkedin_scraping.py`

#### Installation des dépendances
```bash
pip install selenium pandas
```

#### Utilisation
```bash
python src/scraping/linkedin_scraping.py
```

**Fonctionnement:**
1. Le script ouvre Chrome automatiquement
2. Vous devez vous connecter manuellement à LinkedIn
3. Une fois connecté, appuyez sur ENTRÉE dans le terminal
4. Le script récupère automatiquement les posts

**Configuration:**
```python
scrape_linkedin_posts(
    company_url="https://www.linkedin.com/company/orange-senegal/",
    num_posts=30,
    output_file="data/linkedin_posts_orange.csv",
    headless=False  # True pour mode sans interface
)
```

**Avantages:**
- ✅ Fonctionne de manière fiable
- ✅ Contrôle total sur le navigateur
- ✅ Peut gérer l'authentification
- ✅ Pas besoin d'API

**Limitations:**
- ⚠️ Nécessite une connexion manuelle
- ⚠️ Plus lent que l'API
- ⚠️ Peut être détecté par LinkedIn

---

### 2. Facebook Scraping (facebook-scraper)

**Fichier:** `facebook_scraping.py`

#### Installation
```bash
pip install facebook-scraper lxml_html_clean pandas
```

#### Utilisation
```bash
python src/scraping/facebook_scraping.py
```

**Limitations:**
- ⚠️ Facebook bloque souvent les scrapers
- ⚠️ Peut ne récupérer aucun post
- ⚠️ Non fiable pour la production

**Alternative recommandée:** Utiliser l'API officielle Facebook Graph API

---

### 3. Génération de Données d'Exemple

**Fichier:** `generate_sample_data.py`

Utile pour le développement et les tests quand les vraies données ne sont pas accessibles.

#### Utilisation
```bash
python src/scraping/generate_sample_data.py
```

Génère 100 posts d'exemple avec sentiments variés (positifs, négatifs, neutres).

---

## 📊 Format des Données

Tous les scripts génèrent des fichiers CSV avec la structure suivante:

| Colonne | Description | Type |
|---------|-------------|------|
| `platform` | Réseau social (facebook, linkedin, twitter) | string |
| `brand` | Opérateur (Orange, Expresso, Free) | string |
| `post_id` | Identifiant unique du post | string |
| `post_url` | URL du post | string |
| `post_date` | Date de publication | datetime |
| `content` | Texte du post/commentaire | string |
| `like_count` | Nombre de likes/réactions | int |
| `comment_count` | Nombre de commentaires | int |
| `share_count` | Nombre de partages | int |
| `reactions_json` | Détails des réactions (JSON) | string |

---

## 🎯 Entreprises Cibles

### URLs LinkedIn
- **Orange Sénégal:** https://www.linkedin.com/company/orange-senegal/
- **Expresso:** https://www.linkedin.com/company/expresso-senegal/
- **Free Sénégal:** https://www.linkedin.com/company/free-senegal/

### Pages Facebook
- **Orange Sénégal:** https://www.facebook.com/OrangeSenegal
- **Expresso:** https://www.facebook.com/expressosenegal

---

## 🛠️ Configuration Avancée

### Scraping Multiple Entreprises (LinkedIn)

```python
from linkedin_scraping import scrape_multiple_companies

companies = {
    "Orange": "https://www.linkedin.com/company/orange-senegal/",
    "Expresso": "https://www.linkedin.com/company/expresso-senegal/",
    "Free": "https://www.linkedin.com/company/free-senegal/"
}

scrape_multiple_companies(companies, num_posts=20)
```

### Mode Headless (sans interface)

Pour exécuter le scraping sans ouvrir de fenêtre:

```python
scrape_linkedin_posts(
    company_url="...",
    headless=True  # Pas d'interface graphique
)
```

**Note:** En mode headless, vous devrez gérer l'authentification différemment (cookies, tokens).

---

## ⚠️ Considérations Légales et Éthiques

1. **Respect des CGU:** Vérifiez les conditions d'utilisation de chaque plateforme
2. **Rate Limiting:** Ne faites pas trop de requêtes rapidement
3. **Données Personnelles:** Respectez le RGPD et les lois locales
4. **APIs Officielles:** Privilégiez toujours les APIs officielles quand disponibles

---

## 🐛 Résolution de Problèmes

### Problème: "lxml.html.clean ImportError"
**Solution:**
```bash
pip install lxml_html_clean
```

### Problème: "ChromeDriver not found"
**Solution:** Selenium télécharge automatiquement ChromeDriver. Si ça ne fonctionne pas:
```bash
pip install --upgrade selenium
```

### Problème: Aucun post récupéré sur LinkedIn
**Causes possibles:**
- Pas connecté à LinkedIn
- Page entreprise incorrecte
- Sélecteurs CSS changés par LinkedIn

**Solution:**
- Vérifiez que vous êtes bien connecté
- Vérifiez l'URL de la page
- Mettez à jour les sélecteurs CSS dans le code

### Problème: Facebook bloque le scraping
**Solution:** Utilisez l'API officielle Facebook Graph API ou générez des données d'exemple pour le développement.

---

## 📈 Prochaines Étapes

Après avoir récupéré les données:

1. **Nettoyage:** Utilisez le module `src/nlp/` pour prétraiter le texte
2. **Analyse:** Appliquez l'analyse de sentiment
3. **Visualisation:** Créez des dashboards avec les résultats
4. **API:** Exposez les résultats via `src/app/`

---

## 📝 Notes

- Les scripts créent automatiquement le dossier `data/` si nécessaire
- Les fichiers CSV utilisent l'encodage UTF-8 avec BOM pour Excel
- Les timestamps sont au format ISO 8601

---

## 🤝 Contribution

Pour ajouter un nouveau scraper:

1. Créer un fichier `platform_scraping.py`
2. Implémenter une fonction `scrape_platform_posts()`
3. Respecter le schéma de données standard
4. Ajouter la documentation dans ce README
