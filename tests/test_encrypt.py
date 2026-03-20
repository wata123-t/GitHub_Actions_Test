import pytest
from src.encrypt_logic import DataEncryptor

# テスト用の固定キー（32バイト相当）
TEST_KEY = "test-secret-key-32chars-for-pytest"

@pytest.fixture
def encryptor():
    """テストごとにEncryptorインスタンスを作成するフィクスチャ"""
    return DataEncryptor(TEST_KEY)

def test_encryption_decryption_cycle(encryptor):
    """暗号化して復号した結果が、元の文字列と一致するかテスト"""
    raw_text = "Hello, GitHub Actions!"
    encrypted = encryptor.encrypt(raw_text)
    decrypted = encryptor.decrypt(encrypted)
    
    assert raw_text == decrypted
    assert raw_text != encrypted  # 暗号化されていること

def test_randomness_of_encryption(encryptor):
    """同じ文字列を暗号化しても、毎回違う暗号文（IVが別）になるかテスト"""
    raw_text = "Sensitive Data"
    encrypted_1 = encryptor.encrypt(raw_text)
    encrypted_2 = encryptor.encrypt(raw_text)
    
    # AES-CBCモードならIVが違うため、暗号文全体も異なるはず
    assert encrypted_1 != encrypted_2

def test_empty_string(encryptor):
    """空文字を渡してもエラーにならず処理できるかテスト"""
    raw_text = ""
    encrypted = encryptor.encrypt(raw_text)
    decrypted = encryptor.decrypt(encrypted)
    
    assert decrypted == ""
