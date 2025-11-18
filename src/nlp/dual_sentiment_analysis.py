"""
Analyse de sentiments avec deux modèles :
- TextBlob (approche classique basée sur la polarité)
- BERT (modèle transformer avancé de Hugging Face)
"""

import pandas as pd
from textblob import TextBlob
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')


def analyze_with_textblob(text):
    """
    Analyse de sentiment avec TextBlob.
    Retourne un tuple (sentiment, score).
    """
    try:
        analysis = TextBlob(str(text))
        polarity = analysis.sentiment.polarity
        
        # Classification basée sur la polarité
        if polarity > 0.1:
            sentiment = 'Positif'
        elif polarity < -0.1:
            sentiment = 'Négatif'
        else:
            sentiment = 'Neutre'
        
        return sentiment, round(polarity, 4)
    except:
        return 'Neutre', 0.0


def analyze_with_bert(text, sentiment_pipeline):
    """
    Analyse de sentiment avec BERT (Hugging Face).
    Retourne un tuple (sentiment, score).
    """
    try:
        result = sentiment_pipeline(str(text)[:512])[0]  # Limite à 512 caractères pour BERT
        label = result['label']
        score = result['score']
        
        # Mapping des labels BERT vers nos catégories
        if '5' in label or '4' in label:
            sentiment = 'Positif'
        elif '1' in label or '2' in label:
            sentiment = 'Négatif'
        else:
            sentiment = 'Neutre'
        
        return sentiment, round(score, 4)
    except:
        return 'Neutre', 0.0


def dual_sentiment_analysis(input_file="data/sentiment_expresso.csv", 
                            output_file="data/sentiment_dual.csv"):
    """
    Analyse de sentiments avec TextBlob et BERT sur le même dataset.
    Génère un CSV avec les résultats des deux modèles.
    """
    print("Chargement des données...")
    df = pd.read_csv(input_file)
    
    # Détecter la colonne de texte
    text_col = None
    for col in df.columns:
        if col.lower() in ['text', 'clean_text', 'comment']:
            text_col = col
            break
    
    if text_col is None:
        raise ValueError("Aucune colonne de texte trouvée dans le fichier.")
    
    print(f"Colonne de texte détectée : {text_col}")
    print(f"{len(df)} textes à analyser")
    
    # Initialisation du pipeline BERT
    print("\nChargement du modèle BERT...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=-1  # CPU
    )
    
    # Analyse avec TextBlob
    print("\n Analyse avec TextBlob...")
    df[['sentiment_textblob', 'score_textblob']] = df[text_col].apply(
        lambda x: pd.Series(analyze_with_textblob(x))
    )
    
    # Analyse avec BERT
    print(" Analyse avec BERT...")
    df[['sentiment_bert', 'score_bert']] = df[text_col].apply(
        lambda x: pd.Series(analyze_with_bert(x, sentiment_pipeline))
    )
    
    # Ajout d'une colonne pour marquer les cas d'accord/désaccord
    df['modeles_accord'] = df['sentiment_textblob'] == df['sentiment_bert']
    
    # Sauvegarde
    print(f"\n Sauvegarde des résultats dans {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Statistiques
    print("\n" + "="*60)
    print(" RÉSUMÉ DE L'ANALYSE")
    print("="*60)
    
    print("\n🔹 Répartition TextBlob :")
    print(df['sentiment_textblob'].value_counts())
    
    print("\n🔹 Répartition BERT :")
    print(df['sentiment_bert'].value_counts())
    
    accord_rate = (df['modeles_accord'].sum() / len(df)) * 100
    print(f"\n Taux d'accord entre les modèles : {accord_rate:.2f}%")
    
    print("\n Analyse terminée avec succès !")
    return df


if __name__ == "__main__":
    # Exemple d'utilisation
    dual_sentiment_analysis(
        input_file="data/sentiment_expresso.csv",
        output_file="data/sentiment_dual.csv"
    )
