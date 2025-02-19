-- デバイス管理用のデータベースを作成
CREATE DATABASE IF NOT EXISTS lambdadb;
USE lambdadb;

-- デバイステーブルの作成
CREATE TABLE IF NOT EXISTS devices (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT '機器名',
    manufacturer VARCHAR(255) NOT NULL COMMENT 'メーカー名',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックスの作成
CREATE INDEX idx_devices_name ON devices(name);
CREATE INDEX idx_devices_manufacturer ON devices(manufacturer);

-- コメントの追加
ALTER TABLE devices
    COMMENT = '機器管理用のテーブル';

ALTER TABLE devices
    MODIFY COLUMN id VARCHAR(36) COMMENT 'デバイスの一意識別子（UUID）',
    MODIFY COLUMN name VARCHAR(255) COMMENT '機器名',
    MODIFY COLUMN manufacturer VARCHAR(255) COMMENT 'メーカー名',
    MODIFY COLUMN created_at TIMESTAMP COMMENT 'レコード作成日時',
    MODIFY COLUMN updated_at TIMESTAMP COMMENT 'レコード更新日時';