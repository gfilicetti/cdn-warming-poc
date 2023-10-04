#!/bin/bash
# This script will set up the pub/sub topic and create the service account and bindings
# pubsub-setup.sh {topic_name} {project_name} {cloudrun_service_name} {policy_region}

TOPIC=${1:-"warming_urls"}
PROJECT=${2:-$(gcloud config get project)}
PROJECT_NUM=$(gcloud projects describe $PROJECT --format="value(projectNumber)")

printf "Using topic: ${TOPIC} \n"
printf "Using project: ${PROJECT} \n"
printf "Using project number: ${PROJECT_NUM} \n"

# first create the topic
gcloud pubsub topics create $TOPIC

# create an SA specifically for calling CR upon new P/S messages
gcloud iam service-accounts create cloudrun-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"

# give pub sub the account token creator privs
gcloud projects add-iam-policy-binding $PROJECT \
   --member=serviceAccount:service-$PROJECT_NUM@gcp-sa-pubsub.iam.gserviceaccount.com \
   --condition=None \
   --role=roles/iam.serviceAccountTokenCreator

   