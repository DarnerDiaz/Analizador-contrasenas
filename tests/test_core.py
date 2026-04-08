"""Core functionality tests for the Password Strength Analyzer."""

import pytest
from utils.encryption import PasswordEncryptor
from utils.password_analyzer import PasswordAnalyzer
from utils.patterns import PatternDetector


class TestEncryption:
    """Test encryption and decryption functions."""
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encryption and decryption work together."""
        password = "MySecurePassword123!"
        master_password = "master_password_for_testing"
        
        encrypted = PasswordEncryptor.encrypt(password, master_password)
        decrypted = PasswordEncryptor.decrypt(encrypted, master_password)
        
        assert decrypted == password
    
    def test_encrypt_different_outputs(self):
        """Test that encrypting same data produces different outputs."""
        password = "SamePassword"
        master_password = "master_password_for_testing"
        
        encrypted1 = PasswordEncryptor.encrypt(password, master_password)
        encrypted2 = PasswordEncryptor.encrypt(password, master_password)
        
        # Different IVs should produce different ciphertexts
        assert encrypted1 != encrypted2
        # But both should decrypt to same value
        assert PasswordEncryptor.decrypt(encrypted1, master_password) == PasswordEncryptor.decrypt(encrypted2, master_password)
    
    def test_derive_key(self):
        """Test key derivation."""
        password = "test"
        salt = b"salt" * 8  # 32 bytes
        
        key = PasswordEncryptor.derive_key(password, salt)
        assert isinstance(key, bytes)
        assert len(key) == 32


class TestPasswordAnalyzer:
    """Test password analysis functionality."""
    
    def test_analyze_weak_password(self):
        """Test analysis of weak password."""
        result = PasswordAnalyzer.analyze_password("123456")
        
        assert "strength" in result
        assert "score" in result
        assert result["score"] < 40
    
    def test_analyze_strong_password(self):
        """Test analysis of strong password."""
        result = PasswordAnalyzer.analyze_password("MyStr0ng!P@ssw0rd#2024")
        
        assert "strength" in result
        assert "score" in result
        assert result["score"] > 60
    
    def test_calculate_entropy(self):
        """Test entropy calculation."""
        entropy = PasswordAnalyzer.calculate_entropy("password")
        assert isinstance(entropy, float)
        assert entropy > 0
    
    def test_estimate_crack_time(self):
        """Test crack time estimation."""
        time_str = PasswordAnalyzer.estimate_crack_time(50)
        assert isinstance(time_str, str)
        assert len(time_str) > 0
    
    def test_analyze_characters(self):
        """Test character analysis."""
        result = PasswordAnalyzer.analyze_characters("Aa1!")
        assert isinstance(result, dict)
        assert all(isinstance(v, bool) for v in result.values())


class TestPatternDetection:
    """Test pattern detection functionality."""
    
    def test_detect_sequential_pattern(self):
        """Test detection of sequential patterns."""
        result = PatternDetector.detect_patterns("12345678")
        assert isinstance(result, dict)
    
    def test_detect_repeated_pattern(self):
        """Test detection of repeated characters."""
        result = PatternDetector.detect_patterns("aaaaaaa")
        assert isinstance(result, dict)
    
    def test_no_patterns_detected(self):
        """Test password with complex patterns."""
        result = PatternDetector.detect_patterns("Xq9@mK2$pL")
        assert isinstance(result, dict)


class TestIntegration:
    """Integration tests for common workflows."""
    
    def test_full_analysis_workflow(self):
        """Test complete password analysis workflow."""
        password = "TestPassword123!"
        
        # Analyze
        analysis = PasswordAnalyzer.analyze_password(password)
        assert "strength" in analysis
        assert "score" in analysis
        
        # Detect patterns
        patterns = PatternDetector.detect_patterns(password)
        assert isinstance(patterns, dict)
    
    def test_encryption_with_analyzed_password(self):
        """Test encrypting an analyzed password."""
        password = "SecurePass123!"
        master_password = "master_password_for_testing"
        
        # Analyze first
        analysis = PasswordAnalyzer.analyze_password(password)
        assert analysis["score"] > 0
        
        # Then encrypt
        encrypted = PasswordEncryptor.encrypt(password, master_password)
        decrypted = PasswordEncryptor.decrypt(encrypted, master_password)
        
        assert decrypted == password
    
    def test_batch_analysis(self):
        """Test batch password analysis."""
        passwords = ["weak", "Medium123", "Str0ng!P@ssw0rd#2024"]
        results = PasswordAnalyzer.batch_analyze(passwords)
        
        assert len(results) == 3
        assert all("score" in r for r in results)
        assert all("strength" in r for r in results)
