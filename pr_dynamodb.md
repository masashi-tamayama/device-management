# DynamoDB セットアップ

## 📝 変更内容

### 1. データベースインターフェースの実装
#### 1.1 抽象クラスの作成 (`backend/lambda/devices/common/db_interface.py`)
```python
class DatabaseInterface(ABC):
    """データベース操作の抽象クラス"""
    @abstractmethod
    def create_device(self, device_data: Dict) -> Dict:
        """デバイスを作成する"""
        pass
    
    @abstractmethod
    def get_device(self, device_id: str) -> Optional[Dict]:
        """デバイスを取得する"""
        pass
    # ... 他のCRUD操作メソッド
```

#### 1.2 DynamoDB実装 (`backend/lambda/devices/common/dynamodb.py`)
```python
class DynamoDBInterface(DatabaseInterface):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
        self.table = self.dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))

    def create_device(self, device_data: Dict) -> Dict:
        self.table.put_item(Item=device_data)
        return device_data
    # ... 他のCRUD操作メソッド
```

#### 1.3 RDS実装 (`backend/lambda/devices/common/rds.py`)
```python
class RDSInterface(DatabaseInterface):
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    # ... CRUD操作メソッド
```

### 2. DynamoDBテーブルの作成
```bash
aws dynamodb create-table \
    --table-name devices \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=name,AttributeType=S \
        AttributeName=manufacturer,AttributeType=S \
    --key-schema \
        AttributeName=id,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --global-secondary-indexes '[
        {
            "IndexName": "name-index",
            "KeySchema": [{"AttributeName": "name", "KeyType": "HASH"}],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        },
        {
            "IndexName": "manufacturer-index",
            "KeySchema": [{"AttributeName": "manufacturer", "KeyType": "HASH"}],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    ]'
```

### 3. Lambda関数の修正
各Lambda関数（create.py, read.py, update.py, delete.py）を修正し、新しいデータベースインターフェースを使用するように変更。

#### 例：create.py
```python
def handler(event, context):
    try:
        body = json.loads(event['body'])
        device_id = str(uuid.uuid4())
        device_data = {
            'id': device_id,
            'name': body['name'],
            'manufacturer': body['manufacturer']
        }
        
        db = get_db_interface()
        created_device = db.create_device(device_data)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'デバイスを作成しました',
                'device': created_device
            })
        }
    except Exception as e:
        logger.error(f"エラー: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

### 4. テストデータ投入スクリプトの作成
`backend/lambda/devices/scripts/insert_test_data.py`を作成し、以下のテストデータを投入：
- エアコン（パナソニック）
- 冷蔵庫（日立）
- 洗濯機（シャープ）
- 電子レンジ（東芝）
- 掃除機（ダイソン）

## ✅ 動作確認結果

### 1. DynamoDBテーブルの作成
```bash
$ aws dynamodb describe-table --table-name devices
{
    "Table": {
        "TableName": "devices",
        "TableStatus": "ACTIVE",
        "AttributeDefinitions": [
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "name", "AttributeType": "S"},
            {"AttributeName": "manufacturer", "AttributeType": "S"}
        ],
        ...
    }
}
```

### 2. テストデータの投入
```bash
$ python devices/scripts/insert_test_data.py
INFO:__main__:テストデータ投入を開始します...
INFO:root:Using DynamoDB interface
INFO:root:DynamoDBテーブル devices に接続しました
INFO:__main__:データベースに接続しました（タイプ: dynamodb）
...
INFO:__main__:テストデータ投入完了。合計デバイス数: 7件
```

### 3. データの確認
```bash
$ aws dynamodb scan --table-name devices
{
    "Items": [
        {
            "id": {"S": "dev-001"},
            "name": {"S": "エアコン"},
            "manufacturer": {"S": "パナソニック"},
            ...
        },
        ...
    ],
    "Count": 7
}
```

## 📝 環境変数の設定
`.env`ファイルに以下の設定を追加：
```
DB_TYPE=dynamodb
DYNAMODB_TABLE_NAME=devices
AWS_REGION=ap-northeast-1
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
```

## 🔄 切り替え方法
データベースの切り替えは環境変数`DB_TYPE`で制御：
- `DB_TYPE=dynamodb` → DynamoDBを使用
- `DB_TYPE=rds`（または未設定）→ RDSを使用 