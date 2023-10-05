#!/usr/bin/env python

import requests
import uuid
import base64
import socket
from google.cloud import logging
from flask import Flask, request
from threading import Thread

# this code is modified from this quickstart:
# https://cloud.google.com/run/docs/tutorials/pubsub

app = Flask(__name__)

def getInstanceId():
    response = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/id', headers={"Metadata-Flavor": "Google"})
    return response.text

instance_id = getInstanceId()

@app.route("/", methods=["POST"])
def main():

    # Create an ID for myself for logging purpose
    my_id = uuid.uuid1()

    # Create Cloud Logging client
    logging_client = logging.Client(project='cdn-warming-poc')
    logging_client.setup_logging()
    logger = logging_client.logger("cdn-warming-consumer-pubsub")

    # Receive pub/sub message
    envelope = request.get_json()

    # check if our envelope is real
    if not envelope:
        msg = "No Pub/Sub message received"
        log_text = f"Bad Request: {msg}"
        print(log_text)
        logger.log_text(log_text)
        return (log_text, 400)

    # check if we have a message in the envelope
    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "Invalid Pub/Sub message format"
        log_text = f"Bad Request: {msg}"
        print(log_text)
        logger.log_text(log_text)
        return (log_text, 400)

    # pull the message from the envelope
    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        # get the url from the message
        url = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

        # make a get call to the url and capture the response
        response = requests.get(url)

        log_text = f"{my_id} - Status: {response.status_code}; File: {response.json()['args']['file']}; Instance: {instance_id}"
        print(log_text)
        logger.log_text(log_text)

        return (log_text, 204)
    else:
        msg = "No data in the Pub/Sub message"
        log_text = f"Bad Request: {msg}"
        print(log_text)
        logger.log_text(log_text)
        return (log_text, 400)
