超シンプルなML pipeline (GCP)を組んでみる.

### できてること
- [x] 該当フォルダが更新されたとき自動で学習が回り, モデル.pklと設定がgcsに置かれる.

### できてないこと（やる）
- [ ] リファクタ
- [ ] Api化(fast api)して、GCSのlatestモデルとsettingを読み込み、適当な引数を持って予測ができるようにする

### やらないこと
- [ ] 学習をもっとリッチにする

### もしかしたらやるかも
- [ ] Apiのデプロイ
- [ ] Flutterでフロント描く
- [ ] WebPageのデプロイ

---
### 1. localからtraining
```bash
sh local_training.sh
```

### 2. Cloud Functionのデプロイ
```bash
chmod +x deploy_cloud_function.sh
./deploy_cloud_function.sh
```

---
