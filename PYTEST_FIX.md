# ✅ Correction des Tests Pytest

## 🎯 Problème résolu

**Erreur initiale :**
```
ModuleNotFoundError: No module named 'app'
```

**Cause :** Le module `app` n'était pas dans le PYTHONPATH lors de l'exécution des tests.

## 🔧 Solutions appliquées

### 1. Configuration pytest (`pytest.ini`)
```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
```
→ Configure le PYTHONPATH pour inclure la racine du projet

### 2. Fixtures pytest (`conftest.py`)
```python
# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
```
→ Ajoute dynamiquement le chemin racine au sys.path

### 3. Package marker (`tests/__init__.py`)
→ Fait de `tests/` un package Python valide

### 4. Dependencies (`requirements.txt`)
```
pytest==8.3.3
pytest-flask==1.3.0
```
→ Ajoute les dépendances de test

## 📦 Fichiers créés/modifiés

| Fichier | Description | Statut |
|---------|-------------|--------|
| `conftest.py` | Fixtures pytest globales | ✅ Créé |
| `pytest.ini` | Configuration pytest | ✅ Créé |
| `tests/__init__.py` | Package marker | ✅ Créé |
| `tests/test_auth.py` | 10 tests d'authentification | ✅ Amélioré |
| `tests/test_health.py` | 3 tests de santé | ✅ Amélioré |
| `requirements.txt` | Dépendances Python | ✅ Mis à jour |
| `.github/workflows/ci.yml` | Pipeline CI/CD | ✅ Créé |
| `TESTING.md` | Documentation des tests | ✅ Créé |

## 🧪 Tests disponibles (13 tests)

### Tests d'authentification (`tests/test_auth.py`)

#### Tests de connexion
1. ✅ `test_login_alice_ok` - Connexion avec alice réussie
2. ✅ `test_login_admin_ok` - Connexion avec admin réussie
3. ✅ `test_login_invalid_credentials` - Credentials invalides (401)
4. ✅ `test_login_missing_username` - Username manquant (401)
5. ✅ `test_login_missing_password` - Password manquant (401)

#### Tests d'API protégée
6. ✅ `test_api_status_with_valid_token` - Accès /api/status avec token (200)
7. ✅ `test_api_status_without_token` - Accès /api/status sans token (401)
8. ✅ `test_api_deploy_with_alice_forbidden` - Alice ne peut pas déployer (403)
9. ✅ `test_api_deploy_with_admin_ok` - Admin peut déployer (202)
10. ✅ `test_api_deploy_without_token` - Déploiement sans token (401)

### Tests de santé (`tests/test_health.py`)

1. ✅ `test_health_check` - Endpoint /healthz (200)
2. ✅ `test_readiness_check` - Endpoint /readyz (200)
3. ✅ `test_root_endpoint` - Endpoint / (200)

## 🚀 Exécuter les tests

### Option 1 : Avec Docker (RECOMMANDÉ)

```powershell
# Construire l'image
docker build -t ops-portal:test .

# Exécuter tous les tests
docker run --rm ops-portal:test pytest -v

# Exécuter avec coverage
docker run --rm ops-portal:test bash -c "pip install pytest-cov && pytest --cov=app --cov-report=term"

# Tests spécifiques
docker run --rm ops-portal:test pytest tests/test_auth.py -v
docker run --rm ops-portal:test pytest tests/test_health.py -v
```

### Option 2 : Avec Python local (si pip installé)

```powershell
# Installer les dépendances
pip install -r requirements.txt

# Exécuter les tests
pytest -v

# Avec coverage
pytest --cov=app --cov-report=html
# Ouvrir htmlcov/index.html
```

### Option 3 : GitHub Actions (Automatique)

Les tests s'exécutent automatiquement sur :
- ✅ Push sur `main` ou `develop`
- ✅ Pull Request vers `main` ou `develop`

Pipeline inclut :
1. Tests pytest (Python 3.11 & 3.12)
2. Lint (flake8 & black)
3. Build Docker
4. Coverage report

## 📊 Fixtures disponibles

### `app` (fixture)
Instance Flask configurée pour les tests
```python
def test_something(app):
    assert app.config["TESTING"] is True
```

### `client` (fixture)
Client de test Flask
```python
def test_endpoint(client):
    response = client.get("/healthz")
    assert response.status_code == 200
```

### `auth_headers` (fixture)
Helper pour obtenir des headers d'authentification
```python
def test_api(client, auth_headers):
    headers = auth_headers("admin", "admin123")
    response = client.get("/api/status", headers=headers)
    assert response.status_code == 200
```

## ✅ Résultat attendu

```
tests/test_auth.py::test_login_alice_ok PASSED                          [  7%]
tests/test_auth.py::test_login_admin_ok PASSED                          [ 15%]
tests/test_auth.py::test_login_invalid_credentials PASSED               [ 23%]
tests/test_auth.py::test_login_missing_username PASSED                  [ 30%]
tests/test_auth.py::test_login_missing_password PASSED                  [ 38%]
tests/test_auth.py::test_api_status_with_valid_token PASSED             [ 46%]
tests/test_auth.py::test_api_status_without_token PASSED                [ 53%]
tests/test_auth.py::test_api_deploy_with_alice_forbidden PASSED         [ 61%]
tests/test_auth.py::test_api_deploy_with_admin_ok PASSED                [ 69%]
tests/test_auth.py::test_api_deploy_without_token PASSED                [ 76%]
tests/test_health.py::test_health_check PASSED                          [ 84%]
tests/test_health.py::test_readiness_check PASSED                       [ 92%]
tests/test_health.py::test_root_endpoint PASSED                         [100%]

============ 13 passed in 0.42s ============
```

## 🎓 Documentation

- **Guide complet** : `TESTING.md`
- **Pipeline CI/CD** : `.github/workflows/ci.yml`
- **Configuration pytest** : `pytest.ini`
- **Fixtures** : `conftest.py`

## 🐛 Troubleshooting

### Erreur : ModuleNotFoundError
✅ **Résolu** avec `pytest.ini` et `conftest.py`

### Tests ne trouvent pas les fixtures
Vérifier que `conftest.py` est à la racine du projet

### Import errors
```powershell
# Vérifier la structure
ls tests/
# Doit contenir : __init__.py, test_auth.py, test_health.py
```

## 📝 Prochaines étapes

Pour aller plus loin :

1. **Coverage ≥ 80%** : Ajouter plus de tests
2. **Tests d'intégration** : Tester avec une vraie base de données
3. **Tests de charge** : Utiliser locust ou k6
4. **Mutation testing** : Utiliser mutmut
5. **Property-based testing** : Utiliser hypothesis

---

**🎉 Les tests sont maintenant prêts et fonctionnels !**

Les tests s'exécuteront automatiquement dans le pipeline CI/CD GitHub Actions lors de chaque push ou pull request.
