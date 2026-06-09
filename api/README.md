# Getaround Pricing API

API REST FastAPI pour prédire les prix de location de voitures.

## Fonctionnalités

- **POST /predict** : Prédire le prix d'une voiture
- **GET /docs** : Documentation interactive Swagger
- **GET /health** : Vérifier l'état de l'API
- **GET /model-info** : Informations sur le modèle ML

## Lancer localement

### 1. Installer les dépendances

```bash
cd api
pip install -r requirements.txt
```

### 2. Lancer l'API

```bash
uvicorn main:app --reload
```

L'API sera accessible à : `http://localhost:8000`

Documentation interactive : `http://localhost:8000/docs`

## Utilisation

### Endpoint principal : POST /predict

**URL :** `http://localhost:8000/predict`

**Input (JSON) :**
```json
{
  "input": [[1, 150000, 120, 0, 2, 1, 1, 1, 1, 0, 1, 1, 1]]
}
```

**Output (JSON) :**
```json
{
  "prediction": [125.50]
}
```

### Features (dans l'ordre)

1. **model_key** : Modèle encodé (0-27)
2. **mileage** : Kilométrage (ex: 150000)
3. **engine_power** : Puissance moteur (ex: 120)
4. **fuel** : Carburant encodé (0=diesel, 1=electro, 2=hybrid_petrol, 3=petrol)
5. **paint_color** : Couleur encodée (0-9)
6. **car_type** : Type encodé (0-7)
7. **private_parking_available** : Parking privé (0 ou 1)
8. **has_gps** : GPS (0 ou 1)
9. **has_air_conditioning** : Climatisation (0 ou 1)
10. **automatic_car** : Boîte auto (0 ou 1)
11. **has_getaround_connect** : Connect (0 ou 1)
12. **has_speed_regulator** : Régulateur (0 ou 1)
13. **winter_tires** : Pneus hiver (0 ou 1)

## Tester avec curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"input": [[1, 150000, 120, 0, 2, 1, 1, 1, 1, 0, 1, 1, 1]]}'
```

## Tester avec Python

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"input": [[1, 150000, 120, 0, 2, 1, 1, 1, 1, 0, 1, 1, 1]]}
)

print(response.json())
# {'prediction': [125.50]}
```

## Exemple complet

```python
import requests

# Données d'une voiture (ordre: model_key, mileage, engine_power, ...)
car_data = {
    "input": [[
        5,       # model_key (Peugeot encodé)
        150000,  # mileage (kilométrage)
        120,     # engine_power (puissance)
        0,       # fuel (diesel)
        1,       # paint_color (grise)
        2,       # car_type (berline)
        1,       # private_parking_available
        1,       # has_gps
        1,       # has_air_conditioning
        0,       # automatic_car (manuelle)
        1,       # has_getaround_connect
        1,       # has_speed_regulator
        1        # winter_tires
    ]]
}

# Appel API
response = requests.post(
    "http://localhost:8000/predict",
    json=car_data
)

# Résultat
if response.status_code == 200:
    prix = response.json()['prediction'][0]
    print(f"Prix prédit: {prix} euros/jour")
else:
    print(f"Erreur: {response.status_code}")
```

## Déploiement sur Hugging Face Spaces

### 1. Créer un Space

1. Aller sur [huggingface.co/spaces](https://huggingface.co/spaces)
2. Cliquer "Create new Space"
3. Choisir "Docker" comme SDK
4. Nommer le Space (ex: "getaround-api")

### 2. Préparer les fichiers

Créer un `Dockerfile` :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY models ./models

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### 3. Uploader

- `main.py`
- `requirements.txt`
- `Dockerfile`
- Le dossier `models/` avec les fichiers .joblib

## Documentation API

Une fois l'API lancée, accédez à :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## Structure

```
api/
├── main.py              # Application FastAPI
├── requirements.txt     # Dépendances
└── README.md           # Ce fichier
```

## Modèle utilisé

- **Algorithme** : Gradient Boosting Regressor
- **Performance** : R² = 0.726 (72.6% de variance expliquée)
- **Erreur moyenne** : 17.32 euros (RMSE)
- **Dataset d'entraînement** : 4,841 voitures

## Troubleshooting

### Erreur "Modèle non chargé"
```bash
# Vérifier que les fichiers existent
ls ../models/
# Doit afficher: model.joblib, label_encoders.joblib, feature_names.joblib
```

### Erreur "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Port déjà utilisé
```bash
# Utiliser un autre port
uvicorn main:app --reload --port 8001
```

## Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Uvicorn](https://www.uvicorn.org/)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)

---

**Getaround Pricing API**
