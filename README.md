

simple な docker と gcpを使った ml piplineを１から組んでみるテスト.

### やること
- [x] 学習pipelineの構築 (gcsで読み書き)
- [x] 該当フォルダが更新されたとき自動でtrainingされるように(cloud function)
- [ ] リファクタ
- [ ] Api化(fast api)
- [ ] Apiのデプロイ

### 1. localからtraining
```bash
sh local_training.sh
```

### 2. Cloud Functionのデプロイ
```bash
chmod +x deploy_cloud_function.sh
./deploy_cloud_function.sh
```


