import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# データベース接続情報
DB_TYPE = os.getenv("DB_TYPE", "rds")
RDS_HOST = os.getenv("RDS_HOST", "localhost")
RDS_PORT = os.getenv("RDS_PORT", "3306")
RDS_USER = os.getenv("RDS_USER", "root")
RDS_PASSWORD = os.getenv("RDS_PASSWORD", "")
RDS_DATABASE = os.getenv("RDS_DATABASE", "lambdadb")

# SQLAlchemy用のデータベースURL（文字コード設定を追加）
DATABASE_URL = f"mysql+mysqlconnector://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}?charset=utf8mb4&collation=utf8mb4_unicode_ci"

# エンジンの作成（文字コード設定を追加）
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
        "collation": "utf8mb4_unicode_ci"
    }
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 