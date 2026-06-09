from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List

app = FastAPI(
    title="Getaround Pricing API",
    description="""
## API de prediction de prix pour Getaround

Cette API permet de predire le prix optimal de location d'une voiture par jour.

### Exemple concret

Une **Peugeot 308** avec :
- 150 000 km, 120 cv, diesel, grise, berline
- Avec : GPS, clim, parking prive, regulateur, pneus hiver
- Sans : boite auto, Getaround Connect

```json
POST /predict
{
  "input": [[5, 150000, 120, 0, 4, 5, 1, 1, 1, 0, 0, 1, 1]]
}
```

**Reponse** : `{"prediction": [130.50]}` → 130.50 euros/jour

### Modele utilise
- **Algorithme** : Gradient Boosting Regressor
- **Performance** : R² = 0.73 (73% de variance expliquee)
- **Erreur moyenne** : 17 euros (RMSE)
""",
    version="1.0.0"
)

MODEL_PATH = "models/model.joblib"
ENCODERS_PATH = "models/label_encoders.joblib"
FEATURES_PATH = "models/feature_names.joblib"

try:
    model = joblib.load(MODEL_PATH)
    label_encoders = joblib.load(ENCODERS_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    print("[OK] Modele charge avec succes")
except Exception as e:
    print(f"[ERREUR] Erreur lors du chargement du modele : {e}")
    model = None

class PredictionInput(BaseModel):
    """Format d'entree pour la prediction"""
    input: List[List[float]]

    model_config = {
        "json_schema_extra": {
            "example": {
                "input": [[1, 150000, 120, 0, 2, 1, 1, 1, 1, 0, 1, 1, 1]]
            }
        }
    }

class PredictionOutput(BaseModel):
    """Format de sortie pour la prediction"""
    prediction: List[float]

@app.get("/")
def read_root():
    """
    Endpoint racine - Page d'accueil de l'API
    """
    return {
        "message": "Welcome to the Getaround Pricing API",
        "documentation": "/docs",
        "health": "/health",
        "predict": "/predict (POST)"
    }

@app.get("/health")
def health_check():
    """
    Verifier que l'API fonctionne correctement
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modele non charge")

    return {
        "status": "healthy",
        "model_loaded": True,
        "features_count": len(feature_names)
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    """
    Predire le prix de location d'une voiture

    **Input:** Liste de listes de 13 features (permet les predictions en batch)

    **Features (dans l'ordre):**

    | # | Feature | Type | Valeurs |
    |---|---------|------|---------|
    | 1 | model_key | int | 0-27 (Alfa Romeo=0, Audi=1, BMW=2, Citroen=3, Ferrari=4, Fiat=5, Ford=6, Honda=7, KIA=8, Lamborghini=9, Lexus=10, Maserati=11, Mazda=12, Mercedes=13, Mini=14, Mitsubishi=15, Nissan=16, Opel=17, PGO=18, Peugeot=19, Porsche=20, Renault=21, SEAT=22, Subaru=23, Suzuki=24, Toyota=25, Volkswagen=26, Yamaha=27) |
    | 2 | mileage | int | Kilometrage (ex: 150000) |
    | 3 | engine_power | int | Puissance en CV (ex: 120) |
    | 4 | fuel | int | 0=diesel, 1=electro, 2=hybrid_petrol, 3=petrol |
    | 5 | paint_color | int | 0=beige, 1=black, 2=blue, 3=brown, 4=grey, 5=green, 6=orange, 7=red, 8=silver, 9=white |
    | 6 | car_type | int | 0=convertible, 1=coupe, 2=estate, 3=hatchback, 4=sedan, 5=subcompact, 6=suv, 7=van |
    | 7 | private_parking_available | int | 0=Non, 1=Oui |
    | 8 | has_gps | int | 0=Non, 1=Oui |
    | 9 | has_air_conditioning | int | 0=Non, 1=Oui |
    | 10 | automatic_car | int | 0=Non, 1=Oui |
    | 11 | has_getaround_connect | int | 0=Non, 1=Oui |
    | 12 | has_speed_regulator | int | 0=Non, 1=Oui |
    | 13 | winter_tires | int | 0=Non, 1=Oui |

    **Output:** Liste des prix predits (en euros/jour)
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modele non disponible")

    try:
        input_data = np.array(data.input)

        if input_data.shape[1] != len(feature_names):
            raise HTTPException(
                status_code=400,
                detail=f"Nombre de features incorrect. Attendu: {len(feature_names)}, Recu: {input_data.shape[1]}"
            )

        predictions = model.predict(input_data)
        predictions = [round(float(p), 2) for p in predictions]

        return {"prediction": predictions}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erreur de validation: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prediction: {str(e)}")

@app.get("/model-info")
def model_info():
    """
    Informations sur le modele ML utilise
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modele non charge")

    return {
        "model_type": type(model).__name__,
        "features": feature_names,
        "n_features": len(feature_names),
        "description": "Gradient Boosting Regressor entraine sur 4841 voitures"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
