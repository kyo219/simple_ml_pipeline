#!/bin/bash

# gcs_setting.json から設定を読み込む
CONFIG_FILE="secret/gcs_setting.json"
PROJECT_ID=$(jq -r '.project_id' $CONFIG_FILE)
REGION=$(jq -r '.region' $CONFIG_FILE)
BUCKET_NAME=$(jq -r '.bucket_name' $CONFIG_FILE)

# Dockerイメージのビルド
docker build -t gcr.io/$PROJECT_ID/lightgbm-trainer .
# DockerイメージをGoogle Container Registryにプッシュ
docker push gcr.io/$PROJECT_ID/lightgbm-trainer

# Cloud Run Job の作成
gcloud beta run jobs create lightgbm-training-job \
    --image gcr.io/$PROJECT_ID/lightgbm-trainer \
    --region $REGION \
    --set-env-vars GCP_PROJECT=$PROJECT_ID,GCP_LOCATION=$REGION,CLOUD_RUN_SERVICE=lightgbm-trainer

# Cloud Run Job の実行
gcloud beta run jobs execute lightgbm-training-job --region $REGION

# Cloud Function のデプロイ
gcloud functions deploy triggerTrainingPipeline \
    --runtime python39 \
    --trigger-resource $BUCKET_NAME \
    --trigger-event google.storage.object.finalize \
    --entry-point trigger_training_pipeline \
    --set-env-vars GCP_PROJECT=$PROJECT_ID,GCP_LOCATION=$REGION,CLOUD_RUN_SERVICE=lightgbm-trainer