from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import get_settings

settings = get_settings()

# 接続先のURLを生成
DATABASE_URL = settings.sqlalchemy_database_url()

# エンジンの作成
engine = create_engine(
   DATABASE_URL,
   echo=settings.sqlalchemy_echo,
   pool_pre_ping=True,
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースモデルの作成
Base = declarative_base()

# セッションを取得する関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
