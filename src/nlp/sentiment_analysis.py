import pandas as pd
from transformers import pipeline

def analyse_sentiments(input_file="data/sentiment_dual.csv", output_file="data/sentiment_expresso.csv"):
    # Charger le dataset nettoyé
    df = pd.read_csv(input_file)

    # Charger le modèle Hugging Face
    print(" Chargement du modèle...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
    )

    print(" Analyse des sentiments en cours...")
    sentiments = sentiment_pipeline(df["clean_text"].tolist(), truncation=True)

    # Ajouter les résultats dans le DataFrame
    df["sentiment_label"] = [s["label"] for s in sentiments]
    df["sentiment_score"] = [s["score"] for s in sentiments]

    # Sauvegarde
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f" Analyse terminée ! Fichier enregistré : {output_file}")

    # Petit aperçu
    print(df[["clean_text", "sentiment_label", "sentiment_score"]].head())

if __name__ == "__main__":
    analyse_sentiments()
