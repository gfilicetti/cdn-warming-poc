#!/usr/bin/env python

import uuid
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from random import choice
from confluent_kafka import Producer
from google.cloud import logging, pubsub_v1

def main(args):

    # Create an ID for myself for logging purpose
    my_id = uuid.uuid1()

    # Create Cloud Logging client
    logging_client = logging.Client()
    logging_client.setup_logging()
    logger = logging_client.logger("cdn-warming-producer-pubsub")

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    # def delivery_callback(err, msg):
    #     if err:
    #         print('ERROR: Message failed delivery: {}'.format(err))
    #     else:
    #         log_text = "{id} - Produced event to topic {topic}: key = {key} value = {value}".format(
    #             id=my_id, topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8'))
    #         print(log_text)
    #         logger.log_text(log_text)

    # Produce data by selecting random values from these lists.
    topic = "warming_urls"
    ids = ['0001', '0002', '0003', '0014', '0050', '0024']
    urls = ['http://postman-echo.com/get?file=houseofdrag001.ts', 
            'http://postman-echo.com/get?file=stateoftheunion.mp4', 
            'http://postman-echo.com/get?file=mlb-bluejays-v-redsox.mpeg', 
            'http://postman-echo.com/get?file=jeffcorwinexp0001.mp4', 
            'http://postman-echo.com/get?file=tonysoprano-hottake.ts']

    # Initialize a Publisher client.
    client = pubsub_v1.PublisherClient()
    # Create a fully qualified identifier of form `projects/{project_id}/topics/{topic_id}`
    topic_path = client.topic_path("cdn-warming-poc", topic)

    index = 0
    for _ in range(args.count):
        id = choice(ids)
        url = choice(urls)

        # Data sent to Cloud Pub/Sub must be a bytestring.
        data = url.encode("utf-8")

        # When you publish a message, the client returns a future.
        api_future = client.publish(topic_path, data)
        message_id = api_future.result()

        log_text = "{id} - Published event to topic {topic}: value = {value}, message = {message}".format(
            id=my_id, topic=topic_path, value=data, message=message_id)
        print(log_text)
        logger.log_text(log_text)

        index += 1

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('count', type=int, default=10)

    main(parser.parse_args())