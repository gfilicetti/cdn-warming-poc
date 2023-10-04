#!/bin/bash
# This script will set up the pub/sub topic and create the service account and bindings
# pubsub-setup.sh {topic_name} {project_name} {policy_region}

TOPIC=${1:-"warming_urls"}
PROJECT=${2:-$(gcloud config get project)}
REGION=${3:-"us-central1"}
PROJECT_NUM=$(gcloud projects describe $PROJECT --format="value(projectNumber)")

printf "Using topic: ${TOPIC}"
printf "Using project: ${PROJECT}"
printf "Using policy region: ${REGION}"
printf "Using project number: ${PROJECT_NUM}"

# first create the topic
gcloud pubsub topics create $TOPIC

# create an SA specifically for calling CR upon new P/S messages
gcloud iam service-accounts create cloudrun-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"

# give the new SA cloud run invoker privs
gcloud run services add-iam-policy-binding cloudrun-invoking-perms \
    --member=serviceAccount:cloudrun-pubsub-invoker@$PROJECT.iam.gserviceaccount.com \
    --role=roles/run.invoker \
    --region=$REGION

# give pub sub the account token creator privs
gcloud projects add-iam-policy-binding $PROJECT \
   --member=serviceAccount:service-$PROJECT_NUM@gcp-sa-pubsub.iam.gserviceaccount.com \
   --role=roles/iam.serviceAccountTokenCreator

   