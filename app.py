import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import numpy as np

st.title("Simulation de rentabilité boursière")

# Réglages pour l'utilisateur
st.sidebar.header("Paramètres de simulation")

# Choix du stock
stock = st.sidebar.text_input("Symbole de l'action (Yahoo Finance)", "NVDA")

# Montant investi
montant_investi = st.sidebar.number_input("Montant investi (en dollars canadien)", value=1000)

# Année de début de l'investissement
annee_debut = st.sidebar.slider("Année de début", 2004, 2024, 2019)

# Chargement des données
st.write(f"Calcul de la rentabilité pour {stock} depuis {annee_debut}")

# Données téléchargées à partir du 01er janvier de l'année choisie
data = yf.download(stock, start=f"{annee_debut}-01-01")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

# Vérification des données avant de calculer
if not data.empty and len(data) > 0 :
    data = data.copy()


# Partie 1 : Analyse historique du portefeuille (du passé à maintenant)
    # Calcul du portefeuille historique
    # Le calcul du portefeuille se fait en calculant le rendement par jour sur la période d'investissement
    # Rendement jour i = (prix du jour i / Prix d'achat) * Montant investi
    # Prix au jour i est le prix de fermeture au jour i
    # Prix d'achat est le prix de fermeture du stock le jour de début de l'investissement
    data["Valeur_Portefeuille"] = (data["Close"] / data["Close"].iloc[0]) * montant_investi 

    # Graphique de la valeur du portefeuille
    figure_present = px.line(data, x=data.index, y="Valeur_Portefeuille", 
                 title="Évolution réelle de votre investissement",
                 labels={"Valeur_Portefeuille": "Valeur en $", "Date": "Date"}
                 )
    st.plotly_chart(figure_present)

    # Valeur finale
    valeur_finale = data["Valeur_Portefeuille"].iloc[-1]
    gain = valeur_finale - montant_investi

    # Affichage des résultats passés
    col1, col2 = st.columns(2)
    col1.metric("Valeur aujourd'hui", f"{valeur_finale:.2f}$")
    col2.metric("Gain/Perte réel", f"{gain:.2f}$", delta_color="normal")


    # Partie 2 : Simulation Monte Carlo (le futur)

    st.markdown("___")      # ligne de séparation
    st.header("Prédiction Monte Carlo (pour 1 an)")
    st.caption("Simulation de 1000 scénarios futurs basés sur la volatilité historique")

    # Paramètres de simulation
    np.random.seed(71)
    jours_predits = 365        # 1 an = 365 jours
    scenarios_calcul = 1000    # on fait le calcul avec 1000 scenarios
    scenarios_visuel = 50      # on dessine seulement 50 scenarios

    # Calculs mathématiques
    log_returns = np.log(data["Close"] / data["Close"].shift(1))
    mu = log_returns.mean()
    var = log_returns.var()
    tendance = mu - (0.5*var)
    ecart_type = var**0.5
    prix_actuel = data["Close"].iloc[-1]

    # Matrice des prédictions
    predictions = np.zeros((jours_predits, scenarios_calcul))
    predictions[0] = prix_actuel     # tous les scénarios commencent au prix actuel

    # Boucle de génération
    for t in range(1, jours_predits):
        choc_aleatoire = np.random.normal(0, 1, scenarios_calcul)
        predictions[t] = predictions[t-1] * np.exp(tendance + ecart_type*choc_aleatoire)

    # Graphique des prédictions
    fig_monte_carlo = px.line(title=f"Projection de {scenarios_visuel} scénarios possibles")
    for i in range(scenarios_visuel):
        fig_monte_carlo.add_scatter(y=predictions[:, i], mode="lines", name = f"Simulation {i}",
                                    opacity=0.3, showlegend=False)
    
    # ajout de la courbe moyenne
    moyenne_prediction = predictions.mean(axis=1)     # la moyenne de chaque jour pour les 1000 scénarios
    fig_monte_carlo.add_scatter(y=moyenne_prediction, mode="lines", name="Tendance moyenne",
                                line=dict(color="red", width=4))
    
    st.plotly_chart(fig_monte_carlo)

    # Statistiques de prédiction
    prix_finaux_predits = predictions[-1]
    prix_median = np.median(prix_finaux_predits)
    var_95 = np.percentile(prix_finaux_predits, 5)  # sûr à 95% qu'on ne descendra pas plus bas que ce prix

    col_a, col_b = st.columns(2)
    col_a.metric("Prix médian dans 1 an", f"{prix_median:.2f} $")
    col_b.metric("Scénario Pessimiste (95% de risque)", f"{var_95:.2f} $")

    st.caption("Note : Ceci est une projetion statistique. Les performances passées ne 'préjugent' pas les performances futures")
    st.caption("Réalisé par Yves Sery")

    # Au cas ou le tableau de données serait vide ou si l'on fait une erreur de syntaxe pour le symbole
else:
    st.error(f"Aucune donnée trouvée pour le symbole '{stock}'. Vérifiez qu'il s'agit bien du bon symbole.")