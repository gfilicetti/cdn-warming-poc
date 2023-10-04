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

    kafka_config = {
        "bootstrap.servers": "pkc-n3603.us-central1.gcp.confluent.cloud:9092",
        "sasl.username": "RXKZZPZHVYNU2XAJ",
        "sasl.password": "NhQ6zSqNh5C5a2Yup8Xfaa8E7MueU303MU4n8guxrk0W4D8EPyfxmcarrSUhu6KK",
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN"
    }
    records = (p 
        | "Read from source" >> ReadFromKafka(consumer_config=kafka_config, topics=["warming_urls"])
        | "Extract the value" >> beam.Map(lambda x: x[1])
        | "Write to destination" >> WriteToPubSub(topic="projects/cdn-warming-poc/topics/warming_urls")
    )