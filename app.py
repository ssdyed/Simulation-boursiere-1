import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("Simulation de rentabilité boursière")

# Réglages pour l'utilisateur
st.sidebar.header("Paramètres de simulation")

# choix du stock
stock = st.sidebar.text_input("Symbole de l'action (Yahoo Finance)", "NVIDIA")

# Montant investi
montant_investi = st.sidebar.number_input("Montant investi (en dollars canadien)", value=1000)

# Année de début de l'investissement
annee_debut = st.sidebar.slider("Année de début", 2004, 2024, 2019)

# Chargement des données
st.write(f"Calcul de la rentabilité pour {stock} depuis {annee_debut}")

# données télécharger à partir du 20 novembre de l'année de début choisie
data = yf.download(stock, start=f"{annee_debut}-11-20")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)


# Calcul
# Le calcul du rendement total se fait en calculant le rendemnt par jour sur la période d'investissement
# Rendement jour i = (prix du jour i / Prix d'achat) * Montant investi
# Prix au jour i est le prix de fermeture au jour i
# Prix d'achat est le prix de fermeture le jour de début de l'investissement
data["Valeur_Portefeuille"] = (data["Close"] / data["Close"].iloc[0]) * montant_investi


# Affichage des résultats

# Graphique de la valeur du portefeuille
figure = px.line(data, x=data.index, y="Valeur_Portefeuille", 
                 title="Évolution de la valeur du portefeuille",
                 labels={"Valeur_Portefeuille": "Valeur en $", "Date": "Date"}
                 )
st.plotly_chart(figure)

# Valeur finale
valeur_finale = data["Valeur_Portefeuille"].iloc[-1]
gain = valeur_finale - montant_investi

# Résultats
col1, col2 = st.columns(2)
col1.metric("Valeur finale", f"{valeur_finale:.2f}$")
col2.metric("Gain/Perte", f"{gain:.2f}$", delta_color="normal")

st.caption("Réalisé par SDYE - Données chargées sur Yahoo Finance")
