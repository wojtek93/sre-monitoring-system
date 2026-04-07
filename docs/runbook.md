# Runbook: HighErrorRate

When the HighErrorRate alert is firing it means the application is returning too many HTTP 500 errors.

Detection:
Prometheus alert based on:
http_requests_total{path="/error",status="500"} > 10

Investigation:
kubectl get pods -n sre-demo
kubectl logs -n sre-demo deployment/sre-demo
curl -s http://localhost:8000/metrics | grep http_requests_total
http://localhost:9090/targets

Recovery:
kubectl rollout restart deployment/sre-demo -n sre-demo

Verification:
curl http://localhost:8000/health
curl -s http://localhost:8000/metrics | grep http_requests_total
Check Prometheus Alerts page