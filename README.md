# DM Python Data Science — Élections

Ce dépôt contient le travail réalisé pour le DM intermédiaire de Python Data Science.

L’objectif est d’explorer les résultats du premier tour de l’élection présidentielle française de 2022 à l’échelle communale et départementale à l’aide de Python.

## Contenu du dépôt

- `notebook_dm.ipynb` : notebook principal contenant les analyses, tableaux et figures
- `utils.py` : fonctions utilitaires utilisées pour les visualisations
- `requirements.txt` : liste des bibliothèques nécessaires à l’exécution du projet

## Bibliothèques utilisées

Ce projet mobilise notamment :

- `pandas` pour la manipulation et l’analyse des données
- `matplotlib` pour les graphiques
- `great-tables` pour la mise en forme des tableaux
- `cartiflette` et `geopandas` pour la cartographie

## Reproductibilité

Pour exécuter le projet, installer d’abord les dépendances :

```bash
pip install -r requirements.txt
```

Puis ouvrir le notebook Jupyter et exécuter l’ensemble des cellules (Run all).

Remarque:

Le notebook principal contient les réponses aux questions du DM.
Certaines fonctions ont été placées dans utils.py afin d’alléger le notebook et de mieux séparer les calculs, les visualisations et la logique utilitaire.
 