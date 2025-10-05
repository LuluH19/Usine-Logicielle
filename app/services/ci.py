def get_pipelines():
    return [{"name": "build", "last": "success"}, {"name": "deploy", "last": "running"}]


def trigger_pipeline(env):
    return f"run-{env}-001"
