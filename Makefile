IMAGE=ghcr.io/your-org/ops-portal
TAG?=dev

.PHONY: run build push k3d-apply test

run:
	python -c "from app import create_app; app=create_app(); app.run(port=8080,host='0.0.0.0')"

build:
	docker build -t $(IMAGE):$(TAG) .

push:
	docker push $(IMAGE):$(TAG)

k3d-apply:
	kubectl apply -f k8s/namespace.yaml
	kubectl -n ops apply -f k8s/configmap.yaml
	kubectl -n ops apply -f k8s/secret.yaml
	sed "s/{{TAG}}/$(TAG)/" k8s/deployment.yaml | kubectl -n ops apply -f -
	kubectl -n ops apply -f k8s/service.yaml k8s/ingress.yaml

test:
	pytest -q
