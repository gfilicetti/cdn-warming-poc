import datetime
import warnings
from argparse import ArgumentParser, FileType
from configparser import ConfigParser

import apache_beam as beam
from apache_beam.io import WriteToPubSub
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.options.pipeline_options import PipelineOptions

def main(args):
    # get config settings
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    warnings.filterwarnings("ignore")

    project_id="cdn-warming-poc"
    bucket=f"gs://{project_id}"
    temp_location=f"{bucket}/temp"
    staging_location=f"{bucket}/staging"
    region="us-central1"
    kafka_topic="warming_urls"
    pubsub_topic="warming_urls"

    options=PipelineOptions([
        "--runner=DataflowRunner", 
        f"--job_name=kafka-mirror-python-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}",
        "--experiment=use_unsupported_python_version",
        "--dataflow_service_options=enable_prime",
        "--streaming",
        f"--project={project_id}", 
        f"--region={region}", 
        f"--temp_location={temp_location}", 
        f"--staging_location={staging_location}"])

    with beam.Pipeline(options=options) as p:

        kafka_config = {
            "bootstrap.servers": config['bootstrap.servers'],
            "security.protocol": config['security.protocol'],
            # NOTE!!!!!! The config for this job needs 'mechanism' singular but the kafka.env
            # config file needs it to be 'mechanisms' plural. THIS IS INTENTIONAL!
            "sasl.mechanism": config['sasl.mechanisms'],
            "group.id": config['group.id'],
            "auto.offset.reset": config['auto.offset.reset'],

            # This is setting is for JAAS setup only, only the user and pw are in the kafka-env file
            "sasl.jaas.config": f'org.apache.kafka.common.security.plain.PlainLoginModule required serviceName="Kafka" username={config["sasl.username"]} password={config["sasl.password"]};'
        }

        records = (p 
            | "Read from source" >> ReadFromKafka(consumer_config=kafka_config, topics=[args.kafka_topic])
            | "Extract the value" >> beam.Map(lambda x: x[1])
            | "Write to destination" >> WriteToPubSub(topic=args.pubsub_topic)
        )

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()

    # path to a file with kafka environment settings
    parser.add_argument('config_file', type=FileType('r'))

    # just a plain name, like: 'warming_urls'
    parser.add_argument('kafka_topic')

    # the full path, like: 'projects/cdn-warming-poc/topics/warming_urls'
    parser.add_argument('pubsub_topic')
    args = parser.parse_args()

    main(args)

