# Scratch Prometheus Monitoring Lab
Minimal, low-resource Prometheus configuration monitoring a simple web service.

• prometheus-k8s-0 / 1 run under openshift-monitoring. They only scrape cluster infrastructure (nodes, API servers, cluster operators). They do not scrape your custom developer applications.
• prometheus-user-workload-0 / 1 run under openshift-user-workload-monitoring. They are the ones that reach into your custom developer Namespaces to pull your application metrics.

• /metrics inside your app pod is NOT a storage folder. It is simply a live web URL endpoint (like a webpage). Your Node.js/Python code dynamically generates text numbers on this webpage in real-time. It holds no historical data and consumes almost zero space.
• The actual storage happens inside the Prometheus pods themselves. When Prometheus pulls data from your app's /metrics page, it saves those numbers into its own high-performance Timeseries Database (TSDB) stored on its own disk volume inside the monitoring namespace.

• What prometheus-k8s collects: Timeseries numbers like container_memory_working_set_bytes = 104857600 or node_cpu_usage_percentage = 45. It does this by "scraping" (polling) a numerical data stream endpoint over HTTP every few seconds.
• What it completely ignores: Actual application logs (text strings like [ERROR] User login failed for chethan or DB connection timeout). Those text logs are completely handled by a separate logging stack (Vector/Fluentd, OpenShift Logging Operator, and Loki/Elasticsearch).


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


1. YOUR POD            2. THE NETWORK           3. PROMETHEUS POD
┌────────────────┐      ┌───────────────────┐    ┌─────────────────────────────────┐
│ Namespace:     │      │ OpenShift SDN     │    │ Namespace:                      │
│ rocky          │      │                   │    │ openshift-user-workload-monitor │
│                │      │                   │    │                                 │
│ ┌────────────┐ │      │    HTTP GET       │    │ ┌─────────────────────────────┐ │
│ │ App Container│◄─────┼───────────────────┼────┤ │ prometheus-user-workload-0  │ │
│ │            │ │      │   /metrics URL    │    │ │                             │ │
│ │ Generates  │ │      │                   │    │ │ Scrapes data and STORES it  │ │
│ │ live text  ├─┼──────┼───────────────────┼───►│ │ on its own local disk volume│ │
│ │ data on URL│ │      │  api_requests 12  │    │ └─────────────────────────────┘ │
│ └────────────┘ │      │                   │    └─────────────────────────────────┘
└────────────────┘      └───────────────────┘

1. Generation: Your application pod keeps track of active connections in its temporary RAM memory. If 12 fans hit your rockyband tour API, the app simply updates a variable in its memory.
2. The Scrape: Every 15 seconds, the central prometheus-user-workload-0 pod sends an internal HTTP network request to your app: GET http://<your-pod-ip>:8080/metrics.
3. The Extraction: Your app reads its internal memory variables and prints a plain text string onto the webpage right at that exact microsecond: rocky_api_requests_total 12.
4. The Storage: Prometheus reads that text line string, attaches a timestamp to it (e.g., Nov 25, 2026, 22:50:00 -> 12), and saves it onto its own hard disk database volume inside the monitoring namespace.
5. The Memory Wipe: If your application pod crashes, gets deleted, or restarts, its local count drops back to 0. However, your historical data graph remains completely safe and unbroken because Prometheus already sucked the data out and stored it permanently in its own database!



Side-by-Side Comparison


Feature	                          OpenShift-Monitoring (Cluster-Wide)	                                                Project-Specific Monitoring (Our Scratch Lab)
Who Manages It?	                 Cluster Administrators (kubeadmin) via Operators.	                                  Application Developers (You!) via regular YAML.
Where Does It Run?	             Locked namespaces (openshift-monitoring).	                                          Right inside your own namespace (custom-monitoring).
What Does It Track?	              Node CPU/RAM, cluster health, internal OpenShift system controllers.	              Just your explicit app endpoints (simple-web:9898).
Resource Impact	                  Massive (4 GB - 6 GB+ RAM). Runs complex multi-replica 	                            Tiny (< 150 MB RAM). Runs one single, lightweight container.
                                                      engines and data storage scrapers.
Isolation	Shared.               If a developer breaks a rule, it can flood the central                                If your app floods metrics, only your private Prometheus pod crashes.
                                system tracking registers.	100% Isolated.
