def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

from confluent_kafka import Producer
producer = Producer(read_ccloud_config("client.properties"))
producer.produce("my-topic", key="key", value="value")


#!/usr/bin/env python

import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from random import choice
from confluent_kafka import Producer

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('count', default=10)
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

    # Produce data by selecting random values from these lists.
    topic = "wbd-cdn-warming"
    ids = ['0001', '0002', '0003', '0014', '0050', '0024']
    urls = ['http://postman-echo.com/get?file=1', 'http://postman-echo.com/get?file=2', 'http://postman-echo.com/get?file=3', 'http://postman-echo.com/get?file=4', 'http://postman-echo.com/get?file=5']

    index = 0
    for _ in range(args.count):

        id = choice(ids)
        url = choice(urls)
        producer.produce(topic, key=id, value=url, callback=delivery_callback)
        index += 1

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()

