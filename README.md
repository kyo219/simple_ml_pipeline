

simple な docker と gcpを使った ml piplineを１から組んでみるテスト.


# Dockerイメージのビルド
docker build -t lightgbm-trainer .

# コンテナの実行
docker run -it --rm lightgbm-trainer
