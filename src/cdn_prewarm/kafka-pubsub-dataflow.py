import datetime
import warnings

import apache_beam as beam

from apache_beam.io import WriteToPubSub
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.options.pipeline_options import PipelineOptions

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

    # Murat's config
    # kafka_config = {
    #     "bootstrap.servers": "10.164.0.24:9092"
    # }

    kafka_config = {
        "bootstrap.servers": "pkc-n3603.us-central1.gcp.confluent.cloud:9092",
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "PLAIN",
        # "group.id": "cdn_prewarm_group",
        # "auto.offset.reset": "earliest",
        "sasl.jaas.config":f'org.apache.kafka.common.security.plain.PlainLoginModule required serviceName="Kafka" username="RXKZZPZHVYNU2XAJ" password="NhQ6zSqNh5C5a2Yup8Xfaa8E7MueU303MU4n8guxrk0W4D8EPyfxmcarrSUhu6KK";'
    }

    records = (p 
        | "Read from source" >> ReadFromKafka(consumer_config=kafka_config, topics=["warming_2"])
        | "Extract the value" >> beam.Map(lambda x: x[1])
        | "Write to destination" >> WriteToPubSub(topic="projects/cdn-warming-poc/topics/warming_urls")
    )