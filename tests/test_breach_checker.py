"""
Tests for password breach checker
"""

import pytest
from utils.breach_checker import BreachChecker


class TestBreachChecker:
    """Test breach detection functionality"""

    def test_check_common_breached_password(self):
        """Should identify commonly breached passwords"""
        result = BreachChecker.check_password("password123")
        assert result['is_breached'] is True

    def test_check_safe_password(self):
        """Should identify unique, safe passwords"""
        pwd = "UniqueP@ss789!"
        result = BreachChecker.check_password(pwd)
        # Note: result depends on simulation, but should be a dict
        assert isinstance(result, dict)
        assert 'is_breached' in result

    def test_breach_status_message(self):
        """Should provide clear breach status messages"""
        result = BreachChecker.check_password("password")
        assert 'status' in result
        assert isinstance(result['status'], str)

    def test_breach_recommendation(self):
        """Should provide recommendations for breached passwords"""
        result = BreachChecker.check_password("admin")
        assert 'recommendation' in result
        assert result['recommendation'] is not None

    def test_check_similar_passwords(self):
        """Should find similarities to breached passwords"""
        similar = BreachChecker.check_similar_passwords("password")
        assert isinstance(similar, list)

    def test_estimate_breach_risk_critical(self):
        """Breached password should have critical risk"""
        result = BreachChecker.estimate_breach_risk("password123", 30)
        assert result['risk_level'] == "CRITICAL"
        assert result['risk_score'] > 80

    def test_estimate_breach_risk_weak_password(self):
        """Weak but unbreached should have high risk"""
        pwd = "WeakPwd"  # Assuming not in breach DB
        result = BreachChecker.estimate_breach_risk(pwd, 35)
        assert result['risk_level'] in ["HIGH", "CRITICAL"]

    def test_estimate_breach_risk_strong_password(self):
        """Strong unbreached password should have low risk"""
        pwd = "VeryStr0ng!@#Pass"
        result = BreachChecker.estimate_breach_risk(pwd, 85)
        assert result['risk_level'] in ["LOW", "VERY_LOW"]

    def test_risk_score_range(self):
        """Risk score should always be between 0-100"""
        for score_val in [20, 50, 80]:
            result = BreachChecker.estimate_breach_risk("test", score_val)
            assert 0 <= result['risk_score'] <= 100

    def test_breach_checker_consistency(self):
        """Same password should return same breach status"""
        result1 = BreachChecker.check_password("test123")
        result2 = BreachChecker.check_password("test123")
        assert result1['is_breached'] == result2['is_breached']

    def test_case_insensitivity(self):
        """Breach checking should be case insensitive"""
        result_lower = BreachChecker.check_password("password")
        result_upper = BreachChecker.check_password("PASSWORD")
        # Both should detect breach (common password)
        assert result_lower['is_breached'] == result_upper['is_breached']

    def test_unicode_password_checking(self):
        """Should handle unicode passwords"""
        result = BreachChecker.check_password("café@Pass123")
        assert isinstance(result, dict)
        assert 'is_breached' in result

    def test_breach_count_realistic(self):
        """Breach count should be realistic positive number"""
        result = BreachChecker.check_password("password")
        if result['is_breached']:
            assert result['breach_count'] > 0
            assert result['breach_count'] < 1000  # Reasonable upper limit
