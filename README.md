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


# Python 環境構築（Windows 11）

## 1️⃣ Python のインストール手順（Windows 11）

### ✅ 正しい Python のダウンロード
1. [Python 公式サイト](https://www.python.org/downloads/windows/) にアクセス
2. 「Looking for a specific release?」のセクションから最新の安定版を選択
3. **「Windows installer (64-bit)」** をダウンロード  
   ✅ `python-3.x.x-amd64.exe` を選ぶ（Microsoft Store 版ではない）

### ✅ インストール手順
1. **ダウンロードしたインストーラーを実行**
2. **「Add Python to PATH」にチェックを入れる**
3. **「Install Now」をクリック**
4. **インストール完了後、「Disable path length limit」をクリック**
5. **PC を再起動**

---

## 2️⃣ インストール後の確認と Microsoft Store の影響チェック

### ✅ Python の動作確認
```bash
python --version
python3 --version
pip --version

**成功表示**
Python 3.13.2
Python 3.13.2
pip 24.3.1 from C:\Program Files\Python313\Lib\site-packages\pip (python 3.13)
```

# ✅ AWS CLI のインストール & 設定 (#7/2.3)

## 📝 概要
この手順では、Windows 11 環境で **AWS CLI** を **Microsoft Store 版の影響を受けずに** 正しくインストールし、GitBash で使用できるように設定します。

---

## 📌 **1. AWS CLI のインストール**
### ✅ **AWS CLI を公式サイトからダウンロード & インストール**
1. [AWS CLI 公式ダウンロードページ](https://awscli.amazonaws.com/AWSCLIV2.msi) にアクセス
2. `AWSCLIV2.msi`（Windows 64-bit 版）をダウンロード
3. ダウンロードした `AWSCLIV2.msi` を実行
4. **「Add AWS CLI to PATH」にチェックが入っていることを確認**
5. **「Install」をクリック**
6. インストール完了後、PC を再起動

---

## 📌 **2. AWS CLI の動作確認**
### ✅ **AWS CLI のバージョン確認**
```bash
aws --version
```
**期待する出力**
```
aws-cli/2.x.x Python/3.x.x Windows/11 exe/AMD64
```

---

## 📌 **3. AWS CLI の初期設定**
### ✅ **IAM ユーザーの作成**
1. **AWS マネジメントコンソールにログイン**
2. **[IAM ユーザー作成ページ](https://console.aws.amazon.com/iamv2/home?#/users) にアクセス**
3. **ユーザー名を入力**（例: `okita-cli-user`）
4. **「AWS マネジメントコンソールへのアクセス」を無効化**
5. **「アクセスキーを作成」**
6. **「コマンドラインインターフェイス (CLI)」にチェックを入れる**
7. **適切な説明タグを設定**（例: `AWS CLI access key for local development`）
8. **「作成」**

### ✅ **AWS CLI に認証情報を設定**
IAM ユーザーの **アクセスキー ID & シークレットキー** を取得し、以下のコマンドを実行：

```bash
aws configure
```

**入力内容**
```
AWS Access Key ID [None]: AKIA***************
AWS Secret Access Key [None]: *********************
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

### ✅ **AWS CLI の認証情報確認**
```bash
aws configure list
```

---

## 📌 **4. AWS CLI の動作確認**
### ✅ **現在の AWS アカウント情報を取得**
```bash
aws sts get-caller-identity
```
**期待する出力**
```json
{
    "UserId": "AIDA42PHHUNFXVAGTNQAE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/okita-test"
}
```

### ✅ **S3 バケットの一覧を取得**
```bash
aws s3 ls
```
**バケットが存在しない場合、何も表示されなくても OK！**

### ✅ **EC2 インスタンスの一覧を取得**
```bash
aws ec2 describe-instances
```
**まだ EC2 を作成していなければ `Reservations: []` のように空のリストが表示される。**

---

## ✅ **セットアップ完了！**
✅ **AWS CLI を公式サイトからインストール**  
✅ **環境変数を設定し、AWS CLI が GitBash で使用できることを確認**  
✅ **`aws configure` で IAM ユーザーの認証情報を設定**  
✅ **AWS CLI から AWS に接続 & 操作できることを確認**  

🚀 **これで AWS CLI のセットアップが完了しました！** 🎉

---

# ✅ Node.js（React 用）のインストール (#8/2.4)

## 📝 概要
この手順では、Windows 11 環境に **React 開発用の Node.js** を正しくインストールし、動作確認を行います。

---

## 📌 **1. Node.js のインストール**
### ✅ **公式サイトからダウンロード & インストール**
1. [Node.js 公式ダウンロードページ](https://nodejs.org/ja/download/) にアクセス
2. **「LTS（推奨版）」の Windows 版（64-bit）** を選択し、ダウンロード
3. ダウンロードした `node-vxx.x.x-x64.msi` を実行
4. **「Next」→「I accept the terms」→「Next」**
5. **「Add to PATH」にチェックが入っていることを確認**
6. **「Install」をクリック**
7. インストール完了後、PC を再起動

---

## 📌 **2. Node.js の動作確認**
### ✅ **Node.js & npm のバージョン確認**
```bash
node -v
npm -v
```
**期待する出力（例）**
```
v18.16.1  # Node.js のバージョン（LTS）
9.5.1     # npm のバージョン
```
✅ **`node` と `npm` のバージョンが表示されれば成功！**

---

## 📌 **3. 環境変数の確認**
### ✅ **GitBash で確認**
```bash
echo $PATH | tr ':' '\n' | grep node
```
✅ **`C:\Program Files\nodejs` が含まれていれば OK！**

### ✅ **PowerShell で確認**
```powershell
$env:Path -split ";"
```
✅ **`C:\Program Files\nodejs` がリストにあれば OK！**

---

## 📌 **4. `npx` の動作確認**
React プロジェクトを作成する際に使用する `npx` が動作するか確認。

```bash
npx --version
```
✅ **エラーなくバージョンが表示されれば OK！**

---

## 📌 **5. React プロジェクトの作成テスト**
**React のセットアップが正しくできるか確認するため、一時的なテストプロジェクトを作成。**

```bash
npx create-react-app test-app
```

**正常にプロジェクトが作成できたら削除**
```bash
rm -rf test-app
```
✅ **`npx create-react-app` がエラーなく動作すれば成功！**

---

## ✅ **セットアップ完了！**
✅ **Node.js を公式サイトからインストール**  
✅ **環境変数を設定し、GitBash で `node` & `npm` が動作することを確認**  
✅ **`npx create-react-app` が正常に動作することを確認**  
✅ **開発環境に影響しないクリーンなセットアップを実施**  

---