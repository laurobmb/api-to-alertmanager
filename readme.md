# API alertmanagaer
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python app.py

## Send json for test
    curl -X POST "http://127.0.0.1:8000/api" -H  "accept: application/json" -H  "Content-Type: application/json" -d @json-example/example_report.json
    
    curl -X POST "http://10.36.17.1:8000/api" -H  "accept: application/json" -H  "Content-Type: application/json" -d @json-example/example_report.json
    
    curl -X POST "http://127.0.0.1:8000/api" -H  "accept: application/json" -H  "Content-Type: application/json" -d @json-example/alert_report.json
    
    curl -X POST "http://10.36.17.1:8000/api" -H  "accept: application/json" -H  "Content-Type: application/json" -d @json-example/alert_report.json

# Test

## create alerts
    oc -n openshift-monitoring create -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck-alerts.yaml 

## create pods
    oc new-project demo
    
    oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck/backend-v1.yaml 
    
    oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck/backend-v2.yaml 
    
    oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck/backend-v3.yaml 
    
    oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck.yaml


# Docker 
    buildah build -t alertmanager:v1 . 
    podman run -it --rm --name fastapi-alertmanager -p 8000:8000 alertmanager:v1
    podman run -it alertmanager:v1 /bin/sh
    podman exec -it fastapi-alertmanager cat log/fastapi.log

    podman run -it --rm --name fastapi-alertmanager -p 8000:8000 quay.io/lagomes/apialertmanager:v1
    podman run -d --rm --name fastapi-alertmanager -p 8000:8000 quay.io/lagomes/apialertmanager:v1


## Remove project
    oc delete ns demo


https://rhthsa.github.io/openshift-demo/custom-alert.html
https://github.com/rhthsa/openshift-demo    



## View alerts
    ALERTMANAGER="$(oc get route/alertmanager-main -n openshift-monitoring -o jsonpath='{.spec.host}')"

    curl -s -k -H "Authorization: Bearer $(oc sa get-token prometheus-k8s -n openshift-monitoring)" https://${ALERTMANAGER}/api/v1/alerts | jq .

## View logs 
    oc -n openshift-monitoring logs -f -c alertmanager alertmanager-main-0 

    oc -n openshift-monitoring logs -f -c alertmanager alertmanager-main-1

## Extract secret
    oc -n openshift-monitoring extract secret/alertmanager-main --to /tmp/  --confirm

## Set secret
    oc -n openshift-monitoring set data secret/alertmanager-main --from-file /tmp/alertmanager.yaml