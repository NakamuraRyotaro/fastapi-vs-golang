from sqlalchemy import create_engine, text

TEST_DATABASE_URL = "sqlite:///:memory:"


def test_database_connection():
    """テスト用 SQLite に接続できることを検証"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    finally:
        engine.dispose()
