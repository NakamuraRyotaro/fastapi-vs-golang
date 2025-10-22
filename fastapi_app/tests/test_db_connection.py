from sqlalchemy import text
from app.db.database import engine

def test_database_connection():
    """DB接続確認（MySQLコンテナが起動していることが前提）"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        raise AssertionError(f"Database connection failed: {e}")