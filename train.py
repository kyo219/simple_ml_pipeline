import pandas as pd
import lightgbm as lgb
import pickle
import json
import sys
from google.cloud import storage
import io

def train_model(input_dict):
    # GCSからCSVファイルをダウンロードして読み込む
    data = load_csv_from_gcs(input_dict['bucket_name'], 'train/train.csv')

    # 特徴量とターゲットの指定
    X = data[input_dict['training_col_names']]
    y = data[input_dict['y_col_name']]

    # LightGBMのデータセットを作成
    train_data = lgb.Dataset(X, label=y)

    # モデルの学習
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss'
    }
    model = lgb.train(params, train_data, num_boost_round=100)

    # モデルの保存
    model_filename = 'model.pkl'
    with open(model_filename, 'wb') as model_file:
        pickle.dump(model, model_file)
    print("Model trained and saved locally as model.pkl")

    # モデルをGCSにアップロード
    upload_to_gcs(input_dict['bucket_name'], model_filename, 'latest/model.pkl')

def load_csv_from_gcs(bucket_name, blob_name):
    """GCSからCSVファイルをダウンロードしてDataFrameとして読み込む"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    data = blob.download_as_string()
    df = pd.read_csv(io.StringIO(data.decode('utf-8')))
    
    return df

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """ファイルをGCSにアップロードする"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

if __name__ == '__main__':
    # JSONファイルのパスを引数から受け取る
    json_path = sys.argv[1]

    # JSONファイルを読み込む
    with open(json_path, 'r') as f:
        input_dict = json.load(f)
    
    train_model(input_dict)
