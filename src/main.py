import os
import json
from datetime import datetime
from google.cloud import bigquery
from encrypt_logic import DataEncryptor  # 先ほど作成したクラス

def load_to_bigquery(rows_to_insert):
    """BigQueryの指定したテーブルにデータをロードする"""
    client = bigquery.Client()
    
    # 環境変数からプロジェクトIDとデータセット・テーブル名を取得
    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_id = os.getenv("BQ_DATASET_ID", "api_encrypted_store")
    table_id = os.getenv("BQ_TABLE_ID", "raw_data")
    
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    # BigQueryへデータを挿入
    errors = client.insert_rows_json(table_ref, rows_to_insert)
    
    if errors == []:
        print(f"成功: {len(rows_to_insert)} 件のデータをロードしました。")
    else:
        print(f"エラーが発生しました: {errors}")
        raise Exception("BigQueryへのロードに失敗しました")

def main():
    # 1. 疑似的なAPIデータ（本来は requests.get などで取得）
    api_response = [
        {"id": "user_001", "content": "個人情報データA"},
        {"id": "user_002", "content": "個人情報データB"}
    ]
    
    # 2. 暗号化の準備
    aes_key = os.getenv("AES_ENCRYPT_KEY", "default-secret-key-32chars-!!")
    encryptor = DataEncryptor(aes_key)
    
    # 3. データを暗号化してBigQuery用の形式に変換
    rows = []
    for item in api_response:
        encrypted_text = encryptor.encrypt(item["content"])
        rows.append({
            "id": item["id"],
            "encrypted_content": encrypted_text,
            "created_at": datetime.utcnow().isoformat()
        })
    
    # 4. BigQueryへロード
    load_to_bigquery(rows)

if __name__ == "__main__":
    main()
