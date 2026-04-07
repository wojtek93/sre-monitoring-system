# Log Monitoring & Incident Detection System

This project simulates a production-like DevOps / SRE system. It consists of a simple FastAPI application that exposes endpoints, generates controlled HTTP 500 errors, and provides Prometheus metrics. The application is containerized with Docker, deployed to Kubernetes, and monitored using Prometheus with alerting based on error spikes.

The system allows you to simulate incidents, observe metrics, trigger alerts, and follow a basic operational workflow similar to real-world environments.

The application exposes three main endpoints:
- /health – health check endpoint
- /error – generates HTTP 500 responses based on probability
- /metrics – exposes Prometheus metrics

The application is deployed to Kubernetes using Deployment and Service resources. Prometheus is configured via ConfigMap and scrapes the application metrics. An alert is defined to detect high error rates.

To build and deploy the application:

docker build -t sre-demo:local .
kubectl apply -f k8s/
kubectl get pods -n sre-demo
kubectl get svc -n sre-demo

To access the application locally:

kubectl port-forward -n sre-demo svc/sre-demo-service 8000:80

Then test:

curl http://localhost:8000/health

To access Prometheus:

kubectl port-forward -n sre-demo svc/prometheus 9090:9090

Open in browser:
http://localhost:9090

To simulate an incident (generate HTTP 500 errors):

seq 20 | xargs -I{} curl -s http://localhost:8000/error?rate=100 > /dev/null

To verify metrics:

curl -s http://localhost:8000/metrics | grep http_requests_total

Prometheus alert is triggered when the number of HTTP 500 responses exceeds a threshold:

http_requests_total{path="/error",status="500"} > 10

To check alert status:
- open Prometheus
- go to Alerts tab
- find HighErrorRate
- status should become FIRING

Runbook for incident handling is available in:
docs/runbook.md

Technology used:
Python (FastAPI), Docker, Kubernetes, Prometheus

This project demonstrates practical skills in monitoring, alerting, incident simulation, Kubernetes deployment, and troubleshooting in a production-like environment.