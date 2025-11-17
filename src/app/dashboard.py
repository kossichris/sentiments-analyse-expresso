
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import collections
import os

st.set_page_config(page_title="Analyse de Sentiments - Expresso", layout="wide")

# Sélecteur de fichier CSV
st.sidebar.header("📂 Source de données")
csv_files = [f for f in os.listdir("data") if f.endswith(".csv")]
selected_file = st.sidebar.selectbox("Fichier de résultats :", csv_files)

# Sélecteur de modèle (si fichier dual)
st.sidebar.header("🤖 Modèle d'analyse")
model_choice = st.sidebar.radio(
    "Choisissez le modèle à visualiser :",
    ["TextBlob (classique)", "BERT (avancé)", "Comparaison des deux"]
)

@st.cache_data
def load_data(file):
    return pd.read_csv(f"data/{file}")

df = load_data(selected_file)

# Détection si fichier dual (contient les deux modèles)
is_dual = 'sentiment_textblob' in df.columns and 'sentiment_bert' in df.columns

# Détection si fichier dual (contient les deux modèles)
is_dual = 'sentiment_textblob' in df.columns and 'sentiment_bert' in df.columns

# 🟢 Titre principal
st.title("📊 Analyse de Sentiments - Expresso Sénégal")
st.markdown("Ce tableau de bord affiche les résultats de l'analyse des sentiments extraits depuis les publications Facebook d'Expresso Sénégal.")

# Information sur le modèle utilisé
if is_dual:
    if "TextBlob" in model_choice:
        st.info("🔍 Affichage des résultats du modèle **TextBlob** (analyse classique basée sur la polarité)")
    elif "BERT" in model_choice:
        st.info("🤖 Affichage des résultats du modèle **BERT** (analyse avancée avec transformers)")
    else:
        st.info("🔀 Affichage de la **comparaison** entre TextBlob et BERT")

# 🔹 Aperçu des posts (fonctionnalité du projet 'Projet')
st.subheader("Aperçu des posts")
text_col = None
sentiment_col = None

# Déterminer les colonnes à afficher selon le modèle choisi
if is_dual:
    if "TextBlob" in model_choice:
        sentiment_col = "sentiment_textblob"
    elif "BERT" in model_choice:
        sentiment_col = "sentiment_bert"
    else:  # Comparaison
        sentiment_col = None  # On affichera les deux
else:
    for col in df.columns:
        if col.lower() in ["sentiment", "sentiment_label"]:
            sentiment_col = col
            break

for col in df.columns:
    if col.lower() in ["text", "clean_text"]:
        text_col = col
        break

if text_col:
    if sentiment_col:
        st.dataframe(df[[text_col, sentiment_col]].head(10))
    elif is_dual and "Comparaison" in model_choice:
        st.dataframe(df[[text_col, "sentiment_textblob", "sentiment_bert", "modeles_accord"]].head(10))
    else:
        st.dataframe(df[[text_col]].head(10))
else:
    st.info("Colonne de texte non trouvée dans ce fichier.")

# 🔹 Conversion si nécessaire
if "sentiment_label" in df.columns:
    df["sentiment_label"] = df["sentiment_label"].replace({
        "1 star": "Négatif",
        "2 stars": "Négatif",
        "3 stars": "Neutre",
        "4 stars": "Positif",
        "5 stars": "Positif"
    })


# 🔸 Répartition globale
sentiment_col = None

# Déterminer la colonne de sentiment selon le modèle choisi
if is_dual:
    if "TextBlob" in model_choice:
        sentiment_col = "sentiment_textblob"
    elif "BERT" in model_choice:
        sentiment_col = "sentiment_bert"
else:
    for col in df.columns:
        if col.lower() in ["sentiment", "sentiment_label"]:
            sentiment_col = col
            break

if sentiment_col:
    sent_counts = df[sentiment_col].value_counts().reset_index()
    sent_counts.columns = ["Sentiment", "Nombre"]
    fig_pie = px.pie(
        sent_counts,
        names="Sentiment",
        values="Nombre",
        color="Sentiment",
        color_discrete_map={"Positif": "green", "Neutre": "gray", "Négatif": "red"},
        title=f"Répartition globale des sentiments - {model_choice if is_dual else 'Analyse'}"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # 🔸 Pourcentage de positif et négatif (fonctionnalité du projet 'Projet')
    total = sent_counts["Nombre"].sum()
    positif_pct = round((sent_counts[sent_counts["Sentiment"].str.lower().str.contains("positif")]["Nombre"].sum()/total)*100, 2)
    negatif_pct = round((sent_counts[sent_counts["Sentiment"].str.lower().str.contains("négatif")]["Nombre"].sum()/total)*100, 2)
    st.write(f"Pourcentage de posts positifs : {positif_pct}%")
    st.write(f"Pourcentage de posts négatifs : {negatif_pct}%")

# 🔀 Section Comparaison des deux modèles (si fichier dual et comparaison activée)
if is_dual and "Comparaison" in model_choice:
    st.header("🔀 Comparaison des modèles TextBlob vs BERT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("TextBlob")
        sent_counts_tb = df["sentiment_textblob"].value_counts().reset_index()
        sent_counts_tb.columns = ["Sentiment", "Nombre"]
        fig_tb = px.pie(
            sent_counts_tb,
            names="Sentiment",
            values="Nombre",
            color="Sentiment",
            color_discrete_map={"Positif": "green", "Neutre": "gray", "Négatif": "red"},
            title="Répartition TextBlob"
        )
        st.plotly_chart(fig_tb, use_container_width=True)
    
    with col2:
        st.subheader("BERT")
        sent_counts_bert = df["sentiment_bert"].value_counts().reset_index()
        sent_counts_bert.columns = ["Sentiment", "Nombre"]
        fig_bert = px.pie(
            sent_counts_bert,
            names="Sentiment",
            values="Nombre",
            color="Sentiment",
            color_discrete_map={"Positif": "green", "Neutre": "gray", "Négatif": "red"},
            title="Répartition BERT"
        )
        st.plotly_chart(fig_bert, use_container_width=True)
    
    # Taux d'accord
    accord_rate = (df['modeles_accord'].sum() / len(df)) * 100
    st.metric("🤝 Taux d'accord entre les modèles", f"{accord_rate:.2f}%")
    
    # Exemples de désaccord
    st.subheader("📋 Exemples de désaccords entre les modèles")
    desaccord_df = df[df['modeles_accord'] == False][[text_col, "sentiment_textblob", "sentiment_bert"]].head(10)
    st.dataframe(desaccord_df)



# 🔹 Histogramme des scores moyens
sentiment_col = None
score_col = None

# Déterminer les colonnes selon le modèle choisi
if is_dual:
    if "TextBlob" in model_choice:
        sentiment_col = "sentiment_textblob"
        score_col = "score_textblob"
    elif "BERT" in model_choice:
        sentiment_col = "sentiment_bert"
        score_col = "score_bert"
else:
    for col in df.columns:
        if col.lower() in ["sentiment", "sentiment_label"]:
            sentiment_col = col
        if col.lower() in ["sentiment_score", "score"]:
            score_col = col

if sentiment_col and score_col and "Comparaison" not in model_choice:
    avg_score = df.groupby(sentiment_col)[score_col].mean().reset_index()
    fig_bar = px.bar(
        avg_score,
        x=sentiment_col,
        y=score_col,
        color=sentiment_col,
        color_discrete_map={"Positif": "green", "Neutre": "gray", "Négatif": "red"},
        title=f"Score moyen par sentiment - {model_choice if is_dual else 'Analyse'}"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
elif not is_dual:
    st.info("Colonnes de sentiment ou de score non trouvées pour l'histogramme.")

# 🔹 Exemples de textes
st.header("🔍 Exemples de publications")
sentiment_col = None
text_col = None
score_col = None

# Déterminer les colonnes selon le modèle choisi
if is_dual:
    if "TextBlob" in model_choice:
        sentiment_col = "sentiment_textblob"
        score_col = "score_textblob"
    elif "BERT" in model_choice:
        sentiment_col = "sentiment_bert"
        score_col = "score_bert"
else:
    for col in df.columns:
        if col.lower() in ["sentiment", "sentiment_label"]:
            sentiment_col = col
        if col.lower() in ["sentiment_score", "score"]:
            score_col = col

for col in df.columns:
    if col.lower() in ["text", "clean_text"]:
        text_col = col
        break

if sentiment_col and text_col and "Comparaison" not in model_choice:
    sent_choice = st.selectbox("Choisir un type de sentiment :", df[sentiment_col].unique())
    
    if score_col:
        sample_texts = df[df[sentiment_col] == sent_choice][[text_col, score_col]].head(10)
        for _, row in sample_texts.iterrows():
            st.write(f"**Texte :** {row[text_col]}")
            st.write(f"Score : {row[score_col]:.2f}")
            st.markdown("---")
    else:
        sample_texts = df[df[sentiment_col] == sent_choice][[text_col]].head(10)
        for _, row in sample_texts.iterrows():
            st.write(f"**Texte :** {row[text_col]}")
            st.markdown("---")

# 🔹 Wordcloud pour les critiques négatives
if "Comparaison" not in model_choice:
    st.header("☁️ Nuage de mots des critiques négatives")
    sentiment_col = None
    text_col = None
    
    # Déterminer les colonnes selon le modèle choisi
    if is_dual:
        if "TextBlob" in model_choice:
            sentiment_col = "sentiment_textblob"
        elif "BERT" in model_choice:
            sentiment_col = "sentiment_bert"
    else:
        for col in df.columns:
            if col.lower() in ["sentiment", "sentiment_label"]:
                sentiment_col = col
                break
    
    for col in df.columns:
        if col.lower() in ["text", "clean_text"]:
            text_col = col
            break

    if sentiment_col and text_col:
        # Détection du terme "négatif" dans la colonne sentiment
        neg_df = df[df[sentiment_col].str.lower().str.contains("négatif", na=False)]
        neg_texts = " ".join(neg_df[text_col].dropna().tolist())
        if neg_texts:
            wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Reds').generate(neg_texts)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.info("Aucune critique négative à afficher.")
    else:
        st.info("Colonnes nécessaires non trouvées pour le nuage de mots.")


# 🔹 Bloc recommandations enrichi
st.header("💡 Recommandations pour Expresso")

st.markdown("- **Améliorer la couverture et la stabilité du réseau**  \n- **Simplifier l'activation et l'utilisation des forfaits**  \n- **Renforcer la communication et le service client**")

# Suggestions automatiques
if 'neg_texts' in locals() and neg_texts:
    neg_words = neg_texts.split()
    most_common = collections.Counter(neg_words).most_common(10)
    reco_map = {
        "reseau": "Améliorer la qualité et la stabilité du réseau.",
        "connexion": "Renforcer la couverture et la rapidité de la connexion.",
        "service": "Optimiser le service client et la réactivité.",
        "forfait": "Proposer des offres plus adaptées aux besoins des clients.",
        "internet": "Augmenter la vitesse et la fiabilité d'internet.",
        "appel": "Améliorer la qualité des appels et la disponibilité.",
        "client": "Renforcer l'écoute et la satisfaction client."
    }
    st.markdown("**Suggestions basées sur les mots les plus cités dans les critiques négatives :**")
    for word, count in most_common:
        if word in reco_map:
            st.write(f"- {reco_map[word]} ({count} mentions)")

st.success("✅ Tableau de bord prêt !")
# 🔹 Catégorisation par thématique
st.header("📂 Segmentation par thématique")
theme_keywords = {
    "Réseau": ["reseau", "connexion", "internet", "couverture", "signal", "débit"],
    "Service client": ["service", "client", "réponse", "appel", "support", "aide", "conseiller"],
    "Offres": ["forfait", "offre", "prix", "promo", "tarif", "abonnement"],
    "Boutique": ["boutique", "agence", "point de vente", "guichet"]
}
def detect_theme(text):
    for theme, keywords in theme_keywords.items():
        for kw in keywords:
            if kw in str(text).lower():
                return theme
    return "Autre"

text_col = None
sentiment_col = None
score_col = None
for col in df.columns:
    if col.lower() in ["text", "clean_text"]:
        text_col = col
    if col.lower() in ["sentiment", "sentiment_label"]:
        sentiment_col = col
    if col.lower() in ["sentiment_score", "score"]:
        score_col = col

if text_col:
    df["theme"] = df[text_col].apply(detect_theme)
    theme_counts = df["theme"].value_counts().reset_index()
    theme_counts.columns = ["Thème", "Nombre"]
    fig_theme = px.bar(
        theme_counts,
        x="Thème",
        y="Nombre",
        color="Thème",
        title="Répartition des textes par thématique"
    )
    st.plotly_chart(fig_theme, use_container_width=True)

    # 🔹 Exemples par thématique
    st.header("🔍 Exemples de publications par thématique")
    theme_choice = st.selectbox("Choisir une thématique :", df["theme"].unique())
    
    cols_to_display = [text_col]
    if sentiment_col:
        cols_to_display.append(sentiment_col)
    if score_col:
        cols_to_display.append(score_col)
    
    sample_theme = df[df["theme"] == theme_choice][cols_to_display].head(10)
    for _, row in sample_theme.iterrows():
        st.write(f"**Texte :** {row[text_col]}")
        if sentiment_col:
            sentiment_display = f"Sentiment : {row[sentiment_col]}"
            if score_col:
                sentiment_display += f" | Score : {row[score_col]:.2f}"
            st.write(sentiment_display)
        st.markdown("---")
else:
    st.info("Colonne de texte non trouvée pour la segmentation thématique.")
