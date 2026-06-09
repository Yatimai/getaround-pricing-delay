"""
Script de test pour l'API Getaround Pricing
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_root():
    """Test endpoint racine"""
    print("Test 1: Endpoint racine (/)")
    print("-" * 50)
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_health():
    """Test health check"""
    print("Test 2: Health check (/health)")
    print("-" * 50)
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_model_info():
    """Test informations modele"""
    print("Test 3: Model info (/model-info)")
    print("-" * 50)
    response = requests.get(f"{API_URL}/model-info")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Model type: {data['model_type']}")
        print(f"Number of features: {data['n_features']}")
    print()

def test_predict():
    """Test prediction"""
    print("Test 4: Prediction (/predict)")
    print("-" * 50)

    car_data = {
        "input": [[5, 150000, 120, 0, 1, 2, 1, 1, 1, 0, 1, 1, 1]]
    }

    print("Input:")
    print(json.dumps(car_data, indent=2))

    response = requests.post(f"{API_URL}/predict", json=car_data)
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        prediction = response.json()['prediction'][0]
        print(f"[OK] Prix predit: {prediction} euros/jour")
    else:
        print(f"[ERREUR] Erreur: {response.json()}")
    print()

def test_batch_predict():
    """Test prediction batch (plusieurs voitures)"""
    print("Test 5: Prediction batch")
    print("-" * 50)

    cars_data = {
        "input": [
            [5, 150000, 120, 0, 1, 2, 1, 1, 1, 0, 1, 1, 1],
            [3, 50000, 90, 3, 0, 5, 0, 0, 0, 0, 0, 0, 0],
            [10, 80000, 150, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    }

    print(f"Nombre de voitures: {len(cars_data['input'])}")

    response = requests.post(f"{API_URL}/predict", json=cars_data)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        predictions = response.json()['prediction']
        print("\n[OK] Prix predits:")
        for i, prix in enumerate(predictions, 1):
            print(f"  Voiture {i}: {prix} euros/jour")
    else:
        print(f"[ERREUR] Erreur: {response.json()}")
    print()

def run_all_tests():
    """Lancer tous les tests"""
    print("=" * 50)
    print("TESTS DE L'API GETAROUND PRICING")
    print("=" * 50)
    print()

    try:
        test_root()
        test_health()
        test_model_info()
        test_predict()
        test_batch_predict()

        print("=" * 50)
        print("[OK] TOUS LES TESTS TERMINES")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("[ERREUR] Impossible de se connecter a l'API")
        print("Assurez-vous que l'API est lancee:")
        print("   cd api")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"[ERREUR] {e}")

if __name__ == "__main__":
    run_all_tests()
