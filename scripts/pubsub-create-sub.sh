#!/bin/bash
# This script will create a subscription to the passed in topic with the given name
# pubsub-create-sub.sh {new_sub_name} {topic_name} {cloudrun_endpoint_url} {project_name}

SUB=${1:-"us-central1"}
TOPIC=${2:-"warming_urls"}
ENDPOINT=${3:-"-- MUST HAVE ENDPOINT --"}
PROJECT=${4:-$(gcloud config get project)}

printf "Using sub: ${SUB} \n"
printf "Using topic: ${TOPIC} \n"
printf "Using endpoint: ${ENDPOINT} \n"
printf "Using project: ${PROJECT} \n"

# create the subscription to push to cloud run endpoint
gcloud pubsub subscriptions create $SUB --topic $TOPIC \
    --ack-deadline=600 \
    --push-endpoint=$ENDPOINT \
    --push-auth-service-account=cloud-run-pubsub-invoker@$PROJECT.iam.gserviceaccount.com

