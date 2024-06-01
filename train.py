import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import pickle
import json
import sys
from google.cloud import storage
import io
from datetime import datetime

def preprocess_data(df, input_dict):
    # 不要なcolを削除
    df= df[[input_dict['y_col_name']] + input_dict['training_col_names']]
    # ダミー変数の作成
    df = pd.get_dummies(df, columns=input_dict['dummie_cols'])
    # 上記で特徴量の追加があったので, x_col_listを定義し直す.
    x_col_list = list(set(df.columns.to_list()) - set([input_dict['y_col_name']]))
    return df, x_col_list

def train_pipeline(input_dict):
    # GCSからCSVファイルをダウンロードして読み込む
    df_raw = load_csv_from_gcs(input_dict['bucket_name'], f'{input_dict["dataset_name"]}/train_raw/latest/train.csv')
    # 前処理
    df_preprocessed, x_cols = preprocess_data(df_raw, input_dict)
    X = df_preprocessed[x_cols]
    y = df_preprocessed[input_dict['y_col_name']]
    # データを訓練用とテスト用に分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # LightGBMのデータセットを作成
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test)
    # モデルの学習
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss'
    }
    model = lgb.train(params, train_data, num_boost_round=100)
    # テストデータに対する予測
    y_pred = model.predict(X_test)
    # 予測値を二値化（0.5を閾値とする）
    y_pred_binary = (y_pred > 0.5).astype(int)
    # F1スコアの計算
    f1score = f1_score(y_test, y_pred_binary)
    # === GCSへの出力 ===
    # 日付をとっておく
    date_str = datetime.now().strftime('%Y-%m-%d')
    # モデルの保存(local)
    model_filename = 'model.pkl'
    with open(model_filename, 'wb') as model_file:
        pickle.dump(model, model_file)
    print("Model trained and saved locally as model.pkl")
    # モデルをGCSにアップロード（latest）
    upload_to_gcs(input_dict['bucket_name'], model_filename, f'{input_dict["dataset_name"]}/latest/model.pkl')
    # モデルをGCSにアップロード（日付）
    upload_to_gcs(input_dict['bucket_name'], model_filename, f'{input_dict["dataset_name"]}/{date_str}/model.pkl')
    # (predict時必要となる)設定ファイルをGCSにアップロード
    output_settings = {
        "x_cols":x_cols, "y_col":input_dict['y_col_name'], "f1_score":f1score, "date":date_str
    }
    with open('output_setting.json', 'w') as f:
        json.dump(output_settings, f)
    # latest
    upload_to_gcs(input_dict['bucket_name'], 'output_setting.json', f'{input_dict["dataset_name"]}/settings/latest/model_setting.json')
    # 日付
    upload_to_gcs(input_dict['bucket_name'], 'output_setting.json', f'{input_dict["dataset_name"]}/settings/{date_str}/model_setting.json')
    print('=== train pipeline is end! ===')

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
    
    train_pipeline(input_dict)
