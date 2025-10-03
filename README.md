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

```bash
pip install pytest
pytest -q
```

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
