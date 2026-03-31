import pandas as pd
import re
import os


# --- 1. TRAITEMENT DU FLUX SOCIAL (TWEETS) ---
def process_tweets(csv_path):
    df_tweets = pd.read_csv(csv_path)

    # Nettoyage basique
    df_tweets['date'] = pd.to_datetime(df_tweets['date'], errors='coerce')
    df_tweets['content_clean'] = df_tweets['content'].str.lower().apply(lambda x: re.sub(r'http\S+', '', str(x)))

    # Mots-clés pour catégorisation rapide (Simulation NLP/Thèmes)
    themes = {
        'Energy/Oil': ['oil', 'energy', 'hormuz', 'gas', 'brent'],
        'Central Banks/Rates': ['fed', 'ecb', 'rate', 'inflation', 'powell', 'cut', 'hike'],
        'Geopolitics': ['trump', 'iran', 'war', 'israel', 'eu', 'sanctions'],
        'Metals/Commodities': ['gold', 'copper', 'wheat', 'sugar']
    }

    def assign_theme(text):
        for theme, keywords in themes.items():
            if any(kw in text for kw in keywords):
                return theme
        return 'Other'

    df_tweets['Theme'] = df_tweets['content_clean'].apply(assign_theme)
    return df_tweets


# --- 2. TRAITEMENT DU CORPUS (PDFs) ---
# Note: Dans un vrai environnement, on utiliserait PyPDF2 ou pdfminer.
# Ici on va créer un dataframe structuré représentant l'extraction pour alimenter le dashboard.
def process_corpus():
    # Simulation de l'extraction NLP post-lecture des PDFs fournis
    data = [
        {"Doc": "Natixis - US Macro", "Dominant_Theme": "Central Banks/Rates",
         "Key_Point": "Fed rate cuts delayed due to energy shock.", "Signal": "Consensus"},
        {"Doc": "Alexander Campbell - Cascade Trade", "Dominant_Theme": "Metals/Commodities",
         "Key_Point": "Market pricing oil, missing agricultural shock (wheat/sugar).",
         "Signal": "Contrasting View / Weak Signal"},
        {"Doc": "Goldman Sachs - China Musings", "Dominant_Theme": "Geopolitics",
         "Key_Point": "China better placed than DM in this specific oil shock.", "Signal": "Contrasting View"},
        {"Doc": "Unknown - War-driven inflation", "Dominant_Theme": "Metals/Commodities",
         "Key_Point": "Gold dropping because real rates are surging. Transient vs Persistent oil shock.",
         "Signal": "Controversy"},
        {"Doc": "SEB - Nuclear landscape", "Dominant_Theme": "Energy/Oil",
         "Key_Point": "Nuclear power revival in Europe for energy security.", "Signal": "Weak Signal"},
    ]
    return pd.DataFrame(data)


# Si exécuté en standalone, on sauvegarde les données nettoyées
if __name__ == "__main__":
    df_t = process_tweets('financial_juice_tweets.csv')
    df_c = process_corpus()
    df_t.to_csv('processed_tweets.csv', index=False)
    df_c.to_csv('processed_corpus.csv', index=False)
    print("Pipeline exécuté avec succès. Données prêtes pour le dashboard.")