#!/bin/bash
# This script will set up the pub/sub topic and create the service account and bindings
# pubsub-setup.sh {topic_name} {project_name}

TOPIC=${1:-"warming_urls"}
PROJECT=${2:-$(gcloud config get project)}

printf "Using topic: ${TOPIC}"
printf "Using project: ${PROJECT}"

# create the topic we'll be using
gcloud pubsub topics create $TOPIC

# create an SA specifically for calling CR upon new P/S messages
gcloud iam service-accounts create cloud-run-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"

# give the new SA cloud run invoker privs
gcloud run services add-iam-policy-binding cdn-prewarm-pubsub \
    --member=serviceAccount:cloud-run-pubsub-invoker@$PROJECT.iam.gserviceaccount.com \
    --role=roles/run.invoker \
    --region=us-central1

# give pub sub the account token creator privs
gcloud projects add-iam-policy-binding $PROJECT \
   --member=serviceAccount:service-1034328539074@gcp-sa-pubsub.iam.gserviceaccount.com \
   --role=roles/iam.serviceAccountTokenCreator