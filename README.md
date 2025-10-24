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

```bash
cd fastapi_app
uvicorn main:app --reload
```

`http://127.0.0.1:8000/docs` で OpenAPI ドキュメントが確認できます。

## ディレクトリ構成 (抜粋)

```
fastapi_app/
├── app/
│   ├── config/
│   │   └── settings.py         # Pydantic Settings による設定読み込み
│   ├── db/
│   │   └── database.py         # Engine/Session 定義と依存性プロバイダ
│   ├── models/
│   │   ├── todo.py
│   │   └── user.py             # SQLAlchemy モデル定義
│   ├── repositories/
│   │   ├── todo_repository.py
│   │   └── user_repository.py  # DB アクセスを担当
│   ├── services/
│   │   ├── todo_service.py
│   │   └── user_service.py     # ビジネスロジックとバリデーション
│   ├── routers/
│   │   ├── todo_router.py
│   │   └── user_router.py      # FastAPI ルーター
│   └── schemas/
│       ├── todo_schema.py
│       └── user_schema.py      # Pydantic スキーマ
├── tests/
│   ├── repositories/
│   ├── routers/
│   ├── services/
│   └── conftest.py             # in-memory SQLite を共有するフィクスチャ
├── main.py                     # FastAPI エントリポイント
└── requirements.txt            # 依存関係
```

## テスト

```bash
cd fastapi_app
pytest
```

テストでは in-memory SQLite を使用するため、MySQL を起動する必要はありません。

## Go 側

`go_app` ディレクトリに Go 実装が置かれています。現在文章化は進行中で、順次アップデート予定です。
