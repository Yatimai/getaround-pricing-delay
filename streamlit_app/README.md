# Getaround Dashboard - Streamlit

Dashboard interactif pour l'analyse des retards de Getaround.

## Fonctionnalités

- **Vue d'ensemble** des données (21K+ locations)
- **Analyse des retards** avec visualisations
- **Locations consécutives** et problèmes identifiés
- **Simulateur de seuils** interactif
- **Recommandations** basées sur les données

## Lancer localement

### 1. Installer les dépendances

```bash
cd streamlit_app
pip install -r requirements.txt
```

### 2. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur à `http://localhost:8501`

## Structure

```
streamlit_app/
├── app.py              # Application principale
├── requirements.txt    # Dépendances Python
└── README.md          # Ce fichier
```

## Données requises

L'application nécessite le fichier :
- `../data/get_around_delay_analysis.xlsx`

Assurez-vous que ce fichier existe dans le dossier `data/` du projet parent.

## Fonctionnalités interactives

### Sidebar (Panneau latéral)
- **Seuil de délai** : Slider de 0 à 720 minutes
- **Périmètre** : Choix entre Toutes/Mobile/Connect
- **Métriques en temps réel** : Impact du seuil choisi

### Sections du dashboard

1. **Vue d'ensemble** : Statistiques générales
2. **Analyse des retards** : Distribution et proportions
3. **Locations consécutives** : Délais entre locations
4. **Cas problématiques** : Identification des impacts
5. **Simulation** : Trade-off entre seuil et impact
6. **Recommandations** : Décision finale

## Déploiement sur Hugging Face Spaces

### Option 1 : Via l'interface web

1. Aller sur [huggingface.co/spaces](https://huggingface.co/spaces)
2. Cliquer sur "Create new Space"
3. Choisir "Streamlit" comme SDK
4. Uploader les fichiers :
   - `app.py`
   - `requirements.txt`
   - Le dossier `data/` avec le fichier Excel

### Option 2 : Via Git

```bash
# Cloner votre space
git clone https://huggingface.co/spaces/gilles-ai/getaround-dashboard

# Copier les fichiers
cp app.py getaround-dashboard/
cp requirements.txt getaround-dashboard/
cp -r ../data getaround-dashboard/

# Commit et push
cd getaround-dashboard
git add .
git commit -m "Add Streamlit dashboard"
git push
```

## Configuration pour Hugging Face

Créer un fichier `.streamlit/config.toml` (optionnel) :

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## Notes importantes

- Le fichier Excel doit être accessible depuis `../data/`
- Pour Hugging Face, ajuster le chemin si nécessaire
- L'application utilise le cache de Streamlit pour optimiser les performances

## Problèmes courants

### "FileNotFoundError"
```bash
# Vérifier que le fichier existe
ls ../data/get_around_delay_analysis.xlsx

# Ajuster le chemin dans app.py si nécessaire
```

### "ModuleNotFoundError"
```bash
# Installer toutes les dépendances
pip install -r requirements.txt
```

## Documentation

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Docs](https://plotly.com/python/)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)

---

**Getaround Analysis - Streamlit dashboard**
