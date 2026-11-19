This cricket-app is basic idea about giving live score. This is will be available in your local browser, to appear on internet , we need to configure cloudflared but that is planned in another project. 

$echo "Public Scoreboard:  https://$HOST/"  #>> this is actual score board where you update your score card. 
$echo "Scorer Admin Panel: https://$HOST/admin.html"  #>> this link is for admin where admin will update the score card. 


Step 1:
# 1. Create a new OpenShift project
oc new-project cricket-live
# 2. Create a Secret for database and admin scorer credentials
oc create secret generic cricket-secrets   --from-literal=POSTGRESQL_USER=cricket   --from
literal=POSTGRESQL_PASSWORD=cricketpass   --from-literal=POSTGRESQL_DATABASE=cricketdb   --from
literal=ADMIN_PASSWORD=admin123
# 3. Deploy PostgreSQL with 1Gi persistent storage
oc new-app postgresql-persistent   --name=cricket-db   -p DATABASE_SERVICE_NAME=cricket-db   -p 
POSTGRESQL_USER=cricket   -p POSTGRESQL_PASSWORD=cricketpass   -p POSTGRESQL_DATABASE=cricketdb   -p 
VOLUME_CAPACITY=1Gi
# 4. Verify database pod is Running
oc get pods
oc get pv

Step 2:
mkdir -p ~/cricket-app/public
cd ~/cricket-app
# Create package.json, server.js, public/index.html, and public/admin.html

Step 3: Binary S2I Build, Deployment & HTTPS Route
Upload your local source directory directly to OpenShift's internal builder, inject the credentials Secret,
and create an Edge HTTPS Route
cd ~/cricket-app
# 1. Create a Binary Source-to-Image (S2I) BuildConfig
oc new-build nodejs --binary=true --name=cricket-app
# 2. Upload local code and build the container image
oc start-build cricket-app --from-dir=. --follow
# 3. Deploy the built application
oc new-app cricket-app
# 4. Inject database and admin password environment variables from Secret
oc set env deployment/cricket-app --from=secret/cricket-secrets
# 5. Expose securely over HTTPS with automatic HTTP-to-HTTPS redirect
oc create route edge cricket-app --service=cricket-app --insecure-policy=Redirec

Step 4: Verify & Access Your Application
OST=$(oc get route cricket-app -o jsonpath='{.spec.host}')
echo "Public Scoreboard:  https://$HOST/"
echo "Scorer Admin Panel: https://$HOST/admin.html"
# Quick API health check
curl -k "https://$HOST/api/state"
