import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from pipeline import process_tweets, process_corpus

# Mise en place de la structure :
st.set_page_config(page_title="JCAP - Macro Intelligence Dashboard", layout="wide")
left_spacer, center_content, right_spacer = st.columns([1, 2, 1])

with center_content:
    try:
        image = Image.open('jcap_logo.png')
        st.image(image, width=250)
    except FileNotFoundError:
        st.warning("Logo JCAP non trouvé")
    st.markdown("<h1 style='text-align: center;'>Macro Intelligence Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Analyse croisée : Flux Social & Corpus Documentaire</h5>",
                unsafe_allow_html=True)

st.markdown("---")

# Données :
@st.cache_data
def load_data():
    tweets = process_tweets('financial_juice_tweets.csv')
    corpus = process_corpus()
    return tweets, corpus

df_tweets, df_corpus = load_data()

# Sidebar :
st.sidebar.header("Filtres")
selected_theme = st.sidebar.multiselect("Filtrer par Thème", df_tweets['Theme'].unique(), default=df_tweets['Theme'].unique())

# SYNTHÈSE MACRO :
st.header("1. Executive Digest")
col1, col2, col3 = st.columns(3)
col1.metric("Thème Dominant du Marché", "Choc Pétrolier / Geopolitics")
col2.metric("Consensus Principal", "Délai des baisses de taux (Fed)")
col3.metric("Signal Faible Identifié", "Inflation Agricole (Cascade Trade)")
st.info("**Digest:** L'escalade en Iran et la menace sur Ormuz ont provoqué un choc énergétique, ravivant les craintes inflationnistes. Cela force la Fed à repousser ses baisses de taux, faisant grimper les taux réels et chuter l'or. La divergence majeure réside dans la persistance de ce choc : purement énergétique, ou va-t-il se propager à l'alimentaire (blé/sucre) ?")
st.markdown("---")

# ANALYSE DU CORPUS :
st.header("2. Analyse du Corpus Documentaire")
col_c1, col_c2 = st.columns([2, 1])

with col_c1:
    st.subheader("Cartographie des Vues Macro")
    st.dataframe(df_corpus, use_container_width=True)

with col_c2:
    st.subheader("Répartition des Signaux")
    fig_pie = px.pie(df_corpus, names='Signal', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# FLUX SOCIAL :
st.header("3. Social Feed & Thématiques Émergentes (Financial Juice)")
filtered_tweets = df_tweets[df_tweets['Theme'].isin(selected_theme)]
col_t1, col_t2 = st.columns([1, 1])

with col_t1:
    st.subheader("Volume des Thématiques en Temps Réel")
    theme_counts = filtered_tweets['Theme'].value_counts().reset_index()
    theme_counts.columns = ['Theme', 'Count']
    fig_bar = px.bar(theme_counts, x='Theme', y='Count', color='Theme', template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_t2:
    st.subheader("Live Feed Interactif")
    for i, row in filtered_tweets.head(10).iterrows():
        st.markdown(f"**{row['author_name']}** - *{str(row['date'])[:10]}* | `[{row['Theme']}]`")
        st.write(f"> {row['content']}")
        st.markdown("---")