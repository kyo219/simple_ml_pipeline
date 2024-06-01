#!/bin/bash

### Dockerイメージのビルド
docker build -t lightgbm-trainer .

### コンテナの実行
docker run -it --rm lightgbm-trainer