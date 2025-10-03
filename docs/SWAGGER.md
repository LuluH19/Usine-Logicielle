# Documentation Swagger / OpenAPI pour OPS Portal

## 🎯 Accès à l'interface Swagger UI

L'API OPS Portal expose une interface Swagger interactive pour tester facilement tous les endpoints.

### Accès local
- **Swagger UI** : http://localhost:8080/docs
- **Spécification OpenAPI** : http://localhost:8080/apispec.json
- **Fichier OpenAPI statique** : `openapi.yaml` (à la racine du projet)

## 🔐 Authentification dans Swagger

### Méthode 1 : Via l'interface Swagger UI

1. **Ouvrez Swagger UI** : http://localhost:8080/docs

2. **Testez l'endpoint de login** :
   - Dépliez `POST /auth/login`
   - Cliquez sur "Try it out"
   - Entrez les credentials :
     ```json
     {
       "username": "alice",
       "password": "alice123"
     }
     ```
   - Cliquez sur "Execute"
   - **Copiez le token JWT** de la réponse

3. **Configurez l'authentification** :
   - Cliquez sur le bouton **"Authorize"** 🔒 en haut de la page
   - Entrez : `Bearer <votre_token>` (remplacez `<votre_token>` par le token copié)
   - Exemple : `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - Cliquez sur "Authorize"
   - Cliquez sur "Close"

4. **Testez les endpoints protégés** :
   - Tous vos appels incluront maintenant automatiquement le token
   - Testez `GET /api/status` (devrait fonctionner avec alice)
   - Testez `POST /api/deploy` (sera refusé pour alice, nécessite admin)

### Méthode 2 : Utilisateur admin

Pour tester `POST /api/deploy` avec succès :
1. Répétez les étapes ci-dessus mais avec :
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
2. Utilisez le nouveau token admin pour autoriser Swagger
3. Testez `POST /api/deploy` (devrait réussir avec code 202)

## 👥 Utilisateurs de test

| Utilisateur | Mot de passe | Rôles | Accès |
|-------------|--------------|-------|-------|
| alice | alice123 | ops | `/api/status` ✅, `/api/deploy` ❌ |
| admin | admin123 | admin, ops | `/api/status` ✅, `/api/deploy` ✅ |

## 📋 Endpoints disponibles

### Non protégés (pas d'auth requise)
- `GET /` - Informations sur le service
- `GET /healthz` - Health check
- `GET /readyz` - Readiness check
- `GET /docs` - Interface Swagger UI
- `GET /apispec.json` - Spécification OpenAPI JSON

### Authentification
- `POST /auth/login` - Connexion et génération de token JWT

### API protégée (JWT requis)
- `GET /api/status` - Statut du système (rôle: ops)
- `POST /api/deploy` - Déclenchement de déploiement (rôle: admin)

## 🚀 Test rapide via cURL

### 1. Obtenir un token
```bash
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Réponse :
```json
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

### 2. Utiliser le token
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl http://localhost:8080/api/status \
  -H "Authorization: Bearer $TOKEN"

curl -X POST http://localhost:8080/api/deploy \
  -H "Authorization: Bearer $TOKEN"
```

## 🔄 Port-forwarding Kubernetes

Si l'application tourne sur Kubernetes :
```bash
kubectl -n ops port-forward svc/ops-portal 8080:80
```

Puis accédez à : http://localhost:8080/docs

## 📦 Import dans d'autres outils

### Postman
1. Importez le fichier `postman/ops-portal.postman_collection.json`
2. Importez l'environnement `postman/ops-portal.postman_environment.json`
3. Lancez les requêtes dans l'ordre (les tokens sont sauvegardés automatiquement)

### Autres clients API
Importez le fichier `openapi.yaml` dans :
- Insomnia
- Bruno
- Thunder Client (VS Code)
- HTTPie Desktop
- Paw (macOS)

## 🎨 Personnalisation Swagger

Pour personnaliser l'interface Swagger, éditez `app/__init__.py` :
- Modifier `swagger_template` pour changer les infos de base
- Modifier `swagger_config` pour personnaliser l'UI
- Ajouter des tags, descriptions, exemples dans les docstrings des endpoints

## 📝 Notes

- Les tokens JWT expirent après **1 heure** (3600 secondes)
- Après expiration, réauthentifiez-vous pour obtenir un nouveau token
- Les credentials sont en dur dans le code (pour démo uniquement)
- En production, utilisez des variables d'environnement et une base de données

## 🐛 Troubleshooting

### "Authorize" ne fonctionne pas
- Vérifiez que vous avez bien préfixé le token avec `Bearer `
- Format attendu : `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Token expiré (401 Unauthorized)
- Reconnectez-vous via `/auth/login`
- Mettez à jour l'autorisation avec le nouveau token

### 403 Forbidden
- Vérifiez que votre utilisateur a le bon rôle
- alice → rôle "ops" uniquement
- admin → rôles "admin" et "ops"
