import os
import mysql.connector
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

def get_db_connection():
    """データベース接続を取得する関数"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"データベース接続エラー: {err}")
        raise

def init_db():
    """データベースとテーブルを初期化する関数"""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # devicesテーブルの作成
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL COMMENT '機器名',
                manufacturer VARCHAR(255) NOT NULL COMMENT 'メーカー名',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"テーブル作成エラー: {err}")
        raise
    finally:
        cursor.close()
        connection.close()