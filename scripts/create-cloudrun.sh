#!/bin/bash
# This script will deploy a new cloud run in the region passed in 
# pubsub-cloud-run.sh {cloudrun_service_name} {region} {image} {project}
SERVICE=${1:-"cdn-prewarm-us-central1"}
REGION=${2:-"us-central1"}
IMAGE=${3:-"us-central1-docker.pkg.dev/cdn-warming-poc/registry-docker/cdn-prewarm-pubsub"}
PROJECT=${4:-$(gcloud config get project)}

printf "Using cloud run service name: ${SERVICE} \n"
printf "Using region: ${REGION} \n"
printf "Using image: ${IMAGE} \n"
printf "Using project: ${PROJECT} \n"

# create the new cloud run service
gcloud run deploy $SERVICE \
    --image=$IMAGE:latest \
    --min-instances=1 \
    --no-cpu-throttling \
    --allow-unauthenticated \
    --cpu-boost \
    --region=$REGION

# give the pub/sub invoker SA invoker privs on this new cloud run service
gcloud run services add-iam-policy-binding $SERVICE \
    --member=serviceAccount:cloudrun-pubsub-invoker@$PROJECT.iam.gserviceaccount.com \
    --role=roles/run.invoker \
    --region=$REGION
