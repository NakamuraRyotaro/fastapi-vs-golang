from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# 接続先のURLを生成
DATABASE_URL = (
   f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
   f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# エンジンの作成
engine = create_engine(
   DATABASE_URL,
   echo=True,
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