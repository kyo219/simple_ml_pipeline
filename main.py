import os
from google.cloud import storage
from google.cloud import run_v2
# from google.protobuf import duration_pb2

def trigger_training_pipeline(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
    This function is triggered when a file is uploaded to the specified Cloud Storage bucket.

    Args:
        event (dict): The dictionary with data specific to this type of event.
        context (google.cloud.functions.Context): Metadata of triggering event.
    """
    file_name = event['name']
    if file_name == 'train_raw/latest/train.csv':
        # Trigger Cloud Run service
        run_training_pipeline()

def run_training_pipeline():
    client = run_v2.ServicesClient()
    project = os.getenv('GCP_PROJECT')
    location = os.getenv('GCP_LOCATION')
    service = os.getenv('CLOUD_RUN_SERVICE')
    
    # Configure the request
    request = run_v2.RunServiceRequest(
        name=f"projects/{project}/locations/{location}/services/{service}"
    )
    
    response = client.run_service(request=request)
    print(f"Triggered training pipeline: {response}")
