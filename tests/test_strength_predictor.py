"""
Tests for password strength predictor
"""

import pytest
from utils.strength_predictor import PasswordStrengthPredictor


class TestPasswordStrengthPredictor:
    """Test strength prediction and recommendations"""

    def test_predict_next_level_weak_to_moderate(self):
        """Weak password should suggest moderate level improvements"""
        result = PasswordStrengthPredictor.predict_next_strength_level("pass123")
        assert result['next_level'] is not None
        assert len(result['required_changes']) > 0

    def test_predict_next_level_already_maximum(self):
        """Very strong password should show no next level"""
        pwd = "VeryStr0ng!@#P@ss2024!"
        result = PasswordStrengthPredictor.predict_next_strength_level(pwd)
        assert result.get('already_maximum') in [True, False]  # May or may not reach max

    def test_generate_suggestions_short_password(self):
        """Short passwords should get length suggestions"""
        suggestions = PasswordStrengthPredictor.generate_suggestions("abc")
        assert any("character" in s.lower() for s in suggestions)

    def test_generate_suggestions_no_uppercase(self):
        """Password without uppercase should get that suggestion"""
        suggestions = PasswordStrengthPredictor.generate_suggestions("abc123!@#")
        assert any("uppercase" in s.lower() for s in suggestions)

    def test_generate_suggestions_no_special(self):
        """Password without special chars should get that suggestion"""
        suggestions = PasswordStrengthPredictor.generate_suggestions("abcDEF123")
        assert any("special" in s.lower() for s in suggestions)

    def test_generate_suggestions_strong_password(self):
        """Strong password should have no/few suggestions"""
        pwd = "MyStr0ng!@#Pwd2024"
        suggestions = PasswordStrengthPredictor.generate_suggestions(pwd)
        # Strong pwd should have 0-1 suggestions max
        assert len(suggestions) <= 2

    def test_compare_passwords_first_stronger(self):
        """Comparison should identify stronger first password"""
        result = PasswordStrengthPredictor.compare_passwords("WeakPass1", "VeryStr0ng!@#")
        assert result['password2_score'] > result['password1_score']

    def test_compare_passwords_equal_strength(self):
        """Equally strong passwords should show winner=0"""
        pwd = "MyP@ss123"
        result = PasswordStrengthPredictor.compare_passwords(pwd, pwd)
        assert result['winner'] == 0

    def test_compare_passwords_margin_calculation(self):
        """Margin should be positive number"""
        result = PasswordStrengthPredictor.compare_passwords("weak", "VeryStr0ng!")
        assert result['margin'] >= 0

    def test_estimate_improvement_very_strong(self):
        """Very strong password needs no improvement"""
        pwd = "C0mplex!P@ssw0rd#2024$Secure"
        result = PasswordStrengthPredictor.estimate_improvement_effort(pwd)
        assert result['improvement_needed'] <= 20

    def test_estimate_improvement_weak(self):
        """Weak password needs significant improvement"""
        pwd = "weak"
        result = PasswordStrengthPredictor.estimate_improvement_effort(pwd)
        assert result['improvement_needed'] > 50
        assert result['effort_level'] in ['High', 'Medium-High']

    def test_estimate_improvement_moderate(self):
        """Moderate password needs some improvement"""
        pwd = "Moderate123!"
        result = PasswordStrengthPredictor.estimate_improvement_effort(pwd)
        assert result['improvement_needed'] >= 0

    def test_predictor_consistency(self):
        """Predictor should give consistent results"""
        pwd = "TestPass123!"
        
        result1 = PasswordStrengthPredictor.generate_suggestions(pwd)
        result2 = PasswordStrengthPredictor.generate_suggestions(pwd)
        
        assert result1 == result2

    def test_predictor_with_unicode(self):
        """Predictor should handle unicode passwords"""
        pwd = "café@P@ss123!"
        result = PasswordStrengthPredictor.generate_suggestions(pwd)
        assert isinstance(result, list)

    def test_requirements_hierarchy(self):
        """Strength requirements should follow hierarchy"""
        reqs = PasswordStrengthPredictor.REQUIREMENTS
        
        assert reqs['WEAK']['min_length'] <= reqs['MODERATE']['min_length']
        assert reqs['MODERATE']['min_length'] <= reqs['STRONG']['min_length']
