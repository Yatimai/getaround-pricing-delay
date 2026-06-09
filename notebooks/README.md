# Notebooks d'Analyse

Ce dossier contient les notebooks Jupyter pour l'analyse exploratoire des données (EDA).

## Notebooks disponibles

### 1. `01_eda_delay_analysis.ipynb` - Analyse des Retards

**Objectif :** Analyser les retards de restitution et déterminer le seuil optimal.

**Contenu :**
- Chargement et exploration des données
- Analyse de la qualité des données
- Statistiques sur les retards
- Identification des cas problématiques
- Simulation de différents seuils
- Recommandations finales

**Durée estimée :** 30-45 minutes

---

### 2. `02_ml_pricing_model.ipynb` - Modèle de Pricing

**Objectif :** Créer un modèle ML pour prédire les prix optimaux.

**Contenu :**
- Exploration des données de pricing
- Analyse des corrélations
- Préparation des features
- Entraînement de plusieurs modèles avec **MLflow**
- Évaluation et sélection du meilleur modèle
- Sauvegarde du modèle

**MLflow Tracking :**
- Toutes les expériences sont enregistrées localement dans `mlruns/`
- Visualisation : `mlflow ui` dans le terminal

**Durée estimée :** 45-60 minutes

---

## Comment utiliser ces notebooks ?

### Option 1 : Jupyter Notebook (local)

```bash
# Installer Jupyter
pip install jupyter

# Lancer Jupyter
cd notebooks
jupyter notebook
```

### Option 2 : JupyterLab (recommandé)

```bash
# Installer JupyterLab
pip install jupyterlab

# Lancer JupyterLab
cd notebooks
jupyter lab
```

### Option 3 : Google Colab

1. Uploader les notebooks sur Google Drive
2. Ouvrir avec Google Colab
3. Uploader les fichiers de données dans Colab

### Option 4 : VS Code

1. Installer l'extension "Jupyter" dans VS Code
2. Ouvrir le notebook
3. Sélectionner le kernel Python

---

## Dépendances nécessaires

```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib openpyxl mlflow
```

Ou utiliser le fichier `requirements.txt` du projet :

```bash
pip install -r ../requirements.txt
```

---

## Ordre recommandé

1. **Commencer par** `01_eda_delay_analysis.ipynb`
   - Comprendre le problème business
   - Analyser les données de retards
   - Obtenir les insights clés

2. **Puis faire** `02_ml_pricing_model.ipynb`
   - Analyser les données de pricing
   - Entraîner le modèle ML
   - Sauvegarder pour l'API

---

## Conseils

- **Exécuter les cellules dans l'ordre** (de haut en bas)
- **Ne pas sauter de cellules** (les variables dépendent les unes des autres)
- **Prendre le temps de lire les commentaires**
- **Expérimenter** : modifiez les paramètres pour voir l'impact !

---

## Résultats attendus

Après avoir exécuté ces notebooks, vous aurez :

1. Une compréhension complète des données
2. Des visualisations pour le dashboard
3. Une recommandation de seuil (60 minutes)
4. Un modèle ML entraîné et sauvegardé
5. Les fichiers nécessaires pour l'API

---

## Problèmes courants

### "ModuleNotFoundError"
```bash
# Installer le module manquant
pip install nom_du_module
```

### "FileNotFoundError"
```bash
# Vérifier que vous êtes dans le bon dossier
cd notebooks
# Les chemins dans les notebooks sont relatifs (../data/)
```

### "Kernel crashed"
```bash
# Redémarrer le kernel
# Dans Jupyter : Kernel > Restart
```

---

## Ressources utiles

- [Documentation Pandas](https://pandas.pydata.org/docs/)
- [Documentation Scikit-learn](https://scikit-learn.org/stable/)
- [Documentation Matplotlib](https://matplotlib.org/)
- [Guide Jupyter](https://jupyter.org/documentation)

---

Bon courage pour votre analyse !
