# What this repo is ?
超シンプルなML pipeline (GCP)を組んでみる. (GPT4の力を借りて...)

---
# PlanPlan

### できてること
- [x] GCS上の該当フォルダが更新されたとき自動で学習が回り, モデル.pklと設定がgcsに置かれる.



https://github.com/kyo219/simple_ml_pipeline/assets/75966417/db27bb3a-0352-4065-9279-9c76e28a85b9



### できてないこと（やる）
- [ ] リファクタ
- [ ] Api化(fast apiを導入)して、GCSに置かれたlatestモデルとsettingを読み込み、適当な引数を持って予測ができるようにする

### やらないこと
- [ ] 学習をもっとリッチにする

### もしかしたらやるかも
- [ ] Apiのデプロイ
- [ ] Flutterでフロント描く
- [ ] WebPageのデプロイ

---
# How to training

### 1. localからtraining
```bash
sh local_training.sh
```

### 2. Cloud Functionのデプロイ
```bash
chmod +x deploy_cloud_function.sh
./deploy_cloud_function.sh
```

### delete cloud run jobs
```bash
sh delete_cloud_run_jobs.sh
```

---
