import os
from google.cloud import storage
from google.cloud import pubsub_v1

def trigger_training_pipeline(event, context):
    """Background Cloud Function to be triggered by Cloud Storage."""
    file_name = event['name']
    bucket_name = event['bucket']
    print(f"File: {file_name}, Bucket: {bucket_name}")
    if file_name == 'titanic/train_raw/latest/train.csv':
        publish_message_to_pubsub()

def publish_message_to_pubsub():
    """Publishes a message to a Pub/Sub topic to trigger the Cloud Run job indirectly."""
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GCP_PROJECT'),
        topic='trigger-cloud-run'
    )
    publisher.publish(topic_name, b'Trigger Cloud Run', spam='eggs')