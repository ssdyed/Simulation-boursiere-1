# Simulateur t prédicteur boursier (Monte Carlo)

Une application web "Full stack" pour analyser les performances passées d'une action et projeter ses futurs possibles grâce aux statistiques.

Projet réalisé en Python.

## Fonctionnalités clés

### i. Analyse historique (le passé)
- Récupération de données financières en temps réel via l'API ** Yahoo Finance**.
- Calcul de la rentabilité réelle d'un investissement.
- compraison dynamique entre le capital investi et la valeur actuelle.

### ii. Prédiction Monte Carlo (le futur)
- **Moteur statistique** : Génération de **1000 scénarios*** d'volution du prix sur 1 an (n=365 jours)
- **Modèle mathématique** : Utilisation du Mouvement Brownien Géométrique (drift + volatilité stochastique)
- **Gestion des risques** : Calcul automatique de la valeur à laquelle l'on serait à risque à un niveau de confiance de 95% ; et du prix médian cible.
- **Visualisation** : Affichage de 50 trajectoires réprésentatives. Les 1000 scénarios ne sont pas affichés pour avoir une meilleure fluidité.

## Stack technique
- **Langage :** Python
- **Interface Web :** Streamlit
- **Callcul scientifique :** NumPy, Pandas
- **Data visualisation :** Plotly interactive
- **Flux de données :** yFiannce API 
