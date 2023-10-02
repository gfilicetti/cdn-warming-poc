#!/usr/bin/env python

import sys
import uuid
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from random import choice
from confluent_kafka import Producer
from google.cloud import logging

def main(args):
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    # Create an ID for myself for logging purpose
    my_id = uuid.uuid1()

    # Create Producer instance
    producer = Producer(config)

    # Create Cloud Logging client
    logging_client = logging.Client()
    logger = logging_client.logger("cdn-warming-producer")

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            log_text = "{id} - Produced event to topic {topic}: key = {key} value = {value}".format(
                id=my_id, topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8'))
            print(log_text)
            logger.log_text(log_text)

    # Produce data by selecting random values from these lists.
    topic = "warming_urls"
    ids = ['0001', '0002', '0003', '0014', '0050', '0024']
    urls = ['http://postman-echo.com/get?file=houseofdrag001.ts', 
            'http://postman-echo.com/get?file=stateoftheunion.mp4', 
            'http://postman-echo.com/get?file=mlb-bluejays-v-redsox.mpeg', 
            'http://postman-echo.com/get?file=jeffcorwinexp0001.mp4', 
            'http://postman-echo.com/get?file=tonysoprano-hottake.ts']

    index = 0
    for _ in range(args.count):

        id = choice(ids)
        url = choice(urls)
        producer.produce(topic, key=id, value=url, callback=delivery_callback)
        index += 1

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('count', type=int, default=10)

    main(parser.parse_args())