import json
from common.db import get_db_connection

def handler(event, context):
    """デバイスを取得するLambda関数"""
    try:
        # パスパラメータからデバイスIDを取得
        device_id = event.get('pathParameters', {}).get('id')
        
        # データベース接続
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)  # 結果を辞書形式で取得
        
        try:
            if device_id:
                # 特定のデバイスを取得
                query = "SELECT * FROM devices WHERE id = %s"
                cursor.execute(query, (device_id,))
                device = cursor.fetchone()
                
                if device:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(device, default=str)  # datetime型をJSON変換可能に
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({
                            'error': 'Device not found'
                        })
                    }
            else:
                # 全デバイスを取得
                query = "SELECT * FROM devices"
                cursor.execute(query)
                devices = cursor.fetchall()
                
                return {
                    'statusCode': 200,
                    'body': json.dumps(devices, default=str)
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