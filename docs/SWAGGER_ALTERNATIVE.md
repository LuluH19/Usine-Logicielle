# Test rapide de Swagger UI avec Flask et Flasgger

## Méthode alternative : Documentation OpenAPI statique

Comme Flasgger nécessite une configuration complexe, voici une alternative plus simple et universelle :

### 1. Utiliser Swagger Editor en ligne

1. Ouvrez [Swagger Editor](https://editor.swagger.io/)
2. Copiez le contenu du fichier `openapi.yaml` (à la racine du projet)
3. Collez-le dans Swagger Editor
4. L'interface interactive apparaît instantanément
5. Changez le serveur dans la dropdown vers `http://localhost:8080`
6. Testez directement les endpoints

### 2. Utiliser Swagger UI en local (Docker)

```powershell
# Lancer Swagger UI dans un conteneur Docker
docker run -d -p 8081:8080 \
  -e SWAGGER_JSON=/openapi.yaml \
  -v ${PWD}/openapi.yaml:/openapi.yaml \
  swaggerapi/swagger-ui

# Accédez à : http://localhost:8081
```

### 3. Utiliser Postman (déjà configuré)

La collection Postman créée précédemment offre une meilleure expérience pour tester l'API :
- Import : `postman/ops-portal.postman_collection.json`
- Tests automatiques intégrés
- Variables d'environnement pour les tokens
- Documentation complète

### 4. Tester l'API avec curl/PowerShell

#### Obtenir un token
```powershell
$body = @{ username = "admin"; password = "admin123" } | ConvertTo-Json
$response = Invoke-WebRequest -Uri http://localhost:8080/auth/login `
  -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
$token = ($response.Content | ConvertFrom-Json).token
Write-Host "Token: $token"
```

#### Utiliser le token
```powershell
$headers = @{ Authorization = "Bearer $token" }

# GET /api/status
Invoke-WebRequest -Uri http://localhost:8080/api/status `
  -Headers $headers -UseBasicParsing | 
  Select-Object StatusCode, @{N='Content';E={$_.Content | ConvertFrom-Json | ConvertTo-Json}}

# POST /api/deploy
Invoke-WebRequest -Uri http://localhost:8080/api/deploy `
  -Method POST -Headers $headers -UseBasicParsing |
  Select-Object StatusCode, @{N='Content';E={$_.Content | ConvertFrom-Json | ConvertTo-Json}}
```

## Pourquoi cette approche ?

1. **Swagger Editor** : Interface complète, pas de setup requis
2. **Séparation** : La spécification OpenAPI (`openapi.yaml`) reste indépendante du code
3. **Maintenance** : Plus facile à maintenir qu'un système intégré
4. **Performance** : Pas de surcharge dans l'application
5. **Universalité** : Le fichier `openapi.yaml` peut être utilisé avec n'importe quel outil

## Fichiers disponibles

- `openapi.yaml` : Spécification complète de l'API (OpenAPI 3.0.3)
- `postman/ops-portal.postman_collection.json` : Collection Postman
- `postman/ops-portal.postman_environment.json` : Environnement Postman
- `docs/SWAGGER.md` : Documentation complète

## Recommandation

Pour tester rapidement l'API avec une interface Swagger :

1. **Option 1** : [Swagger Editor en ligne](https://editor.swagger.io/) + copier `openapi.yaml`
2. **Option 2** : Collection Postman (tests automatiques + gestion tokens)
3. **Option 3** : Swagger UI Docker (si vous voulez une UI locale dédiée)
