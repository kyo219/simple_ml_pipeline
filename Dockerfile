FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir pandas
RUN pip install --no-cache-dir lightgbm
RUN pip install --no-cache-dir google-cloud-storage
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir google-cloud-run
RUN pip install --no-cache-dir protobuf
# RUN pip install --no-cache-dir -r requirements.txt --- 一旦なし

# スクリプトと認証ファイル、設定ファイルをコンテナにコピー
COPY train.py .
COPY secret/service-account.json /app/service-account.json
COPY model_setting.json /app/model_setting.json

# 環境変数の設定
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account.json"

# デフォルトの実行コマンド
CMD ["python", "train.py", "/app/model_setting.json"]
