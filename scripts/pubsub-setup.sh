#!/bin/bash
# This script will set up the pub/sub topic and create the service account and bindings
# pubsub-setup.sh {topic_name} {project_name} {cloudrun_service_name} {policy_region}

TOPIC=${1:-"warming_urls"}
PROJECT=${2:-$(gcloud config get project)}
CLOUDRUN=${3:-"cdn-prewarm-us-central1"}
REGION=${4:-"us-central1"}
PROJECT_NUM=$(gcloud projects describe $PROJECT --format="value(projectNumber)")

printf "Using topic: ${TOPIC} \n"
printf "Using project: ${PROJECT} \n"
printf "Using cloud run service: ${CLOUDRUN} \n"
printf "Using policy region: ${REGION} \n"
printf "Using project number: ${PROJECT_NUM} \n"

# first create the topic
gcloud pubsub topics create $TOPIC

# create an SA specifically for calling CR upon new P/S messages
gcloud iam service-accounts create cloudrun-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"

# give the new SA cloud run invoker privs
gcloud run services add-iam-policy-binding $CLOUDRUN \
    --member=serviceAccount:cloudrun-pubsub-invoker@$PROJECT.iam.gserviceaccount.com \
    --role=roles/run.invoker \
    --region=$REGION

# give pub sub the account token creator privs
gcloud projects add-iam-policy-binding $PROJECT \
   --member=serviceAccount:service-$PROJECT_NUM@gcp-sa-pubsub.iam.gserviceaccount.com \
   --role=roles/iam.serviceAccountTokenCreator

   