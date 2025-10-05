from flask import Blueprint
from .auth import requires_roles
from .services.ci import get_pipelines, trigger_pipeline
from .services.artifacts import list_artifacts
from .services.monitor import get_status

api_bp = Blueprint("api", __name__)


@api_bp.get("/status")
@requires_roles("ops")
def status():
    """
    Obtenir le statut du système
    ---
    tags:
      - API
    summary: Retourne l'état des pipelines, artefacts et monitoring
    description: Nécessite le rôle 'ops' ou 'admin'
    security:
      - Bearer: []
    responses:
      200:
        description: Statut récupéré avec succès
        schema:
          type: object
          properties:
            ci:
              type: array
              description: État des pipelines CI/CD
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: build
                  last:
                    type: string
                    example: success
            artifacts:
              type: array
              description: Liste des artefacts disponibles
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: ops-portal:1.0.0
                  registry:
                    type: string
                    example: internal
            monitor:
              type: object
              description: Informations de monitoring
              properties:
                uptime:
                  type: string
                  example: 72h
                errors_last_hour:
                  type: integer
                  example: 0
                deps:
                  type: array
                  items:
                    type: string
                  example: [db, cache, queue]
      401:
        description: Token manquant ou invalide
        schema:
          type: object
          properties:
            error:
              type: string
              example: missing token
      403:
        description: Rôle insuffisant
        schema:
          type: object
          properties:
            error:
              type: string
              example: forbidden
    """
    return {
        "ci": get_pipelines(),
        "artifacts": list_artifacts(),
        "monitor": get_status(),
    }


@api_bp.post("/deploy")
@requires_roles("admin")
def deploy():
    """
    Déclencher un déploiement en production
    ---
    tags:
      - API
    summary: Lance un déploiement (nécessite le rôle admin)
    description: Seuls les utilisateurs avec le rôle 'admin' peuvent déclencher un déploiement
    security:
      - Bearer: []
    responses:
      202:
        description: Déploiement déclenché avec succès
        schema:
          type: object
          properties:
            deployment_run_id:
              type: string
              example: run-prod-001
              description: Identifiant du run de déploiement
      401:
        description: Token manquant ou invalide
        schema:
          type: object
          properties:
            error:
              type: string
              example: missing token
      403:
        description: Rôle admin requis
        schema:
          type: object
          properties:
            error:
              type: string
              example: forbidden
    """
    run_id = trigger_pipeline("prod")
    return {"deployment_run_id": run_id}, 202
