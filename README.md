# device-management

# 🔧 機器管理システム

## 📌 プロジェクト概要
本プロジェクトは、AWS 環境で動作する **機器管理システム** です。  
機器の登録・編集・削除・一覧表示を行い、データは **RDS（MySQL）または DynamoDB** に保存されます。

## 📂 ディレクトリ構成
```
device-management/
│── backend/    # バックエンド（Lambda）
│   ├── lambda/ # AWS Lambda のコード置き場
│   │   ├── requirements.txt  # 依存ライブラリ（空のファイル）
│── frontend/   # フロントエンド（Reactなど）
│── README.md   # プロジェクトの説明
```

---

## 🏗️ 使用技術
### **フロントエンド**
- React（または Vue.js）
- AWS S3 + CloudFront

### **バックエンド**
- AWS Lambda（Python）
- API Gateway
- FastAPI
- MySQL（RDS）または DynamoDB

---

## 🚀 機能一覧
- 🔹 **機器一覧画面**
  - 登録された機器を一覧表示
- 🔹 **機器登録**
  - 新しい機器を登録
- 🔹 **機器編集**
  - 登録済み機器を更新
- 🔹 **機器削除**
  - 機器情報を削除

---

## 🔧 環境構築手順

### **1. GitHub リポジトリの作成**
開発を管理するために **GitHubリポジトリ** を作成します。

📌 **手順**
1. [GitHub](https://github.com/) にアクセスし、アカウントにログイン
2. **「New Repository（新しいリポジトリ）」** を作成
   - **リポジトリ名:** `device-management`
   - **Public（公開） or Private（非公開）:** 任意
   - **Readmeの追加:** 追加する
3. **作成したリポジトリのURLをコピー**

---

### **2. システム構成**
本システムは、AWS を活用して以下の構成で動作します。

---

#### **① フロントエンド（S3 + CloudFront）**
📌 **S3（Amazon Simple Storage Service）とは？**  
S3 は **静的なウェブサイトや画像、動画などのファイルを保存できるクラウドストレージ** です。  
React で作成したフロントエンドは、静的ファイル（HTML/CSS/JS）として出力されるため、S3 にアップロードすれば **サーバー不要で Web サイトを公開** できます。

📌 **CloudFront とは？**  
CloudFront は **CDN（コンテンツ配信ネットワーク）** の AWS サービスで、S3 に置いた静的ファイルを高速・安全に配信できます。

📌 **なぜ S3 + CloudFront を使うのか？**
- **S3** → フロントエンドの静的ファイルを保存
- **CloudFront** → ユーザーが素早くアクセスできるようにキャッシュ＆配信

💡 **React のプロジェクトを `npm run build` でビルドし、その出力フォルダを S3 にアップロードすれば、すぐに公開できます。**

---

#### **② バックエンド（API Gateway + Lambda）**
本システムのバックエンドは、AWS Lambda を使用してサーバーレスで動作します。

📌 **バックエンドの構成**
| 項目 | 説明 |
|----|----|
| **言語** | Python |
| **フレームワーク** | AWS Lambda（サーバーレスの実行環境） |
| **API** | API Gateway（フロントエンドと Lambda を繋ぐためのサービス） |

📌 **なぜ Lambda を使うのか？**
- **サーバー不要**（EC2 のようにサーバーを用意しなくてよい）
- **イベントドリブン**（API Gateway 経由でリクエストが来た時だけ処理を実行するのでコスト削減）
- **スケーラブル**（リクエスト数が増えても自動でスケール）

📌 **Lambda の基本的な動き**
1. **React（フロントエンド）から APIリクエスト**
2. **API Gateway がリクエストを受け取り、Lambda に転送**
3. **Lambda が Python コードを実行 し、データベース（RDS/DynamoDB）とやり取り**
4. **処理結果を API Gateway 経由でフロントエンドに返す**

---

#### **③ データベース（RDS vs DynamoDB）**
本システムでは、データの保存方法として **RDS（MySQL）** または **DynamoDB** を利用できます。

📌 **データベースの選択**
| パターン | データベース | 保存形式 |
|----|----|----|
| **パターン1** | RDS（MySQL） | JSON として受け取るが、内部ではリレーショナル形式（テーブル） |
| **パターン2** | DynamoDB | JSON 形式のまま保存（NoSQL） |

📌 **RDS（MySQL）のデータ保存方法**
RDS は **リレーショナルデータベース** なので、データは **テーブル形式** で保存されます。

```sql
CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL
);
```
📌 **DynamoDB のデータ保存方法**
DynamoDB は **NoSQLデータベース** なので、データはそのまま JSON 形式で保存されます。

```json
{
    "id": "device123",
    "name": "エアコン",
    "manufacturer": "Panasonic"
}
```

📌 **どちらも JSON 形式で保存する？**
- **MySQL（RDS）** → JSON 形式で受け取るが、内部ではテーブルに変換  
- **DynamoDB** → そのまま JSON 形式で保存

💡 **つまり、フロントエンドから送るデータは JSON 形式ですが、RDS と DynamoDB では保存の仕方が違います。**

---

### **④ まとめ**
| 項目 | 説明 |
|----|----|
| **フロントエンド** | React を使用し、S3 に静的ファイルを配置し、CloudFront で配信 |
| **バックエンド** | AWS Lambda（Python）を API Gateway 経由で呼び出す |
| **データベース** | RDS（MySQL）はリレーショナルデータとして保存、DynamoDB は JSON のまま保存 |
