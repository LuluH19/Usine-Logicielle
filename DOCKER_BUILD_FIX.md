# 🐳 Configuration Docker Build & GHCR

## ❌ Problème résolu

**Erreur initiale :**
```
ERROR: failed to build: Cache export is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
```

### Cause
Le **driver Docker par défaut** ne supporte pas :
- ❌ Export de cache vers le registry
- ❌ Multi-platform builds
- ❌ Cache layer avancé

## ✅ Solution implémentée

### 1. Configuration Docker Buildx

Ajout de `driver-opts` dans tous les workflows :

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    driver-opts: |
      image=moby/buildkit:latest
```

**Avantages :**
- ✅ Supporte le cache GHA (GitHub Actions)
- ✅ Multi-platform builds (amd64, arm64)
- ✅ Performance optimale avec BuildKit

### 2. Utilisation du cache GitHub Actions

Au lieu du cache registry (`type=registry`), on utilise le **cache GHA** :

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

**Bénéfices :**
- ✅ Gratuit pour les repos publics/privés GitHub
- ✅ Intégré nativement à GitHub Actions
- ✅ Pas besoin de credentials supplémentaires
- ✅ Performance optimale

## 📦 Workflows créés/modifiés

### 1. `.github/workflows/ci.yml` (modifié)

**Job `build` :**
- Utilise Docker Buildx avec BuildKit
- Cache GHA au lieu de registry
- Ajoute `load: true` pour charger l'image après le build
- Tags simplifiés : `ops-portal:test`

### 2. `.github/workflows/docker-publish.yml` (nouveau)

**Workflow dédié au push GHCR :**
- Se déclenche sur push vers `main`
- Push vers `ghcr.io/LuluH19/Usine-Logicielle/ops-portal`
- Tags multiples : `latest`, `sha`, `branch`
- Multi-platform : linux/amd64, linux/arm64
- Scan de vulnérabilités avec Trivy

**Déclencheurs :**
```yaml
on:
  push:
    branches: [ main ]
    tags:
      - 'v*.*.*'
  workflow_dispatch:  # Déclenchement manuel possible
```

## 🚀 Utilisation

### Build local avec Buildx

```bash
# Créer un builder (une seule fois)
docker buildx create --name ops-builder --use

# Build avec cache
docker buildx build \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  --tag ops-portal:dev \
  --load \
  .
```

### Push vers GHCR manuellement

```bash
# Login GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u LuluH19 --password-stdin

# Tag l'image
docker tag ops-portal:dev ghcr.io/LuluH19/Usine-Logicielle/ops-portal:latest

# Push
docker push ghcr.io/LuluH19/Usine-Logicielle/ops-portal:latest
```

### Déclencher le workflow manuellement

Sur GitHub :
1. Aller dans **Actions**
2. Sélectionner **Docker Publish to GHCR**
3. Cliquer sur **Run workflow**
4. Choisir la branche `main`

## 📊 Comparaison des types de cache

| Type | Avantages | Inconvénients |
|------|-----------|---------------|
| **type=gha** | ✅ Gratuit<br>✅ Rapide<br>✅ Intégré GitHub | ❌ Uniquement GitHub Actions |
| **type=registry** | ✅ Universel<br>✅ Partageable | ❌ Coûteux<br>❌ Nécessite driver spécial |
| **type=local** | ✅ Simple | ❌ Non partageable<br>❌ Lent |
| **type=inline** | ✅ Simple | ❌ Augmente la taille d'image |

## 🔐 Permissions GHCR

Le workflow a besoin de ces permissions :

```yaml
permissions:
  contents: read
  packages: write
```

**Automatiquement fourni par `GITHUB_TOKEN` :**
- ✅ Lecture du code source
- ✅ Écriture dans GitHub Container Registry
- ✅ Upload des résultats de sécurité (Trivy)

## 🛡️ Sécurité

### Scan Trivy intégré

Chaque image buildée est scannée pour :
- CVE (Common Vulnerabilities and Exposures)
- Dépendances vulnérables
- Configurations dangereuses

**Résultats uploadés vers :**
- GitHub Security → Code scanning alerts
- Visible dans l'onglet **Security** du repo

## 📈 Optimisations appliquées

### 1. Multi-stage build (Dockerfile)
```dockerfile
# Builder stage
FROM python:3.12-slim AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
```

### 2. Layer caching optimal
- Dependencies installées en premier (changent rarement)
- Code copié en dernier (change souvent)

### 3. Mode cache `max`
```yaml
cache-to: type=gha,mode=max
```
- Cache **tous les layers** intermédiaires
- Pas seulement le résultat final

## 🎯 Résultat attendu

### CI Pipeline (ci.yml)
```
✅ test (Python 3.11)
✅ test (Python 3.12)
✅ lint
✅ build
   └─ Build Docker image
   └─ Test /healthz endpoint
```

### GHCR Pipeline (docker-publish.yml)
```
✅ Build and push Docker image
   ├─ Build for linux/amd64
   ├─ Build for linux/arm64
   ├─ Push to ghcr.io
   ├─ Tags: latest, sha, main
   └─ Scan vulnerabilities with Trivy
```

## 📝 Tags générés automatiquement

Pour un commit `945f786` sur `main` :
- `ghcr.io/LuluH19/Usine-Logicielle/ops-portal:latest`
- `ghcr.io/LuluH19/Usine-Logicielle/ops-portal:main`
- `ghcr.io/LuluH19/Usine-Logicielle/ops-portal:main-945f786`

Pour un tag `v1.2.3` :
- `ghcr.io/LuluH19/Usine-Logicielle/ops-portal:1.2.3`
- `ghcr.io/LuluH19/Usine-Logicielle/ops-portal:1.2`
- `ghcr.io/LuluH19/Usine-Logicielle/ops-portal:v1.2.3`

## 🔗 Références

- [Docker Buildx Documentation](https://docs.docker.com/buildx/working-with-buildx/)
- [GitHub Actions Cache](https://docs.docker.com/build/ci/github-actions/cache/)
- [GHCR Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [BuildKit Backend](https://docs.docker.com/build/buildkit/)

---

**✅ Les workflows sont maintenant configurés pour supporter le cache Docker correctement !**
