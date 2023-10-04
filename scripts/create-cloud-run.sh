#!/bin/bash
# This script will deploy a new cloud run in the region passed in 
# pubsub-cloud-run.sh {region} {image} {cloudrun_service_name}
REGION=${1:-"us-central1"}
IMAGE=${2:-"us-central1-docker.pkg.dev/cdn-warming-poc/registry-docker/cdn-prewarm-container"}
SERVICE=${3:-"cdn-prewarm"}

gcloud run deploy $SERVICE \
    --image=$IMAGE:latest \
    --min-instances=1 \
    --no-cpu-throttling \
    --allow-unauthenticated \
    --cpu-boost \
    --region=$REGION