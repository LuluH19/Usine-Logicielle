# Script de test local pour valider les tests pytest

## Prérequis
- Docker installé
- Image ops-portal construite

## Tester localement avec Docker

### Option 1 : Tests dans un conteneur temporaire
```powershell
# Reconstruire l'image avec les dépendances de test
docker build -t ops-portal:test .

# Exécuter les tests dans le conteneur
docker run --rm ops-portal:test pytest -v

# Ou avec plus de détails
docker run --rm ops-portal:test pytest -v --tb=short
```

### Option 2 : Tests avec montage du code source
```powershell
# Lancer un conteneur avec le code source monté
docker run --rm -it `
  -v ${PWD}/app:/app/app `
  -v ${PWD}/tests:/app/tests `
  -v ${PWD}/conftest.py:/app/conftest.py `
  -v ${PWD}/pytest.ini:/app/pytest.ini `
  ops-portal:test `
  pytest -v

# Avec coverage
docker run --rm -it `
  -v ${PWD}:/app `
  ops-portal:test `
  bash -c "pip install pytest-cov && pytest --cov=app --cov-report=term"
```

### Option 3 : Shell interactif dans le conteneur
```powershell
docker run --rm -it ops-portal:test bash

# Puis dans le conteneur :
pytest -v
pytest tests/test_auth.py -v
pytest tests/test_health.py -v
```

## Tests disponibles

### Tests d'authentification (tests/test_auth.py)
- ✅ `test_login_alice_ok` - Connexion avec alice
- ✅ `test_login_admin_ok` - Connexion avec admin
- ✅ `test_login_invalid_credentials` - Mauvais mot de passe
- ✅ `test_login_missing_username` - Username manquant
- ✅ `test_login_missing_password` - Mot de passe manquant
- ✅ `test_api_status_with_valid_token` - Accès /api/status avec token
- ✅ `test_api_status_without_token` - Accès /api/status sans token
- ✅ `test_api_deploy_with_alice_forbidden` - Alice ne peut pas déployer
- ✅ `test_api_deploy_with_admin_ok` - Admin peut déployer

### Tests de santé (tests/test_health.py)
- ✅ `test_health_check` - Endpoint /healthz
- ✅ `test_readiness_check` - Endpoint /readyz
- ✅ `test_root_endpoint` - Endpoint /

## CI/CD GitHub Actions

Le fichier `.github/workflows/ci.yml` a été créé avec :
- Tests automatiques sur push/PR
- Support Python 3.11 et 3.12
- Linting avec flake8 et black
- Build Docker
- Coverage report

## Structure des fichiers de test

```
Usine Logicielle/
├── conftest.py              # Configuration pytest et fixtures
├── pytest.ini               # Configuration pytest
├── tests/
│   ├── __init__.py         # Package marker
│   ├── test_auth.py        # Tests d'authentification (10 tests)
│   └── test_health.py      # Tests de santé (3 tests)
└── .github/
    └── workflows/
        └── ci.yml          # Pipeline CI/CD
```

## Exécution des tests

### Commandes rapides
```powershell
# Tous les tests
pytest -v

# Tests spécifiques
pytest tests/test_auth.py -v
pytest tests/test_health.py -v

# Avec coverage
pytest --cov=app --cov-report=html
# Ouvrir htmlcov/index.html

# Tests en mode quiet
pytest -q

# Tests avec output détaillé
pytest -vv --tb=short
```

## Résultats attendus

```
tests/test_auth.py::test_login_alice_ok PASSED
tests/test_auth.py::test_login_admin_ok PASSED
tests/test_auth.py::test_login_invalid_credentials PASSED
tests/test_auth.py::test_login_missing_username PASSED
tests/test_auth.py::test_login_missing_password PASSED
tests/test_auth.py::test_api_status_with_valid_token PASSED
tests/test_auth.py::test_api_status_without_token PASSED
tests/test_auth.py::test_api_deploy_with_alice_forbidden PASSED
tests/test_auth.py::test_api_deploy_with_admin_ok PASSED
tests/test_health.py::test_health_check PASSED
tests/test_health.py::test_readiness_check PASSED
tests/test_health.py::test_root_endpoint PASSED

============ 12 passed in 0.25s ============
```

## Fixtures disponibles (conftest.py)

- `app` - Instance Flask configurée pour les tests
- `client` - Client de test Flask
- `runner` - CLI runner Flask
- `auth_headers(username, password)` - Helper pour obtenir des headers avec JWT

## Troubleshooting

### ModuleNotFoundError: No module named 'app'
✅ Résolu avec `pytest.ini` et `conftest.py`

### Tests ne s'exécutent pas
```powershell
# Vérifier l'installation pytest
docker run --rm ops-portal:test pip list | grep pytest

# Vérifier la structure
docker run --rm ops-portal:test ls -la tests/
```

### Erreurs d'import
```powershell
# Vérifier le PYTHONPATH
docker run --rm ops-portal:test python -c "import sys; print(sys.path)"
```
