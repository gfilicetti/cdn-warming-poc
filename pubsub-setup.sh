#!/bin/bash

# create the topic we'll be using
gcloud pubsub topics create warming_urls

# create an SA specifically for calling CR upon new P/S messages
gcloud iam service-accounts create cloud-run-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"

# give the new SA cloud run invoker privs
gcloud run services add-iam-policy-binding cdn-warming-poc \
    --member=serviceAccount:cloud-run-pubsub-invoker@cdn-warming-poc.iam.gserviceaccount.com \
    --role=roles/run.invoker

# give pub sub the account token creator privs
gcloud projects add-iam-policy-binding cdn-warming-poc \
   --member=serviceAccount:service-1034328539074@gcp-sa-pubsub.iam.gserviceaccount.com \
   --role=roles/iam.serviceAccountTokenCreator

gcloud pubsub subscriptions create us-west4 --topic warming_urls \
    --ack-deadline=600 \
    --push-endpoint=https://cdn-prewarm-pubsub-7amek6gxsq-uc.a.run.app/ \
    --push-auth-service-account=cloud-run-pubsub-invoker@cdn-warming-poc.iam.gserviceaccount.com


