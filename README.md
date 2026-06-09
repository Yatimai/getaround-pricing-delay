# Getaround Pricing and Delay Analysis

End-to-end machine learning project for a car-rental marketplace, covering the full path from
analysis to a deployed service. It answers two business questions: how long a minimum delay
between rentals should be to limit friction between consecutive drivers, and what daily rental
price to recommend for a given car. The project ships a Streamlit dashboard for decision support,
a FastAPI prediction service, and MLflow experiment tracking, all containerized with Docker.

## Architecture

```
   Data (pricing CSV + delay XLSX)
            │
            ▼
   Notebooks  ──  EDA / delay analysis (01) + ML pricing model (02)
            │                         │
            │                         ▼
            │              MLflow tracking (model comparison)
            ▼                         │
   Trained model (.joblib)  ◀─────────┘
        │                 │
        ▼                 ▼
   FastAPI service     Streamlit dashboard
   (price prediction)  (delay threshold + pricing decision support)
        │                 │
        └──── Docker, deployable to Hugging Face Spaces ────┘
```

## Tech Stack

- **Language**: Python 3.11
- **ML**: scikit-learn (Gradient Boosting, Random Forest, Linear, Ridge), pandas, NumPy
- **Experiment tracking**: MLflow
- **API**: FastAPI (Docker)
- **Dashboard**: Streamlit
- **Deployment**: Docker, Hugging Face Spaces

## Project Structure

```
getaround-pricing-delay/
├── notebooks/
│   ├── 01_eda_delay_analysis.ipynb   # Delay analysis and threshold study
│   └── 02_ml_pricing_model.ipynb     # Pricing model, MLflow tracking
├── api/                              # FastAPI prediction service
│   ├── main.py
│   ├── test_api.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── models/                       # Trained model + encoders (.joblib)
├── streamlit_app/                    # Streamlit dashboard
│   ├── app.py
│   ├── requirements.txt
│   └── data/                         # Dataset (self-contained for deployment)
├── models/                           # Trained model artifacts
├── data/                             # Datasets
└── LICENSE
```

## Dataset

Getaround course dataset (publicly available, anonymized rental records):

- `get_around_pricing_project.csv`: car features used for price prediction.
- `get_around_delay_analysis.xlsx`: rental delay observations used for the threshold study.

The datasets are intentionally duplicated under `data/` and `streamlit_app/data/` so that each
deployable component (FastAPI service, Streamlit app) is self-contained.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional, for the API and containerized runs)

### Run the dashboard locally

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

### Run the API locally

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 7860
# or: docker build -t getaround-api . && docker run -p 7860:7860 getaround-api
```

## Results

Four regressors were trained and compared with MLflow on the pricing task. Metrics are the test-set
R-squared logged during training:

| Model                 | Test R2   |
|-----------------------|-----------|
| **Gradient Boosting** | **0.726** |
| Random Forest         | 0.723     |
| Linear Regression     | 0.668     |
| Ridge                 | 0.668     |

Gradient Boosting was selected and serialized as the production model used by the API and the
dashboard.

## Deployment

Both components are deployed on Hugging Face Spaces (Docker-based):

- **Prediction API**: https://yatimai-getaround-api.hf.space
- **Dashboard**: https://yatimai-getaround-dashboard.hf.space

Each component is self-contained (its own datasets and model artifacts), so the directories
`api/` and `streamlit_app/` can be deployed independently. On the free tier, Spaces may sleep
after inactivity and wake on the first request.

## Design Notes

- **Delay analysis**: the threshold study quantifies the trade-off between reducing friction for
  the next driver and the share of rentals affected by a minimum-delay rule.
- **Model choice**: Gradient Boosting edges out Random Forest and clearly beats the linear
  baselines, capturing non-linear interactions between car features and price.
- **MLflow**: every candidate model is tracked with its parameters and metrics, making the
  comparison reproducible rather than ad hoc.

## License

MIT
