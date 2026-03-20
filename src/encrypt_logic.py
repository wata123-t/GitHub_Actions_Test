import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class DataEncryptor:
    def __init__(self, key: str):
        # AES-256のため、キーは32バイトである必要があります
        # GitHub Secretsから渡す環境変数を想定
        self.key = key.encode('utf-8')[:32].ljust(32, b'\0')

    def encrypt(self, plain_text: str) -> str:
        """データをAES暗号化し、IVと暗号文を結合してBase64で返す"""
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # パディング（16バイト境界に合わせる）して暗号化
        ct_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
        
        # IV + 暗号文 をまとめてBase64エンコード（BigQueryに入れやすくするため）
        return base64.b64encode(iv + ct_bytes).decode('utf-8')

    def decrypt(self, encrypted_base64: str) -> str:
        """Base64形式のデータを復号する（検証用）"""
        data = base64.b64decode(encrypted_base64)
        iv = data[:AES.block_size]
        ct = data[AES.block_size:]
        
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')

# 実行例
if __name__ == "__main__":
    # 実際は os.environ.get("AES_KEY") などで取得
    SECRET_KEY = "my-super-secret-key-12345" 
    encryptor = DataEncryptor(SECRET_KEY)

    raw_data = "APIからの機密データ: ユーザーID 001"
    encrypted = encryptor.encrypt(raw_data)
    
    print(f"暗号化前: {raw_data}")
    print(f"暗号化後: {encrypted}")
    print(f"復号テスト: {encryptor.decrypt(encrypted)}")
