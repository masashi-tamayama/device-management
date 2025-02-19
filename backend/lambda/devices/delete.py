import json
from common.db import get_db_connection

def handler(event, context):
    """デバイスを削除するLambda関数"""
    try:
        # パスパラメータからデバイスIDを取得
        device_id = event['pathParameters']['id']
        
        # データベース接続
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # デバイスの存在確認
            cursor.execute("SELECT id FROM devices WHERE id = %s", (device_id,))
            if not cursor.fetchone():
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        'error': 'Device not found'
                    })
                }
            
            # デバイスの削除
            cursor.execute("DELETE FROM devices WHERE id = %s", (device_id,))
            connection.commit()
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Device deleted successfully',
                    'device_id': device_id
                })
            }
            
        except Exception as e:
            print(f"データベースエラー: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Internal server error'
                })
            }
            
        finally:
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"エラー: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(e)
            })
        } 