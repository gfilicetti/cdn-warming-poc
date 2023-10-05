# This script will create messages with 1 of 5 random URLs and push them to Kafka
# python -m cdn_prewarm.producer { config_file } { kafka_topic } { count }
# eg: python -m cdn_prewarm.producer kafka-env cdn_warming 1000

from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from random import choice
from confluent_kafka import Producer

def main(args):
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
            log_text = "Message to topic {topic}: key = {key} value = {value}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8'))
            print(log_text)

    # Produce data by selecting random values from these lists.
    ids = ['0001', '0002', '0003', '0014', '0050', '0024']
    urls = ['http://postman-echo.com/get?file=houseofdragonsS01E01-001.ts', 
            'http://postman-echo.com/get?file=stateoftheunion20231004.mp4', 
            'http://postman-echo.com/get?file=mlb-bluejays-v-redsox-GAME1011.mpeg', 
            'http://postman-echo.com/get?file=jeffcorwinexpS12E01-050.mp4', 
            'http://postman-echo.com/get?file=tonysoprano-intro-012.ts']

    index = 0
    for _ in range(args.count):
        id = choice(ids)
        url = choice(urls)
        producer.produce(args.topic, key=id, value=url, callback=delivery_callback)
        index += 1

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('topic')
    parser.add_argument('count', type=int, default=10)

    main(parser.parse_args())