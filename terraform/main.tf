# 1. Terraform 本体の設定（バックエンドなど）
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }

  backend "gcs" {
    bucket  = "your-name-tfstate-bucket" # 作成した実際のバケット名に書き換えてください
    prefix  = "terraform/state"
  }
}

# 2. プロバイダーの設定
provider "google" {
  project = var.project_id
  region  = var.region
}

# 3. BigQuery データセットの作成
resource "google_bigquery_dataset" "portfolio_dataset" {
  dataset_id                  = var.dataset_id
  location                    = var.region
  friendly_name               = "Portfolio Data"
  description                 = "APIから取得した暗号化データを格納する場所"
  delete_contents_on_destroy = true 
}

# 4. テーブルの作成
resource "google_bigquery_table" "raw_api_data" {
  dataset_id = google_bigquery_dataset.portfolio_dataset.dataset_id
  table_id   = "raw_data"

  schema = <<EOF
[
  {"name": "id", "type": "STRING", "mode": "NULLABLE"},
  {"name": "encrypted_content", "type": "STRING", "mode": "NULLABLE"},
  {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"}
]
EOF
}
