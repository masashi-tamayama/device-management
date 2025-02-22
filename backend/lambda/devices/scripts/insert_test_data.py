import os
import sys
import uuid
from datetime import datetime
import logging
from dotenv import load_dotenv

# commonディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.db_interface import get_db_interface

# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境変数の読み込み
load_dotenv()

# テスト用の環境変数を一時的に設定
os.environ['RDS_HOST'] = 'localhost'
os.environ['RDS_PORT'] = '3306'
os.environ['RDS_USER'] = 'root'
os.environ['RDS_PASSWORD'] = 'okitasouji'
os.environ['RDS_DATABASE'] = 'lambdadb'

def generate_test_data():
    """テストデータを生成する"""
    return [
        {
            'id': str(uuid.uuid4()),
            'name': 'エアコン',
            'manufacturer': 'パナソニック',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': '冷蔵庫',
            'manufacturer': '日立',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': '洗濯機',
            'manufacturer': 'シャープ',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': '電子レンジ',
            'manufacturer': '東芝',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': '掃除機',
            'manufacturer': 'ダイソン',
            'created_at': datetime.now().isoformat()
        }
    ]

def insert_test_data():
    """テストデータを投入する"""
    try:
        # データベースインターフェースの取得
        db = get_db_interface()
        logger.info(f"データベースに接続しました（タイプ: {os.getenv('DB_TYPE', 'rds')}）")

        # 既存のデータを確認
        existing_devices = db.list_devices()
        logger.info(f"既存のデバイス数: {len(existing_devices)}件")

        # テストデータの生成と投入
        test_devices = generate_test_data()
        for device in test_devices:
            try:
                db.create_device(device)
                logger.info(f"デバイスを作成しました: {device['name']} ({device['manufacturer']})")
            except Exception as e:
                logger.error(f"デバイス作成エラー: {str(e)}")
                continue

        # 投入後のデータを確認
        updated_devices = db.list_devices()
        logger.info(f"テストデータ投入完了。合計デバイス数: {len(updated_devices)}件")

    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    logger.info("テストデータ投入を開始します...")
    insert_test_data()
    logger.info("テストデータ投入が完了しました。") 