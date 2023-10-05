# This script will block and loop listening for messages on the Kafka topic and then will call the URL
# -- NOTE: This is meant to be run locally for testing
# python -m cdn_prewarm.consumer-kafka { config_file } { kafka_topic } { project_id }
# eg: python -m cdn_prewarm.consumer-kafka kafka-env cdn_warming cdn-warming-poc-project

import requests
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING

def main(args):
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    consumer.subscribe([args.topic], on_assign=reset_offset)

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
                # extract the id and url from the message
                id = msg.key().decode('utf-8')
                url = msg.value().decode('utf-8')

                # make a get call to the url and capture the response
                response = requests.get(url)

                log_text = f"URL called - Status: {response.status_code}; Response: {response.json()['args']['file']}"
                print(log_text)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('topic')
    parser.add_argument('project_id')
    parser.add_argument('--reset', action='store_true')

    main(parser.parse_args())

