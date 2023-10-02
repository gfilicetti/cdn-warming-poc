# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
COPY requirements.txt /
COPY src/ /src/

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# set our context
ENV APP_HOME /src
WORKDIR $APP_HOME

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 cdn_prewarm.consumer:app settings.ini
CMD [ "python", "-m", "cdn_prewarm.consumer", "settings.ini" ]
