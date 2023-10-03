#!/bin/bash
gcloud run deploy cdn-prewarm \
--image=us-central1-docker.pkg.dev/cdn-warming-poc/registry-docker/cdn-prewarm-container:latest \
--min-instances=1 \
--no-cpu-throttling \
--allow-unauthenticated \
--cpu-boost \
--region=us-central1