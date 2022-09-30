# API alertmanagaer

[![Docker Repository on Quay](https://quay.io/repository/lagomes/apialertmanager/status "Docker Repository on Quay")](https://quay.io/repository/lagomes/apialertmanager)

### Execute
* python3 -m venv venv
* source venv/bin/activate
* pip install --upgrade pip
* pip install -r requirements.txt
* python app.py

### Send json for test
* curl -X POST "http://127.0.0.1:8000/api" -H  "accept: application/json" -H  "Content-Type: application/json" -d @json-example/example_report.json 

* curl -X POST "http://127.0.0.1:8000/api" -H  "accept: application/json" -H  "Content-Type: application/json" -d @json-example/alert_report.json  


## Create pod stuck

### create alerts
* oc -n openshift-monitoring create -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck-alerts.yaml 

### create pods
* oc new-project demo  
* oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck/backend-v1.yaml
* oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck/backend-v2.yaml
* oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck/backend-v3.yaml
* oc apply -n demo -f https://raw.githubusercontent.com/rhthsa/openshift-demo/main/manifests/pod-stuck.yaml

## Deploy for docker 
* buildah build -t alertmanager:v1 . 
* podman run -it --rm --name fastapi-alertmanager -p 8000:8000 alertmanager:v1
* podman run -it alertmanager:v1 /bin/sh

### deploy POD from quay image
* podman run -it --rm --name fastapi-alertmanager -p 8000:8000 quay.io/lagomes/apialertmanager:main
* podman run -d --rm --name fastapi-alertmanager -p 8000:8000 quay.io/lagomes/apialertmanager:main

### Get LOGS from POD
* podman exec -it fastapi-alertmanager cat log/fastapi.log


## Alerts from Openshift 

### View alerts
* ALERTMANAGER="$(oc get route/alertmanager-main -n openshift-monitoring -o jsonpath='{.spec.host}')"
* curl -s -k -H "Authorization: Bearer $(oc sa get-token prometheus-k8s -n openshift-monitoring)" https://${ALERTMANAGER}/api/v1/alerts | jq .

### View logs from pod of alermanager
* oc -n openshift-monitoring logs -f -c alertmanager alertmanager-main-0 
* oc -n openshift-monitoring logs -f -c alertmanager alertmanager-main-1

### Extract secret from alertmanager
* oc -n openshift-monitoring extract secret/alertmanager-main --to /tmp/  --confirm

### Set secret to alertmanager
* oc -n openshift-monitoring set data secret/alertmanager-main --from-file /tmp/alertmanager.yaml


# Reference

https://rhthsa.github.io/openshift-demo/custom-alert.html

https://github.com/rhthsa/openshift-demo    
