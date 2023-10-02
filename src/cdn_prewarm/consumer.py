#!/usr/bin/env python

import os
import sys
import requests
import uuid
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
from google.cloud import logging
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/ztatuz")
def status():
    print("I'm in ztatuz!!")
    return "OK"

def main(config, reset):
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    # config_parser = ConfigParser()
    # config_parser.read_file(args.config_file)
    # config = dict(config_parser['default'])
    # config.update(config_parser['consumer'])

    # Create an ID for myself for logging purpose
    my_id = uuid.uuid1()

    # Create Consumer instance
    consumer = Consumer(config)

    # Create Cloud Logging client
    logging_client = logging.Client()
    logger = logging_client.logger("cdn-warming-consumer")

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    topic = "warming_urls"
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # exact the id and url from the message
                id = msg.key().decode('utf-8')
                url = msg.value().decode('utf-8')

                # make a get call to the url and capture the response
                response = requests.get(url)

                log_text = f"{my_id} - Status: {response.status_code}; File: {response.json()['args']['file']}"
                print(log_text)
                logger.log_text(log_text)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()

if __name__ == '__main__':
    # Parse the command line.
    print("About to parse args")
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')

    # main(parser.parse_args())
    args = parser.parse_args()

    # get config settings
    print("Now parsing config")
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    print("firing off the thread")
    thread = Thread(target=main, args=(config, args.reset))
    thread.start()

    print("running the gunicorn")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))