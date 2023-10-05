# This script will consume messages on a Pub/Sub subscription, extract the URL can call it, waiting for a 200
# -- NOTE: This is meant to be run with gunicorn, typically in a python container, typically running in Cloud Run

import requests
import base64
from google.cloud import logging
from flask import Flask, request
from threading import Thread

# this code is modified from this quickstart:
# https://cloud.google.com/run/docs/tutorials/pubsub

app = Flask(__name__)

# Here we call the internal Google metadata server to get our instance id (NOTE: this code won't run outside of Google Cloud)
def getInstanceId():
    response = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/id', headers={"Metadata-Flavor": "Google"})
    return response.text

# TODO: this is temporarily hard-coded, we need to figure out how to get parameters into a gunicorn server
project='cdn-warming-poc-project'

# This is a distinguishable id, unique to each container instance
instance_id = getInstanceId()

@app.route("/", methods=["POST"])
def main():

    # Create Cloud Logging client
    logging_client = logging.Client(project=project)
    logging_client.setup_logging()
    logger = logging_client.logger("cdn-warming-consumer-pubsub")

    # Receive pub/sub message
    envelope = request.get_json()

    # check if our envelope is real
    if not envelope:
        msg = "No Pub/Sub message received"
        log_text = f"Bad Request: {msg}"
        logger.log_text(log_text)
        print(log_text)
        return (log_text, 400)

    # check if we have a message in the envelope
    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "Invalid Pub/Sub message format"
        log_text = f"Bad Request: {msg}"
        logger.log_text(log_text)
        print(log_text)
        return (log_text, 400)

    # pull the message from the envelope
    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        # get the url from the message
        url = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

        # make a get call to the url and capture the response
        response = requests.get(url)

        log_text = f"ID: {instance_id[-8:]} - Status: {response.status_code}; File: {response.json()['args']['file']}"
        logger.log_text(log_text)
        print(log_text)

        return (log_text, 204)
    else:
        msg = "No data in the Pub/Sub message"
        log_text = f"Bad Request: {msg}"
        logger.log_text(log_text)
        print(log_text)
        return (log_text, 400)
