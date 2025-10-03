# 🎯 Test de l'authentification avec Swagger

## 📦 Ce qui a été créé pour vous

Vous disposez maintenant de **3 méthodes professionnelles** pour tester l'API avec Swagger/OpenAPI :

### 1. 🌐 Swagger Editor (EN LIGNE) - ⭐ RECOMMANDÉ

La méthode la plus simple et rapide !

**Étapes :**
1. Ouvrir : **https://editor.swagger.io**
2. Copier tout le contenu du fichier `openapi.yaml` (à la racine du projet)
3. Coller dans Swagger Editor (Ctrl+A, Ctrl+V)
4. Sélectionner le serveur : `http://localhost:8080` (menu déroulant en haut)
5. Tester les endpoints !

**Tutoriel détaillé :** Voir `docs/SWAGGER_QUICKSTART.md`

---

### 2. 🐳 Swagger UI Docker (LOCAL)

Interface Swagger dédiée sur votre machine.

```powershell
# Lancer Swagger UI
docker run -d --name swagger-ui -p 8081:8080 `
  -e SWAGGER_JSON=/openapi.yaml `
  -v ${PWD}/openapi.yaml:/openapi.yaml `
  swaggerapi/swagger-ui

# Accédez à : http://localhost:8081
```

Pour arrêter :
```powershell
docker stop swagger-ui && docker rm swagger-ui
```

---

### 3. 📮 Postman - ⭐ TESTS AUTOMATIQUES

Collection complète avec tests automatiques intégrés.

**Import dans Postman :**
1. Importer `postman/ops-portal.postman_collection.json`
2. Importer `postman/ops-portal.postman_environment.json`
3. Sélectionner l'environnement "OPS Portal - Local"
4. Lancer les requêtes (les tokens sont sauvegardés automatiquement !)

---

## 🚀 Démarrage rapide (Swagger Editor)

### Prérequis
```powershell
# Assurez-vous que le port-forward est actif
kubectl -n ops port-forward svc/ops-portal 8080:80
```

### Test en 5 minutes

1. **Ouvrir Swagger Editor** : https://editor.swagger.io

2. **Charger l'API** :
   - Copier `openapi.yaml` (racine du projet)
   - Coller dans l'éditeur

3. **Se connecter** :
   ```json
   POST /auth/login
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
   → Copier le token JWT

4. **Autoriser** :
   - Cliquer "Authorize" 🔒
   - Entrer : `Bearer <votre_token>`
   - Cliquer "Authorize"

5. **Tester** :
   - `GET /api/status` → 200 OK
   - `POST /api/deploy` → 202 Accepted

---

## 👥 Utilisateurs de test

| Username | Password | Rôles | Accès |
|----------|----------|-------|-------|
| `alice` | `alice123` | ops | `/api/status` ✅<br>`/api/deploy` ❌ |
| `admin` | `admin123` | admin, ops | `/api/status` ✅<br>`/api/deploy` ✅ |

---

## 📚 Documentation complète

- **Guide rapide** : `docs/SWAGGER_QUICKSTART.md`
- **Tutoriel détaillé** : `docs/SWAGGER.md`
- **Récapitulatif** : `SWAGGER_TESTING.md`
- **Spécification OpenAPI** : `openapi.yaml`

---

## 🎓 Pourquoi ces 3 méthodes ?

### Swagger Editor (en ligne)
- ✅ Aucune installation
- ✅ Interface intuitive
- ✅ Immédiat
- ❌ Requiert Internet

### Swagger UI Docker
- ✅ Interface complète
- ✅ Local (pas d'Internet)
- ✅ Professionnel
- ❌ Port 8081 utilisé

### Postman
- ✅ Tests automatiques
- ✅ Gestion des tokens
- ✅ Export/Import facile
- ❌ Application à installer

**Choisissez celle qui vous convient !** 🎯

---

## ✅ Checklist de test

- [ ] Port-forward actif (`kubectl -n ops port-forward svc/ops-portal 8080:80`)
- [ ] Swagger Editor ouvert avec `openapi.yaml`
- [ ] Login réussi (alice ou admin)
- [ ] Token copié et configuré dans "Authorize"
- [ ] GET `/api/status` → 200 OK
- [ ] POST `/api/deploy` avec admin → 202 Accepted

**Tous les tests passent ?** ✅ Votre API fonctionne parfaitement !

---

## 🐛 Problèmes ?

### Port-forward non actif
```powershell
kubectl -n ops get pods  # Vérifier que les pods tournent
kubectl -n ops port-forward svc/ops-portal 8080:80
```

### Token expiré (401)
- Les tokens expirent après 1 heure
- Reconnectez-vous via `/auth/login`

### 403 Forbidden sur /api/deploy
- Normal si vous utilisez alice (rôle ops seulement)
- Utilisez admin (rôles admin + ops)

---

**Besoin d'aide ?** Consultez `docs/SWAGGER_QUICKSTART.md` pour un tutoriel pas-à-pas complet ! 📖
