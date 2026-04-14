"""
Comprehensive tests for encryption module security
"""

import pytest
from cryptography.fernet import InvalidToken
from utils.encryption import PasswordEncryptor
from config import PASSWORD_CONFIG


class TestPasswordEncryptor:
    """Test password encryption and decryption"""

    def test_encrypt_decrypt_basic(self):
        """Basic encrypt/decrypt should be reversible"""
        password = "MySecurePassword123!"
        master = "MasterKey2024!"
        
        encrypted = PasswordEncryptor.encrypt(password, master)
        decrypted = PasswordEncryptor.decrypt(encrypted, master)
        
        assert decrypted == password

    def test_encrypt_produces_different_output(self):
        """Each encryption should produce different ciphertext (due to IV)"""
        password = "test"
        master = "master"
        
        encrypted1 = PasswordEncryptor.encrypt(password, master)
        encrypted2 = PasswordEncryptor.encrypt(password, master)
        
        # Due to random IV, ciphertexts should differ
        assert encrypted1 != encrypted2

    def test_decrypt_with_wrong_master_fails(self):
        """Decryption with wrong master key should fail or return corrupted data"""
        password = "secret123"
        master1 = "MasterKey1"
        master2 = "MasterKey2"
        
        encrypted = PasswordEncryptor.encrypt(password, master1)
        
        # Should fail with wrong key
        with pytest.raises((InvalidToken, ValueError, Exception)):
            PasswordEncryptor.decrypt(encrypted, master2)

    def test_encrypt_empty_password(self):
        """Encrypting empty password should work"""
        encrypted = PasswordEncryptor.encrypt("", "master")
        decrypted = PasswordEncryptor.decrypt(encrypted, "master")
        assert decrypted == ""

    def test_encrypt_very_long_password(self):
        """Encrypting very long password should work"""
        long_pass = "A" * 10000 + "1!@#"
        master = "MasterKey"
        
        encrypted = PasswordEncryptor.encrypt(long_pass, master)
        decrypted = PasswordEncryptor.decrypt(encrypted, master)
        
        assert decrypted == long_pass

    def test_encrypt_unicode_characters(self):
        """Encrypting unicode should work"""
        passwords = ["café@Pass", "niño123!", "日本語パス", "😀Secure!"]
        master = "master"
        
        for password in passwords:
            encrypted = PasswordEncryptor.encrypt(password, master)
            decrypted = PasswordEncryptor.decrypt(encrypted, master)
            assert decrypted == password

    def test_encrypt_special_characters(self):
        """All special characters should be preserved"""
        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        password = f"Pass{special_chars}"
        master = "key"
        
        encrypted = PasswordEncryptor.encrypt(password, master)
        decrypted = PasswordEncryptor.decrypt(encrypted, master)
        
        assert decrypted == password

    def test_encrypt_null_bytes(self):
        """Encrypt with null bytes in password"""
        password = "pass\x00null"
        master = "key"
        
        # Should handle gracefully
        try:
            encrypted = PasswordEncryptor.encrypt(password, master)
            decrypted = PasswordEncryptor.decrypt(encrypted, master)
            assert decrypted == password or "null" in decrypted
        except (ValueError, TypeError):
            pass  # Acceptable to reject

    def test_master_key_case_sensitive(self):
        """Master key should be case sensitive"""
        password = "secret"
        
        encrypted1 = PasswordEncryptor.encrypt(password, "MasterKey")
        
        # Different case should fail
        with pytest.raises((InvalidToken, ValueError, Exception)):
            PasswordEncryptor.decrypt(encrypted1, "masterkey")

    def test_encrypt_with_short_master_key(self):
        """Short master key should still work"""
        password = "pwd"
        master = "a"
        
        encrypted = PasswordEncryptor.encrypt(password, master)
        decrypted = PasswordEncryptor.decrypt(encrypted, master)
        
        assert decrypted == password

    def test_encrypt_with_very_long_master_key(self):
        """Very long master key should work"""
        password = "secret"
        master = "M" * 1000
        
        encrypted = PasswordEncryptor.encrypt(password, master)
        decrypted = PasswordEncryptor.decrypt(encrypted, master)
        
        assert decrypted == password

    def test_batch_encrypt_decrypt(self):
        """Batch encryption/decryption"""
        passwords = ["pass1", "pass2", "pass3"]
        master = "master"
        
        encrypted = [PasswordEncryptor.encrypt(p, master) for p in passwords]
        decrypted = [PasswordEncryptor.decrypt(e, master) for e in encrypted]
        
        assert decrypted == passwords

    def test_encrypted_format_consistency(self):
        """Encrypted data format should be consistent"""
        password = "test123"
        master = "key"
        
        encrypted = PasswordEncryptor.encrypt(password, master)
        
        # Should be string or bytes
        assert isinstance(encrypted, (str, bytes))
        
        # Should be non-empty
        assert len(encrypted) > 0

    def test_encrypt_with_newlines(self):
        """Password with newlines should encrypt properly"""
        password = "line1\nline2\nline3"
        master = "key"
        
        encrypted = PasswordEncryptor.encrypt(password, master)
        decrypted = PasswordEncryptor.decrypt(encrypted, master)
        
        assert decrypted == password

    def test_storage_format_recovery(self):
        """Should recover original password from storage"""
        passwords = ["simple", "Complex!", "unicode™", "spaces in pwd"]
        master = "masterkey"
        
        for orig in passwords:
            encrypted = PasswordEncryptor.encrypt(orig, master)
            recovered = PasswordEncryptor.decrypt(encrypted, master)
            assert recovered == orig, f"Failed for {orig}"

    def test_encrypt_reproducibility_with_same_key(self):
        """Decryption should always work with correct key"""
        password = "test"
        master = "master"
        
        for _ in range(5):
            encrypted = PasswordEncryptor.encrypt(password, master)
            decrypted = PasswordEncryptor.decrypt(encrypted, master)
            assert decrypted == password
