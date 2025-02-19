import json
from common.db import get_db_connection

def handler(event, context):
    """デバイスを更新するLambda関数"""
    try:
        # パスパラメータからデバイスIDを取得
        device_id = event['pathParameters']['id']
        
        # リクエストボディの取得
        body = json.loads(event['body'])
        
        # 更新可能なフィールド
        updatable_fields = ['name', 'type', 'location', 'status']
        update_data = {k: v for k, v in body.items() if k in updatable_fields}
        
        if not update_data:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No valid fields to update'
                })
            }
        
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
            
            # UPDATE文の構築
            set_clause = ", ".join([f"{field} = %s" for field in update_data.keys()])
            query = f"UPDATE devices SET {set_clause} WHERE id = %s"
            
            # パラメータの準備
            params = list(update_data.values()) + [device_id]
            
            # 更新の実行
            cursor.execute(query, params)
            connection.commit()
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Device updated successfully',
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