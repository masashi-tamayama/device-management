import pytest
from fastapi.testclient import TestClient
from datetime import datetime, UTC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from devices.main import app
from devices.models import Device
from devices.database import Base, get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_database(test_db):
    """各テストの前にデータベースをクリーンアップ"""
    Base.metadata.drop_all(bind=test_db)
    Base.metadata.create_all(bind=test_db)
    yield

def test_list_devices_empty(test_db):
    """デバイスが存在しない場合のテスト"""
    response = client.get("/api/v1/devices/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_devices_with_data(test_db):
    """デバイスが存在する場合のテスト"""
    # テストデータの作成
    test_devices = [
        Device(
            id="test-device-1",
            name="テストデバイス1",
            manufacturer="テストメーカー1"
        ),
        Device(
            id="test-device-2",
            name="テストデバイス2",
            manufacturer="テストメーカー2"
        )
    ]
    
    # テストデータの保存
    with test_db.connect() as connection:
        for device in test_devices:
            connection.execute(Device.__table__.insert().values(
                id=device.id,
                name=device.name,
                manufacturer=device.manufacturer,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            ))
        connection.commit()
    
    # APIリクエスト
    response = client.get("/api/v1/devices/")
    assert response.status_code == 200
    
    # レスポンスの検証
    devices = response.json()
    assert len(devices) == 2
    assert devices[0]["name"] == "テストデバイス1"
    assert devices[0]["manufacturer"] == "テストメーカー1"
    assert devices[1]["name"] == "テストデバイス2"
    assert devices[1]["manufacturer"] == "テストメーカー2"

def test_list_devices_error_handling(test_db):
    """エラーハンドリングのテスト"""
    # 無効なデータベースエンジンを作成
    invalid_engine = create_engine("mysql+mysqlconnector://invalid:invalid@invalid_host:3306/invalid_db")
    invalid_session = sessionmaker(autocommit=False, autoflush=False, bind=invalid_engine)
    
    # 無効なセッションを使用するようにアプリケーションを設定
    def override_get_db():
        db = invalid_session()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.get("/api/v1/devices/")
        assert response.status_code == 500
        assert "error" in response.json()
    finally:
        # 依存関係の上書きをクリア
        app.dependency_overrides.clear() 