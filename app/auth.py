import time
import jwt
from flask import Blueprint, request, jsonify, current_app
from functools import wraps

auth_bp = Blueprint("auth", __name__)

USERS = {
    "alice": {"password": "alice123", "roles": ["ops"]},
    "admin": {"password": "admin123", "roles": ["admin", "ops"]},
}


def generate_token(sub, roles):
    now = int(time.time())
    payload = {
        "iss": current_app.config["JWT_ISSUER"],
        "aud": current_app.config["JWT_AUDIENCE"],
        "iat": now,
        "exp": now + current_app.config["JWT_EXP_SECONDS"],
        "sub": sub,
        "roles": roles,
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


@auth_bp.post("/login")
def login():
    """
    Connexion utilisateur
    ---
    tags:
      - Authentication
    summary: Authentifie un utilisateur et retourne un token JWT
    description: |
      Utilisateurs disponibles pour les tests :
      - alice / alice123 (rôle: ops)
      - admin / admin123 (rôles: admin, ops)
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: alice
              description: Nom d'utilisateur
            password:
              type: string
              format: password
              example: alice123
              description: Mot de passe
    responses:
      200:
        description: Authentification réussie
        schema:
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
              description: Token JWT valide pour 1 heure
      401:
        description: Credentials invalides
        schema:
          type: object
          properties:
            error:
              type: string
              example: invalid credentials
    """
    data = request.get_json() or {}
    user = USERS.get(data.get("username"))
    if not user or user["password"] != data.get("password"):
        return jsonify({"error": "invalid credentials"}), 401
    token = generate_token(data["username"], user["roles"])
    return jsonify({"token": token})


def requires_roles(*required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return {"error": "missing token"}, 401
            token = auth.split(" ", 1)[1]
            try:
                payload = jwt.decode(
                    token,
                    current_app.config["SECRET_KEY"],
                    algorithms=["HS256"],
                    audience=current_app.config["JWT_AUDIENCE"],
                    issuer=current_app.config["JWT_ISSUER"],
                )
            except Exception as e:
                return {"error": str(e)}, 401
            roles = payload.get("roles", [])
            if required and not any(r in roles for r in required):
                return {"error": "forbidden"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
