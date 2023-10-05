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

    print("1. Top of main")

    # Create an ID for myself for logging purpose
    my_id = uuid.uuid1()

    # Create Cloud Logging client
    logging_client = logging.Client(project='cdn-warming-poc')
    logging_client.setup_logging()
    logger = logging_client.logger("cdn-warming-consumer-pubsub")

    print("2. After constants")

    # Receive pub/sub message
    envelope = request.get_json()
    print("3. After getting envelope")

    if not envelope:
        msg = "No Pub/Sub message received"
        log_text = f"Bad Request: {msg}"
        print(log_text)
        logger.log_text(log_text)
        return (log_text, 400)

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "Invalid Pub/Sub message format"
        log_text = f"Bad Request: {msg}"
        print(log_text)
        logger.log_text(log_text)
        return (log_text, 400)

    pubsub_message = envelope["message"]
    print(f"4. After getting message from envelope: {pubsub_message}")

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        # get the url from the message
        url = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        print(f"5. After getting url: {url}")

        # make a get call to the url and capture the response
        print(f"6. Before making request")
        response = requests.get(url)
        print(f"7. After getting response: {response}")

        log_text = f"{my_id} - Status: {response.status_code}; File: {response.json()['args']['file']}"
        print(log_text)
        logger.log_text(log_text)

        print(f"8. Before returning")

        return (log_text, 204)
    else:
        msg = "No data in the Pub/Sub message"
        log_text = f"Bad Request: {msg}"
        print(log_text)
        logger.log_text(log_text)
        return (log_text, 400)
