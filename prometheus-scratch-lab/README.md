# Scratch Prometheus Monitoring Lab
Minimal, low-resource Prometheus configuration monitoring a simple web service.

## Deployment Steps
```bash
oc new-project custom-monitoring
oc new-app stefanprodan/podinfo:6.5.4 --name=simple-web
oc expose deployment/simple-web --port=9898 --target-port=9898
oc apply -f prometheus-config.yaml
oc new-app prom/prometheus:v2.45.0 --name=prometheus-engine
oc set volumes deployment/prometheus-engine --add --name=config-storage-volume --type=configmap --configmap-name=prometheus-core-config --mount-path=/etc/prometheus --overwrite
oc create route edge prometheus-engine --service=prometheus-engine --insecure-policy=Redirect
\`\`\`
