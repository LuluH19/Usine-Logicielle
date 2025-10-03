# 🎯 Guide de Test - API OPS Portal avec Swagger

## ✅ Ce qui est disponible

### 📄 Documentation OpenAPI 3.0.3
- Fichier : `openapi.yaml` (racine du projet)
- Spécification complète de l'API
- Prêt à être importé dans n'importe quel outil

### 📦 Collection Postman
- Fichier : `postman/ops-portal.postman_collection.json`
- Environnement : `postman/ops-portal.postman_environment.json`
- Tests automatiques inclus
- Gestion automatique des tokens JWT

## 🚀 3 Méthodes pour tester avec Swagger

### ✨ Méthode 1 : Swagger Editor (RECOMMANDÉ)

**La plus simple et la plus rapide !**

1. Ouvrez votre navigateur : **[https://editor.swagger.io](https://editor.swagger.io)**
   
2. **Copiez le contenu** du fichier `openapi.yaml` (vous pouvez l'ouvrir dans VS Code)

3. **Collez** dans Swagger Editor (remplace le contenu existant)

4. **Changez le serveur** :
   - En haut à droite, sélectionnez le serveur dropdown
   - Choisissez `http://localhost:8080`

5. **Testez !** :
   - Dépliez `POST /auth/login`
   - Cliquez "Try it out"
   - Credentials : `alice` / `alice123` ou `admin` / `admin123`
   - Cliquez "Execute"
   - Copiez le token JWT

6. **Authentifiez-vous** :
   - Cliquez le bouton "Authorize" 🔒 en haut
   - Entrez : `Bearer <votre_token>`
   - Cliquez "Authorize" puis "Close"

7. **Testez les endpoints protégés** :
   - `GET /api/status`
   - `POST /api/deploy` (admin seulement)

---

### 🐳 Méthode 2 : Swagger UI en local (Docker)

**Interface Swagger dédiée sur votre machine**

```powershell
# Lancer Swagger UI
cd "C:\Users\33781\Usine Logicielle"
docker run -d --name swagger-ui -p 8081:8080 `
  -e SWAGGER_JSON=/openapi.yaml `
  -v ${PWD}/openapi.yaml:/openapi.yaml `
  swaggerapi/swagger-ui

# Accédez à : http://localhost:8081
```

**Pour arrêter :**
```powershell
docker stop swagger-ui
docker rm swagger-ui
```

---

### 📮 Méthode 3 : Postman (Tests automatisés)

**La plus professionnelle**

1. Ouvrez **Postman**

2. **Importez la collection** :
   - File → Import
   - Sélectionnez `postman/ops-portal.postman_collection.json`

3. **Importez l'environnement** :
   - Cliquez sur l'icône "Environments" (à gauche)
   - Import
   - Sélectionnez `postman/ops-portal.postman_environment.json`

4. **Sélectionnez l'environnement** :
   - En haut à droite, choisissez "OPS Portal - Local"

5. **Exécutez les requêtes** :
   - Folder "Authentication" → "Login - Alice (ops)" → Send
   - Le token est **automatiquement sauvegardé**
   - Folder "API - Protected Endpoints" → testez les endpoints

6. **Tests automatiques** :
   - Chaque requête inclut des assertions
   - Vérifiez l'onglet "Test Results" après chaque requête

---

## 📊 Comparaison des méthodes

| Méthode | Avantages | Inconvénients |
|---------|-----------|---------------|
| **Swagger Editor** | ✅ Aucune installation<br>✅ Interface intuitive<br>✅ Immédiat | ❌ En ligne (Internet requis) |
| **Swagger UI Docker** | ✅ Interface complète<br>✅ Local<br>✅ Pas d'Internet | ❌ Nécessite Docker<br>❌ Port 8081 |
| **Postman** | ✅ Tests automatiques<br>✅ Gestion tokens<br>✅ Professionnel | ❌ Installation requise<br>❌ Courbe d'apprentissage |

---

## 🎓 Tutoriel pas-à-pas : Premier test avec Swagger Editor

### Étape 1 : Ouvrir l'éditeur
```
https://editor.swagger.io
```

### Étape 2 : Charger votre API
1. Ctrl+A pour tout sélectionner
2. Supprimer
3. Ouvrir `openapi.yaml` dans VS Code
4. Copier tout le contenu (Ctrl+A, Ctrl+C)
5. Coller dans Swagger Editor (Ctrl+V)

### Étape 3 : Configurer le serveur
- Menu déroulant en haut : sélectionnez `http://localhost:8080`

### Étape 4 : Se connecter
```yaml
POST /auth/login
Body:
{
  "username": "admin",
  "password": "admin123"
}
```
**Résultat attendu** : Code 200 + token JWT

### Étape 5 : Copier le token
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcH...
```

### Étape 6 : Autoriser
1. Bouton "Authorize" 🔒 en haut
2. Entrer : `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. Cliquez "Authorize"

### Étape 7 : Tester un endpoint protégé
```yaml
GET /api/status
```
**Résultat attendu** : Code 200 + données CI, artifacts, monitor

### Étape 8 : Tester avec permissions admin
```yaml
POST /api/deploy
```
**Résultat attendu** : Code 202 + `deployment_run_id`

---

## 🐛 Troubleshooting

### ❌ "Failed to fetch"
- Vérifiez que le port-forward est actif :
  ```powershell
  kubectl -n ops port-forward svc/ops-portal 8080:80
  ```

### ❌ "401 Unauthorized"
- Token expiré (durée : 1 heure)
- Reconnectez-vous via `/auth/login`
- Mettez à jour l'autorisation

### ❌ "403 Forbidden"
- Alice ne peut pas accéder à `/api/deploy`
- Utilisez admin : `admin` / `admin123`

### ❌ CORS Error
- Swagger Editor en ligne peut avoir des problèmes CORS
- Solution : Utilisez Swagger UI Docker (méthode 2)

---

## 📚 Ressources

- **Documentation complète** : `docs/SWAGGER.md`
- **Spécification OpenAPI** : `openapi.yaml`
- **Collection Postman** : `postman/ops-portal.postman_collection.json`
- **Swagger Editor** : https://editor.swagger.io
- **Swagger UI Image** : https://hub.docker.com/r/swaggerapi/swagger-ui

---

## ✅ Checklist de test

- [ ] L'application tourne (port-forward actif)
- [ ] Swagger Editor ouvert avec `openapi.yaml` chargé
- [ ] Serveur configuré sur `http://localhost:8080`
- [ ] Login alice réussi (200)
- [ ] Token copié et configuré dans "Authorize"
- [ ] GET /api/status réussi (200)
- [ ] POST /api/deploy échoue avec alice (403) ✅ Normal !
- [ ] Login admin réussi (200)
- [ ] Nouveau token admin configuré
- [ ] POST /api/deploy réussi avec admin (202)

**Si tous les tests passent : ✅ Votre API fonctionne parfaitement !**
