from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

http_requests = Counter("ops_http_requests_total", "Count HTTP requests", ["endpoint"])

def init_metrics(app):
    @app.before_request
    def _count():
        pass  # on pourrait labelliser par endpoint avec une before/after_request

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
