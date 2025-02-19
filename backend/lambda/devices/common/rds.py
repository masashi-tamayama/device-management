import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import logging
from typing import Dict, List, Optional
from .db_interface import DatabaseInterface

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数の読み込み
load_dotenv()

class RDSInterface(DatabaseInterface):
    """RDS(MySQL)を使用したデバイス管理クラス"""
    
    def __init__(self):
        """データベース接続を初期化"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            logger.info(f"RDSデータベース {os.getenv('DB_NAME')} に接続しました")
        except Error as e:
            logger.error(f"データベース接続エラー: {str(e)}")
            raise

    def __del__(self):
        """デストラクタ: 接続を閉じる"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            logger.info("データベース接続を閉じました")

    def create_device(self, device_data: Dict) -> Dict:
        """デバイスを作成する"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = """
                INSERT INTO devices (id, name, manufacturer)
                VALUES (%(id)s, %(name)s, %(manufacturer)s)
            """
            cursor.execute(query, device_data)
            self.connection.commit()
            logger.info(f"デバイスを作成しました: {device_data['id']}")
            return device_data
        except Error as e:
            logger.error(f"デバイス作成エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def get_device(self, device_id: str) -> Optional[Dict]:
        """デバイスを取得する"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM devices WHERE id = %s"
            cursor.execute(query, (device_id,))
            device = cursor.fetchone()
            if device:
                logger.info(f"デバイスを取得しました: {device_id}")
            else:
                logger.info(f"デバイスが見つかりません: {device_id}")
            return device
        except Error as e:
            logger.error(f"デバイス取得エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def update_device(self, device_id: str, update_data: Dict) -> Optional[Dict]:
        """デバイスを更新する"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            # 更新可能なフィールドを指定
            allowed_fields = ['name', 'manufacturer']
            update_fields = {k: v for k, v in update_data.items() if k in allowed_fields}
            
            if not update_fields:
                logger.warning(f"更新可能なフィールドがありません: {device_id}")
                return None
            
            # UPDATE文の構築
            set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
            query = f"UPDATE devices SET {set_clause} WHERE id = %s"
            
            # パラメータの準備
            params = list(update_fields.values()) + [device_id]
            
            # 更新の実行
            cursor.execute(query, params)
            self.connection.commit()
            
            # 更新後のデータを取得
            cursor.execute("SELECT * FROM devices WHERE id = %s", (device_id,))
            updated_device = cursor.fetchone()
            
            logger.info(f"デバイスを更新しました: {device_id}")
            return updated_device
        except Error as e:
            logger.error(f"デバイス更新エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def delete_device(self, device_id: str) -> bool:
        """デバイスを削除する"""
        cursor = self.connection.cursor()
        try:
            query = "DELETE FROM devices WHERE id = %s"
            cursor.execute(query, (device_id,))
            self.connection.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"デバイスを削除しました: {device_id}")
            else:
                logger.info(f"削除対象のデバイスが見つかりません: {device_id}")
            return deleted
        except Error as e:
            logger.error(f"デバイス削除エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def list_devices(self) -> List[Dict]:
        """全デバイスを取得する"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM devices"
            cursor.execute(query)
            devices = cursor.fetchall()
            logger.info(f"デバイス一覧を取得しました: {len(devices)}件")
            return devices
        except Error as e:
            logger.error(f"デバイス一覧取得エラー: {str(e)}")
            raise
        finally:
            cursor.close() 