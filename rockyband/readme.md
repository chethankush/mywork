This is three tier application

Step 1 for your new three-tier project:
# 1. Create the 'rocky' namespace
oc new-project rocky

# 2. Create the Secret for PostgreSQL credentials
oc create secret generic rocky-db-secret \
  --from-literal=POSTGRESQL_USER=rockyuser \
  --from-literal=POSTGRESQL_PASSWORD=rockypass \
  --from-literal=POSTGRESQL_DATABASE=rockydb

# 3. Create the ConfigMap for non-sensitive settings
oc create configmap rocky-config \
  --from-literal=BAND_NAME="ROCKY BAND" \
  --from-literal=TOUR_TITLE="WORLD TOUR 2026" \
  --from-literal=BACKEND_URL="http://rocky-backend:8080"

# 4. Deploy Tier 3: PostgreSQL Database
oc new-app postgresql-persistent \
  --name=rocky-db \
  -p DATABASE_SERVICE_NAME=rocky-db \
  -p POSTGRESQL_USER=rockyuser \
  -p POSTGRESQL_PASSWORD=rockypass \
  -p POSTGRESQL_DATABASE=rockydb \
  -p VOLUME_CAPACITY=1Gi


Step 2: Create & Deploy rocky-backend (2 Replicas)
Run these commands in your terminal to create the backend code and build/deploy it inside OpenShift:

mkdir -p ~/rockyband/backend
cd ~/rockyband/backend

Build & Deploy rocky-backend on OpenShift (Notice: NO route created—internal ClusterIP only!)
oc new-build nodejs --binary=true --name=rocky-backend
oc start-build rocky-backend --from-dir=. --follow
oc new-app rocky-backend

Inject database credentials from Secret and non-sensitive config from ConfigMap
oc set env deployment/rocky-backend --from=secret/rocky-db-secret
oc set env deployment/rocky-backend --from=configmap/rocky-config

oc scale deployment/rocky-backend --replicas=2


Step 3: Create & Deploy rocky-frontend
Run these commands to create the frontend proxy/UI server and deploy it onto OpenShift:

mkdir -p ~/rockyband/frontend/public
cd ~/rockyband/frontend

oc new-build nodejs --binary=true --name=rocky-frontend
oc start-build rocky-frontend --from-dir=. --follow
oc new-app rocky-frontend

oc set env deployment/rocky-frontend --from=configmap/rocky-config

oc create route edge rockyband --service=rocky-frontend --insecure-policy=Redirect

Verify & Print Your RockyBand URL

oc get pods,svc,route
HOST=$(oc get route rockyband -o jsonpath='{.spec.host}')
echo "RockyBand URL: https://$HOST/"
