gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:1034328539074-compute@developer.gserviceaccount.com" \
    --role="roles/logging.logWriter"
