from flask import Flask
from .metrics import init_metrics
from .auth import auth_bp
from .api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="change-me",
        JWT_ISSUER="ops-portal",
        JWT_AUDIENCE="ops",
        JWT_EXP_SECONDS=3600,
    )

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp,  url_prefix="/api")

    @app.get("/")
    def index():
        return {
            "service": "ops-portal",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/auth/login",
                "api": "/api/status",
                "health": "/healthz",
                "metrics": "/metrics",
                "docs": "See openapi.yaml or Swagger Editor"
            }
        }, 200

    @app.get("/healthz")
    def health():
        return {"status": "ok"}, 200

    @app.get("/readyz")
    def ready():
        return {"ready": True}, 200

    init_metrics(app)  # /metrics
    return app
