import pandas as pd
import re
import string
from langdetect import detect
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Télécharger les ressources NLTK au premier lancement
nltk.download('stopwords')
nltk.download('wordnet')

def nettoyer_texte(texte):
    if not isinstance(texte, str):
        return ""
    # Supprimer URLs, hashtags, mentions
    texte = re.sub(r"http\S+|www\S+|https\S+", '', texte)
    texte = re.sub(r"[@#]\w+", '', texte)
    # Supprimer chiffres, ponctuation et emojis
    texte = texte.translate(str.maketrans('', '', string.punctuation + string.digits))
    texte = texte.encode('ascii', 'ignore').decode('ascii')
    # Minuscule
    texte = texte.lower()
    # Stopwords français
    stop_words = set(stopwords.words('french'))
    mots = [mot for mot in texte.split() if mot not in stop_words]
    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    mots = [lemmatizer.lemmatize(m) for m in mots]
    return " ".join(mots)

def main():
    input_file = "data/facebook_expresso.csv"
    output_file = "data/facebook_expresso_clean.csv"
    df = pd.read_csv(input_file)
    print("Colonnes du fichier :", list(df.columns))
    if "text" in df.columns:
        # Supprimer doublons et lignes vides uniquement sur la colonne 'text'
        df = df.drop_duplicates(subset=["text"])
        df = df.dropna(subset=["text"])
        # Garder uniquement les textes en français
        def is_french(text):
            try:
                return detect(text) == "fr"
            except Exception:
                return False
        df = df[df["text"].apply(is_french)]
        # Nettoyage du texte
        if "text" in df.columns:
            df["clean_text"] = df["text"].apply(nettoyer_texte)
            # Supprimer les lignes sans texte
            df = df[df["clean_text"].str.len() > 0]
            df = df.reset_index(drop=True)
            df.to_csv(output_file, index=False, encoding="utf-8-sig")
            print(f" Fichier nettoyé enregistré : {output_file}")
            print(df[["text", "clean_text"]].head())
        else:
            print(" La colonne 'text' a été supprimée lors du nettoyage. Vérifiez le contenu du CSV.")
    else:
        print(" La colonne 'text' est absente du fichier. Vérifiez le CSV ou indiquez la colonne à nettoyer.")

if __name__ == "__main__":
    main()
