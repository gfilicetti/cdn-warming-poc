# Required connection configs for Kafka producer, consumer, and admin
bootstrap.servers="pkc-n3603.us-central1.gcp.confluent.cloud:9092"
security.protocol="SASL_SSL"
sasl.mechanisms="PLAIN"
sasl.username="RXKZZPZHVYNU2XAJ"
sasl.password="NhQ6zSqNh5C5a2Yup8Xfaa8E7MueU303MU4n8guxrk0W4D8EPyfxmcarrSUhu6KK"

# Best practice for higher availability in librdkafka clients prior to 1.7
session.timeout.ms="45000"

# Required connection configs for Confluent Cloud Schema Registry
schema.registry.url="https://psrc-4rw99.us-central1.gcp.confluent.cloud"
basic.auth.credentials.source="USER_INFO"
basic.auth.user.info="NN27DQO75Z2C4ESU:7EuQsk1hc1kpp5PIPoc8YoE1qwOy+vLlOxa6K7bXFO78gyHtTrMHx1HR1EuH3SLS"
