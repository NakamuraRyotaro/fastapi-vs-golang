# fastapi-vs-golang

Python(FastAPI) と Go の実装を比較するためのリポジトリです。以下は FastAPI 側 (`fastapi_app`) の利用手順です。

## セットアップ

1. Python 3.11 系を用意する。
2. 仮想環境を作成して有効化する。

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. 依存関係をインストールする。

   ```bash
   pip install -r fastapi_app/requirements.txt
   ```

## 環境変数

`fastapi_app/.env` を使ってアプリ設定を上書きできます。最低限、MySQL を利用する場合は以下を設定してください。

```env
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=3306
DB_NAME=...
```

`DATABASE_URL` を指定すればそちらが優先され、指定しない場合は上記情報から MySQL の接続文字列を生成します。どちらも無ければローカルの SQLite (`sqlite:///./app.db`) を使用します。

## アプリケーションの起動

### Docker を利用する場合

```bash
docker-compose up --build
```

FastAPI は `http://127.0.0.1:8000`、Swagger UI は `http://127.0.0.1:8000/docs` で確認できます。Go 側のサービスも同時に立ち上がります。

### ローカルで FastAPI を動かす場合

```bash
cd fastapi_app
uvicorn main:app --reload
```

この場合も Swagger UI は `http://127.0.0.1:8000/docs` から確認できます。

## ディレクトリ構成 (抜粋)

```
fastapi-vs-golang/
├── benchmark/                  # ベンチマーク関連スクリプト・データ
├── data/                       # 共有データ置き場
├── docs/                       # ドキュメント類
├── docker-compose.yml          # ローカル開発用コンテナ設定
├── fastapi_app/
│   ├── .env                    # FastAPI 側の環境変数の設定
│   ├── Dockerfile              # FastAPI コンテナ定義
│   ├── alembic/
│   │   └── versions/           # マイグレーションスクリプト
│   ├── alembic.ini             # Alembic 設定
│   ├── app/
│   │   ├── config/
│   │   │   └── settings.py     # Pydantic Settings による設定読み込み
│   │   ├── db/
│   │   │   └── database.py     # Engine/Session 定義と依存性プロバイダ
│   │   ├── models/
│   │   │   ├── todo.py
│   │   │   └── user.py         # SQLAlchemy モデル定義
│   │   ├── repositories/
│   │   │   ├── todo_repository.py
│   │   │   └── user_repository.py  # DB アクセス層
│   │   ├── services/
│   │   │   ├── todo_service.py
│   │   │   └── user_service.py     # ビジネスロジック層
│   │   ├── routers/
│   │   │   ├── todo_router.py
│   │   │   └── user_router.py      # FastAPI ルーター定義
│   │   └── schemas/
│   │       ├── todo_schema.py
│   │       └── user_schema.py  # Pydantic スキーマ
│   ├── main.py                 # FastAPI エントリポイント
│   ├── pytest.ini              # Pytest 設定
│   ├── requirements.txt        # Python 依存パッケージ定義
│   └── tests/
│       ├── repositories/       # リポジトリ層のユニットテスト
│       ├── routers/            # ルーター/API エンドポイントのテスト
│       ├── services/           # サービス層のユニットテスト
│       └── conftest.py         # in-memory SQLite を共有するフィクスチャ
├── go_app/                     # Go 実装（ディレクトリ構成は順次整備）
└── README.md                   # このドキュメント
```

## テスト

```bash
cd fastapi_app
pytest
```

テストでは in-memory SQLite を使用するため、MySQL を起動する必要はありません。

## Go 側

`go_app` ディレクトリに Go 実装を置く予定です。現在実装進行中で、順次アップデート予定です。
