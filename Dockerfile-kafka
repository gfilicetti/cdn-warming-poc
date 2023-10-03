# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
COPY requirements.txt /
COPY src/ /src/
# This crazy copy is needed in case kafka-env isn't present, it will give an error
# but not if there is another file being copied and not if it's a wildcard glob
# versus an exact reference
COPY requirements.txt src/kafka-en[v] /secret/

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# set our context
WORKDIR /src

# run the script directly, it will listen on 8080 plus spawn a thread to listen for Kafka
CMD [ "python", "-m", "cdn_prewarm.consumer-cloudrun", "/secret/kafka-env" ]

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 cdn_prewarm.consumer:app settings.ini
