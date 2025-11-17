import pandas as pd

# Chemin du fichier Excel d'entrée
input_file = "data/dataset_facebook-comments-scraper_2025-11-07_11-56-54-643.xlsx"

# Fichier CSV de sortie
output_file = "data/facebook_expresso.csv"

# Lecture du fichier Excel
df = pd.read_excel(input_file)

# Affiche les premières lignes pour vérifier
print("Aperçu du fichier Excel :")
print(df.head())

# Conversion vers CSV
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"✅ Conversion terminée ! Fichier enregistré sous : {output_file}")
