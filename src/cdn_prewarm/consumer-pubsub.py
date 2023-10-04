#!/usr/bin/env python

import os
import requests
import uuid
import base64
from google.cloud import logging
from flask import Flask, request
from threading import Thread

# this code is modified from this quickstart:
# https://cloud.google.com/run/docs/tutorials/pubsub

app = Flask(__name__)

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
    if not envelope:
        msg = "No Pub/Sub message received"
        print(f"Error: {msg}")
        return (f"Bad Request: {msg}", 400)

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "Invalid Pub/Sub message format"
        print(f"Error: {msg}")
        return (f"Bad Request: {msg}", 400)

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        # get the url from the message
        url = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

        # make a get call to the url and capture the response
        response = requests.get(url)

        log_text = f"{my_id} - Status: {response.status_code}; File: {response.json()['args']['file']}"
        print(log_text)
        logger.log_text(log_text)
        return ("", 204)
    else:
        msg = "No data in the Pub/Sub message"
        print(f"Error: {msg}")
        return (f"Bad Request: {msg}", 400)
