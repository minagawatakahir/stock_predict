# 株価予測アプリ

日本の国策・政策動向データを統合した高精度株価予測システム

## 📚 ドキュメント

- [要件定義書](https://atlas-one-yokohamademo-01.atlassian.net/wiki/spaces/pfLlmM5sxRYx/pages/196739481)
- [全体要件マスタードキュメント](https://atlas-one-yokohamademo-01.atlassian.net/wiki/spaces/pfLlmM5sxRYx/pages/196837498)
- [開発環境セットアップガイド](https://atlas-one-yokohamademo-01.atlassian.net/wiki/spaces/pfLlmM5sxRYx/pages/196870701)

## 🎯 プロジェクト目標

四半期先の株価を高精度で予測し、以下の成功基準を達成：
- **MAPE < 8%**
- **方向性的中率 > 55%**
- **10-20銘柄で予測可能**

## 🏗️ アーキテクチャ

```
┌─────────────────┐
│ データ収集層     │
│ - yfinance      │
│ - e-Stat API    │
│ - BOJ Scraper   │
└────────┬────────┘
         │
┌────────▼────────┐
│  Airflow        │
│  (Orchestration)│
└────────┬────────┘
         │
┌────────▼────────┐
│  TimescaleDB    │
│  (時系列DB)     │
└────────┬────────┘
         │
┌────────▼────────┐
│  ML モデル層    │
│  - XGBoost      │
│  - LSTM         │
│  - Transformer  │
└────────┬────────┘
         │
┌────────▼────────┐
│  FastAPI        │
│  (REST API)     │
└────────┬────────┘
         │
┌────────▼────────┐
│  React Frontend │
└─────────────────┘
```

## 📁 プロジェクト構造

```
stock-prediction-app/
├── airflow/
│   └── dags/
│       └── stock_prediction_pipeline.py   # データ収集DAG
├── api/
│   ├── main.py                            # FastAPIアプリ
│   └── routers/                           # APIルーター
├── data_collection/
│   ├── e_stat_api.py                      # e-Stat APIクライアント
│   └── boj_scraper.py                     # 日銀データスクレイパー
├── db/
│   ├── models.py                          # SQLAlchemyモデル
│   └── database.py                        # DB接続管理
├── ml/
│   └── models/
│       └── xgboost_model.py               # XGBoost予測モデル
├── frontend/
│   └── src/                               # Reactアプリ
├── docker-compose.yml                     # Docker構成
├── requirements.txt                       # Python依存関係
└── .env.example                           # 環境変数テンプレート
```

## 🚀 クイックスタート

### 1. 環境変数設定

```bash
cp .env.example .env
# .envファイルを編集してAPI Keyを設定
```

### 2. Dockerで起動

```bash
# 全サービスを起動
docker-compose up -d

# ログ確認
docker-compose logs -f
```

### 3. データベース初期化

```bash
# Pythonコンテナに入る
docker-compose exec api bash

# マイグレーション実行
python -c "from db.database import init_db, setup_timescale; init_db(); setup_timescale()"
```

### 4. API確認

```bash
# ヘルスチェック
curl http://localhost:8000/

# 予測取得
curl http://localhost:8000/api/v1/predictions/7203.T
```

### 5. Airflow UI

ブラウザで http://localhost:8080 を開く
- ユーザー名: admin
- パスワード: admin

## 📊 データソース

| カテゴリ | ソース | 更新頻度 |
|---------|--------|---------|
| 株価 | Yahoo Finance | 日次 |
| GDP, CPI | e-Stat API | 月次/四半期 |
| 政策金利 | 日本銀行 | 不定期 |
| 国策情報 | 政府プレスリリース | 日次 |

## 🤖 機械学習モデル

### Phase 1 (MVP)
- **XGBoost**: ファンダメンタルズ + マクロ経済 + 国策データ

### Phase 2 (計画中)
- **LSTM**: 時系列トレンド学習
- **Transformer**: 複数時間軸の注意機構
- **Stacking**: 3モデルの統合

## 🧪 テスト実行

```bash
# ユニットテスト
pytest

# カバレッジ付き
pytest --cov=. --cov-report=html
```

## 📋 Jira チケット

- [TAX-1: Phase 1 MVP構築](https://atlas-one-yokohamademo-01.atlassian.net/browse/TAX-1)
- [TAX-4: Airflowパイプライン](https://atlas-one-yokohamademo-01.atlassian.net/browse/TAX-4)

## 🛠️ 開発ワークフロー

1. Jiraでチケット確認
2. フィーチャーブランチ作成 (`git checkout -b feature/TAX-XXX`)
3. コード実装
4. テスト作成・実行
5. プルリクエスト作成
6. レビュー後マージ

## 📈 パフォーマンス目標

- API応答時間: < 500ms
- 予測精度 MAPE: < 8%
- データ更新: 毎日朝9時
- システム稼働率: > 99%

## 🐛 トラブルシューティング

### Docker起動エラー
```bash
# コンテナとボリュームをクリーンアップ
docker-compose down -v
docker-compose up -d
```

### データベース接続エラー
```bash
# PostgreSQLログ確認
docker-compose logs db
```

## 📞 サポート

質問や問題があれば Confluence または Jira でご連絡ください。

## 📝 ライセンス

内部プロジェクト - 非公開
