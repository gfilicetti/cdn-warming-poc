#!/bin/bash
# This script will deploy a new cloud run in the region passed in 
# pubsub-cloud-run.sh {region} {image} {cloudrun_service_name}
REGION=${1:-"us-central1"}
IMAGE=${2:-"us-central1-docker.pkg.dev/cdn-warming-poc/registry-docker/cdn-prewarm-container"}
SERVICE=${3:-"cdn-prewarm-us-central1"}
PROJECT=${4:-$(gcloud config get project)}

printf "Using region: ${REGION} \n"
printf "Using image: ${IMAGE} \n"
printf "Using cloud run service: ${SERVICE} \n"
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
