import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from devices.database import Base
from devices.main import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# テスト用の環境変数を設定
os.environ["DB_TYPE"] = "rds"
os.environ["RDS_HOST"] = "localhost"
os.environ["RDS_PORT"] = "3306"
os.environ["RDS_USER"] = "root"
os.environ["RDS_PASSWORD"] = "okitasouji"
os.environ["RDS_DATABASE"] = "test_lambdadb"

# テスト用のデータベースURL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:okitasouji@localhost:3306/test_lambdadb"

@pytest.fixture(scope="session")
def test_db():
    """テスト用データベースのセットアップとクリーンアップ"""
    # テスト用データベースの作成
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True
    )
    
    # テーブルの作成
    Base.metadata.create_all(bind=engine)
    
    # テスト用セッションの作成
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield engine
    
    # テスト後のクリーンアップ
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client():
    """テストクライアントを提供"""
    return TestClient(app) 