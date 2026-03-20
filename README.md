# 🛡️ Secure Data Pipeline with GitHub Actions & BigQuery

## 🌟 プロジェクトの概要
外部APIからデータを取得し、**AES-256暗号化**を施した上で **BigQuery** へロード、さらに **dbt** で品質検証を行うエンドツーエンドのデータパイプラインです。

### 🔑 こだわったポイント
1. **データの安全性 (AES Encryption)**: 
   APIから取得した機密データを、クラウドに保存する直前にPythonで暗号化。ストレージ上でのデータ漏洩リスクを最小限に抑えています。
2. **Infrastructure as Code (Terraform)**: 
   GCPリソース（BigQuery, GCS）をTerraformで定義し、環境の再現性を確保。
3. **品質保証の二段構え**: 
   - **pytest**: 暗号化ロジックの正確性をユニットテストで検証。
   - **dbt test**: ロード後のデータの「一意性」や「非欠損」をSQLレベルで自動検証。
4. **完全自動化 (CI/CD)**: 
   GitHub Actionsにより、プッシュからデプロイ・テストまでを一貫して自動化。

## 🛠️ 使用技術
- **Language**: Python 3.9 (requests, pycryptodome, pytest)
- **Infrastructure**: Terraform (GCP Provider)
- **Data Warehouse**: Google Cloud BigQuery
- **Data Transformation**: dbt-bigquery
- **CI/CD**: GitHub Actions
