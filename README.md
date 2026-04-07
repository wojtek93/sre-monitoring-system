# Log Monitoring & Incident Detection System

This project demonstrates a production-oriented DevOps / SRE system with monitoring, alerting and incident response workflow. It includes a FastAPI application, Docker containerization, Kubernetes deployment, Prometheus monitoring, Grafana dashboards, and alerting based on HTTP 500 errors.

The goal is to demonstrate a full monitoring workflow: deploy → generate errors → observe metrics → trigger alert → visualize in Grafana.

---
## Architecture

The system consists of:

- FastAPI application exposing HTTP endpoints (/health, /error, /metrics)
- Kubernetes Deployment managing application replicas
- Prometheus scraping metrics from the application
- Alert rules detecting HTTP 500 error spikes
- Grafana dashboards visualizing system metrics and errors

Data flow:
Application → Prometheus → Alerting → Grafana

---
## Project structure


k8s/                   # Kubernetes manifests (deployments, services, configs)
app/                   # FastAPI application
monitoring/grafana/    # Grafana dashboards (not applied via kubectl)
docs/                  # runbook and documentation

---

## Requirements

- Docker Desktop (with Kubernetes enabled)
- kubectl
- Git

Check setup:

docker ps  
kubectl get nodes  

---

## Clone project

git clone https://github.com/wojtek93/sre-monitoring-system.git  
cd sre-monitoring-system  

---

## Build Docker image

docker build -t sre-demo:local .  

---

## Deploy to Kubernetes

kubectl apply -f k8s/  

Check status:

kubectl get pods -n sre-demo  
kubectl get svc -n sre-demo  

Wait until all pods are in **Running** state

---

## Access application

kubectl port-forward -n sre-demo svc/sre-demo-service 8000:80  

Test:

curl http://localhost:8000/health  

---

## Access Prometheus

kubectl port-forward -n sre-demo svc/prometheus 9090:9090  

---

## Prometheus integration

Prometheus scrapes metrics directly from the FastAPI application using the `/metrics` endpoint.

The application exposes metrics on port `8000`, and Prometheus is configured to collect them from the application service.

Example scrape flow:

FastAPI app -> /metrics endpoint -> Prometheus scrape -> alert evaluation -> Grafana dashboard

To verify that Prometheus is connected correctly:

1. Open Prometheus:
   http://localhost:9090

2. Go to:
   Status -> Targets

3. Check that the application target is in `UP` state

4. Query example:
   http_requests_total

If the target is `UP`, Prometheus is successfully scraping application metrics.

## Access Grafana

kubectl port-forward -n sre-demo svc/grafana 3000:3000  

Open:

http://localhost:3000  

Login:

admin / admin  

--- 
## Prometheus scrape configuration

Prometheus is configured to scrape the application metrics endpoint.

Example target:

- application service on port `8000`
- metrics path: `/metrics`

The scrape configuration is defined in:

`k8s/prometheus.yaml`
or
`monitoring/prometheus/prometheus.yml`

---
## Configure Grafana data source

1. Open Grafana:
   http://localhost:3000

2. Login:
   admin / admin

3. Go to:
   Connections → Data Sources

4. Click:
   Add data source

5. Select:
   Prometheus

6. In URL field enter:
   http://prometheus:9090

7. Click:
   Save & Test

If the connection is successful, Grafana is now connected to Prometheus.

---

## Load dashboard

1. Go to **Dashboards**
2. Click **Import**
3. Upload file:

monitoring/grafana/grafana-dashboard.json  

4. Select Prometheus as data source  
5. Click Import  

---

## Simulate incident

Run in new terminal:

seq 20 | xargs -I{} curl -s http://localhost:8000/error?rate=100 > /dev/null  

---

## Verify metrics

curl -s http://localhost:8000/metrics | grep http_requests_total  

---

## Check alert

In Prometheus:

1. Go to **Alerts**
2. Find: HighErrorRate
3. Status should be: FIRING  

---

## Observe dashboard

In Grafana dashboard you should see:

- request count increasing  
- HTTP 500 errors spike  
- metrics updating in real time  

---

## Troubleshooting

If pods are not running:

kubectl get pods -n sre-demo
kubectl describe pod <pod-name> -n sre-demo
kubectl logs -n sre-demo <pod-name>

If service is not accessible:

kubectl get svc -n sre-demo
kubectl port-forward -n sre-demo svc/sre-demo-service 8000:80

---

## Runbook

See:

docs/runbook.md  

---

## Tech stack

FastAPI, Docker, Kubernetes, Prometheus, Grafana, GitHub Actions  

---

## What this demonstrates

- containerized application deployment  
- Kubernetes-based system  
- metrics collection and monitoring  
- alerting based on error rate  
- dashboard-based observability  
- basic incident response workflow  

---

## CI/CD

The project includes a GitHub Actions pipeline that:

- builds Docker image on push
- validates application build process
- prepares image for deployment

This simulates a basic CI workflow used in production environments.

---