# cdn-warming-poc

## Introduction
This project showcases taking messages containing a URL from a Kafka topic, translating them into pub/sub messages and then using push subscriptions to invoke Cloud Run instances to process the messages, take the URL and make a GET call to the url.

## Goals
1. We show that Pub/Sub push will scale Cloud Run instances to deal with all the messages coming through
1. We show how a Dataflow job can be used to get messages from Kafka and send them to Pub/Sub

## Setup & Installation
> **NOTE:** We're assuming that your environment will be the Google Cloud Shell which already has the necessary tooling. If you're using your own machine, you'll have some installs to do

### Setting up Kafka
For ease of use, get a free trial instance of Kafka from Confluent. You will need to fill in the information for instance and username/password in the `kafka-env` file.

In your Kafka environment set up a topic, eg: `cdn_warming`.  You'll need this value later.

### Setting up your Python environment
We'll be using a virtual environment to keep things neat and tidy for our Python code.

1. Navigate to the root of this repository
    ```
    cd ./cdn-warming-poc
    ```

1. Create the virtual python environment

    ```
    python -m venv .venv
    source ./.venv/bin/activate
    ```
    > **NOTE:** You need to activate every time you do not see "`(.venv)`" in your command prompt using this command:
    ```
    source ./.venv/bin/activate 
    ```

1. Install required Python libraries

    ```
    pip install -r ./requirements.txt
    ```

### Setting up Pub/Sub
You will need to create the Pub/Sub topic, as well as a Service Account to invoke Cloud Run from Pub/Sub message pushes. 

Run the following command with whatever substitutions you want:

```bash
./scripts/pubsub-setup.sh { topic_name } 
```
`topic_name`: The name of a new Pub/Sub topic, eg: `cdn_warming`

### Setting up Artifact Registry
> Need to create an Artifact registry for docker and get its URL, eg: `us-central1-docker.pkg.dev/cdn-warming-poc/registry-docker`

### Setting up Cloud Build trigger
> Need to set up Cloud Build to point to ./cloudbuild-pubsub.yaml (or rename it) and use the artifact registry URL (which might be hardcoded in the file)

> Need to set up a 2nd gen source repo connection to this repository.

> Need to hook up the trigger to this source repo and set it to manual invocation.

### Create Cloud Run Instances
> How to run the `create-cloudrun.sh` and copy the endpoint url

### Create Subscriptions
> How to run the `pubsub-create-sub.sh` and pass in the endpoint url of the Cloud Run to push to

## Running The Demo
> Generally you, produce messages, watch the logs for print out, watch the instance count for each cloud run, look at the uniqueness of the container IDs
