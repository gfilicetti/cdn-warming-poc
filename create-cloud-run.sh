#!/bin/bash
# This script will deploy a new cloud run in the region passed in 
# pubsub-cloud-run.sh {region} {image}
REGION=${1:-"us-central1"}
IMAGE=${1:-"us-central1-docker.pkg.dev/cdn-warming-poc/registry-docker/cdn-prewarm-container"}

gcloud run deploy cdn-prewarm \
    --image=$IMAGE:latest \
    --min-instances=1 \
    --no-cpu-throttling \
    --allow-unauthenticated \
    --cpu-boost \
    --region=$REGION