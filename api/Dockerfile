FROM python:3.11-slim

WORKDIR /app

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY main.py .

# Copier les modèles
COPY models ./models

# Exposer le port (Hugging Face utilise 7860)
EXPOSE 7860

# Lancer l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
