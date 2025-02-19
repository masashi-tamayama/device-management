import json
import uuid
from common.db import get_db_connection

def handler(event, context):
    """デバイスを作成するLambda関数"""
    try:
        # リクエストボディの取得
        body = json.loads(event['body'])
        
        # 必須フィールドの検証
        required_fields = ['name', 'type']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': f'Missing required field: {field}'
                    })
                }
        
        # デバイスIDの生成
        device_id = str(uuid.uuid4())
        
        # データベース接続
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # デバイスの作成
            query = """
                INSERT INTO devices (id, name, type, location, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                device_id,
                body['name'],
                body['type'],
                body.get('location', ''),  # オプショナル
                body.get('status', 'active')  # デフォルト: active
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            return {
                'statusCode': 201,
                'body': json.dumps({
                    'message': 'Device created successfully',
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