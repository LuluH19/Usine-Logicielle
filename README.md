# Ops Portal - Mini-portail d'Usine Logicielle

Portail d'opérations pour une usine logicielle, développé en Flask et déployé sur Kubernetes/OpenShift.

## 🎯 Fonctionnalités

- 🔎 Statut de l'usine (CI/CD, artefacts, monitors)
- 🚀 Actions OPS (déploiements, purge cache, redémarrage services)
- 🔐 Authentification JWT + RBAC (ops, admin)
- 📈 Health/readiness/metrics Prometheus

## 🛠️ Stack technique

- Flask + Gunicorn
- JWT pour l'authentification
- Docker
- Kubernetes/OpenShift
- Helm
- GitHub Actions (CI/CD)
- Prometheus/Grafana

## 🚀 Démarrage rapide

### Local

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -c "from app import create_app; create_app().run(port=8080)"
```

### Docker

```bash
docker build -t ops-portal:dev .
docker run -p 8080:8080 ops-portal:dev
```

### Kubernetes

```bash
# Créer le secret à partir de l'exemple
cp k8s/secret.example.yaml k8s/secret.yaml
# Éditer k8s/secret.yaml avec vos valeurs

# Déployer
kubectl apply -f k8s/namespace.yaml
kubectl -n ops apply -f k8s/configmap.yaml
kubectl -n ops apply -f k8s/secret.yaml
sed "s/{{TAG}}/dev/" k8s/deployment.yaml | kubectl -n ops apply -f -
kubectl -n ops apply -f k8s/service.yaml k8s/ingress.yaml
```

### Helm

```bash
helm install ops-portal ./helm/ops-portal -n ops --create-namespace
```

## 🔐 API

### Authentification

```bash
# Login
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"alice123"}'

# Réponse: {"token": "eyJ..."}
```

### Endpoints protégés

```bash
# Statut (role: ops)
curl http://localhost:8080/api/status \
  -H "Authorization: Bearer <token>"

# Déploiement (role: admin)
curl -X POST http://localhost:8080/api/deploy \
  -H "Authorization: Bearer <token>"
```

### Utilisateurs par défaut

- `alice` / `alice123` (role: ops)
- `admin` / `admin123` (roles: admin, ops)

## 📊 Monitoring

- Health: `GET /healthz`
- Readiness: `GET /readyz`
- Metrics Prometheus: `GET /metrics`

## 🧪 Tests

### Exécuter les tests

```bash
# Avec Docker (RECOMMANDÉ)
docker build -t ops-portal:test .
docker run --rm ops-portal:test pytest -v

# Avec Python local (si pip installé)
pip install -r requirements.txt
pytest -v

# Avec coverage
pytest --cov=app --cov-report=html
```

### Tests disponibles

- **13 tests** au total
- `tests/test_auth.py` : 10 tests d'authentification et autorisation
- `tests/test_health.py` : 3 tests des endpoints de santé

**Documentation** : Voir `PYTEST_FIX.md` et `TESTING.md`

## 📖 Documentation Swagger/OpenAPI

### Tester l'API avec Swagger

**3 méthodes disponibles :**

1. **Swagger Editor (EN LIGNE)** ⭐ RECOMMANDÉ
   - Ouvrir : [https://editor.swagger.io](https://editor.swagger.io)
   - Copier le contenu de `openapi.yaml`
   - Coller dans l'éditeur
   - Sélectionner serveur `http://localhost:8080`

2. **Swagger UI Docker (LOCAL)**
   ```bash
   docker run -d --name swagger-ui -p 8081:8080 \
     -e SWAGGER_JSON=/openapi.yaml \
     -v ${PWD}/openapi.yaml:/openapi.yaml \
     swaggerapi/swagger-ui
   # Accès : http://localhost:8081
   ```

3. **Postman** ⭐ TESTS AUTOMATIQUES
   - Importer `postman/ops-portal.postman_collection.json`
   - Importer `postman/ops-portal.postman_environment.json`

**Documentation détaillée** : `SWAGGER_README.md`, `SWAGGER_TESTING.md`, `docs/SWAGGER_QUICKSTART.md`

## 🔧 Makefile

```bash
make run          # Lancer en local
make build        # Build Docker
make push         # Push vers registry
make k3d-apply    # Déployer sur K8s
make test         # Lancer les tests
```

## 📁 Structure

```
ops-portal/
├─ app/                    # Backend Flask
│  ├─ __init__.py
│  ├─ api.py              # Routes API
│  ├─ auth.py             # JWT + RBAC
│  ├─ metrics.py          # Prometheus
│  └─ services/           # Services métier
├─ tests/                 # Tests pytest
├─ k8s/                   # Manifests Kubernetes
├─ helm/ops-portal/       # Chart Helm
├─ .github/workflows/     # CI/CD
└─ Dockerfile
```

## 🚀 CI/CD

Le pipeline GitHub Actions :
1. Build & test (pytest)
2. Build & push Docker image vers GHCR
3. Deploy sur Kubernetes (branche main uniquement)

Configuration requise :
- Secret `KUBECONFIG_CONTENT` dans GitHub

## 🔐 Sécurité

- Secrets via Kubernetes Secret
- JWT avec expiration
- RBAC (ops/admin)
- TLS via Ingress/Route
- Resource limits sur les pods

## 📈 Roadmap

- [ ] UI React pour le portail
- [ ] Intégrations réelles (GitLab, Jenkins, Nexus)
- [ ] OpenTelemetry (traces/logs)
- [ ] Operator Kubernetes pour automatisation
- [ ] Multi-environnements (dev/preprod/prod)

## 📝 Notes OpenShift

Pour OpenShift, utilisez `k8s/route-openshift.yaml` au lieu de `k8s/ingress.yaml` :

```bash
kubectl -n ops apply -f k8s/route-openshift.yaml
```
