"""
Edge cases and boundary tests for password analyzer strength calculations
"""

import pytest
from utils.password_analyzer import PasswordAnalyzer
from config import PASSWORD_CONFIG


class TestPasswordAnalyzerEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_entropy_with_empty_string(self):
        """Empty password should have 0 entropy"""
        entropy = PasswordAnalyzer.calculate_entropy("")
        assert entropy == 0

    def test_entropy_with_only_lowercase(self):
        """Password with only lowercase should use 26-char set"""
        entropy = PasswordAnalyzer.calculate_entropy("abcdef")
        assert entropy > 0
        # 6 chars * log2(26) ≈ 28.2
        assert 25 < entropy < 32

    def test_entropy_with_only_uppercase(self):
        """Password with only uppercase should use 26-char set"""
        entropy = PasswordAnalyzer.calculate_entropy("ABCDEF")
        assert entropy > 0

    def test_entropy_with_only_digits(self):
        """Password with only digits should use 10-char set"""
        entropy = PasswordAnalyzer.calculate_entropy("123456")
        expected = 6 * 3.32  # log2(10) ≈ 3.32
        assert 19 < entropy < 21

    def test_entropy_with_special_chars(self):
        """Password with special characters should use extended set"""
        entropy = PasswordAnalyzer.calculate_entropy("!@#$%^")
        assert entropy > 0

    def test_entropy_with_all_char_types(self):
        """Password with all char types uses largest set"""
        entropy = PasswordAnalyzer.calculate_entropy("aB1!@#")
        # 6 chars * log2(94) ≈ 48.8
        assert entropy > 40

    def test_entropy_comparison(self):
        """Longer passwords should have higher entropy"""
        entropy_short = PasswordAnalyzer.calculate_entropy("Pass1!")
        entropy_long = PasswordAnalyzer.calculate_entropy("Pass1!Pass1!")
        assert entropy_long > entropy_short

    def test_strength_very_weak(self):
        """Very weak password classification"""
        result = PasswordAnalyzer.analyze_password("123")
        assert result['strength'] == "VERY_WEAK"
        assert result['score'] < 25

    def test_strength_weak(self):
        """Weak password classification"""
        result = PasswordAnalyzer.analyze_password("password123")
        assert result['strength'] in ["WEAK", "MODERATE"]

    def test_strength_strong(self):
        """Strong password classification"""
        result = PasswordAnalyzer.analyze_password("MyStr0ng!P@ssw0rd")
        assert result['strength'] in ["STRONG", "VERY_STRONG"]
        assert result['score'] > 70

    def test_strength_very_strong(self):
        """Very strong password classification"""
        result = PasswordAnalyzer.analyze_password("C0mpl3x!P@ssw0rd#2024$Mid")
        assert result['strength'] == "VERY_STRONG"

    def test_crack_time_very_weak(self):
        """Very weak passwords should crack quickly"""
        time_str = PasswordAnalyzer.estimate_crack_time(10)
        assert "instant" in time_str.lower() or "segundo" in time_str.lower()

    def test_crack_time_weak(self):
        """Weak passwords should crack in minutes/hours"""
        time_str = PasswordAnalyzer.estimate_crack_time(30)
        assert "minute" in time_str.lower() or "minuto" in time_str.lower() or "hour" in time_str.lower()

    def test_crack_time_strong(self):
        """Strong passwords need more time"""
        time_str = PasswordAnalyzer.estimate_crack_time(80)
        assert "year" in time_str.lower() or "año" in time_str.lower()

    def test_crack_time_maximum_entropy(self):
        """Very high entropy should show very long times"""
        time_str = PasswordAnalyzer.estimate_crack_time(128)
        assert "year" in time_str.lower() or "billion" in time_str.lower()

    def test_batch_analyze_empty_list(self):
        """Batch analysis with empty list should return empty results"""
        results = PasswordAnalyzer.batch_analyze([])
        assert results == []

    def test_batch_analyze_single_password(self):
        """Batch analysis with one password"""
        results = PasswordAnalyzer.batch_analyze(["TestPass123!"])
        assert len(results) == 1
        assert 'strength' in results[0]

    def test_batch_analyze_multiple(self):
        """Batch analysis with multiple passwords"""
        passwords = ["weak", "Medium123!", "VeryStr0ng!P@ss"]
        results = PasswordAnalyzer.batch_analyze(passwords)
        assert len(results) == 3
        # Should be ordered by ascending strength
        scores = [r['score'] for r in results]
        assert scores[0] < scores[2]

    def test_batch_analyze_with_unicode(self):
        """Batch analysis should handle unicode characters"""
        passwords = ["niño123!", "Contraseña2024!", "café@Pass"]
        results = PasswordAnalyzer.batch_analyze(passwords)
        assert len(results) == 3
        assert all('strength' in r for r in results)

    def test_analyze_with_spaces(self):
        """Password with spaces should be analyzed"""
        result = PasswordAnalyzer.analyze_password("My Pass 123!")
        assert result is not None
        assert 'strength' in result

    def test_analyze_very_long_password(self):
        """Very long password should not crash"""
        long_pass = "a" * 256 + "B1!"
        result = PasswordAnalyzer.analyze_password(long_pass)
        assert result['strength'] == "VERY_STRONG"

    def test_analyze_with_null_bytes(self):
        """Password analysis should handle edge case inputs safely"""
        # This should not crash
        try:
            result = PasswordAnalyzer.analyze_password("\x00null")
            assert result is not None
        except (ValueError, TypeError):
            # Acceptable to reject null bytes
            pass

    def test_entropy_precision(self):
        """Entropy should be rounded to 2 decimal places"""
        entropy = PasswordAnalyzer.calculate_entropy("test123!")
        # Check it's a float with max 2 decimals
        assert isinstance(entropy, float)
        decimal_places = len(str(entropy).split('.')[-1])
        assert decimal_places <= 2

    def test_score_always_0_to_100(self):
        """Strength score should always be between 0 and 100"""
        passwords = ["a", "abc123", "ComplexP@ss!", "x" * 100]
        for pwd in passwords:
            result = PasswordAnalyzer.analyze_password(pwd)
            assert 0 <= result['score'] <= 100
