"""
Pattern detection tests for weak password patterns
"""

import pytest
from utils.patterns import PatternDetector


class TestPatternDetection:
    """Test pattern detection in passwords"""

    def test_detect_sequential_patterns(self):
        """Should detect sequential number patterns"""
        password = "pass123456"
        patterns = PatternDetector.detect_patterns(password)
        assert any('sequential' in p.lower() for p in patterns)

    def test_detect_date_patterns(self):
        """Should detect common date formats"""
        patterns = PatternDetector.detect_patterns("password01011990")
        assert len(patterns) > 0

    def test_detect_repeated_chars(self):
        """Should detect repeated characters"""
        patterns = PatternDetector.detect_patterns("passssssword")
        assert any('repeat' in p.lower() for p in patterns)

    def test_detect_keyboard_patterns(self):
        """Should detect keyboard walks like qwerty"""
        patterns = PatternDetector.detect_patterns("qwerty123")
        assert len(patterns) > 0

    def test_no_patterns_strong_password(self):
        """Strong password should have few patterns"""
        patterns = PatternDetector.detect_patterns("C0mpl3x!@#")
        # Should have 0 or very few patterns
        assert len(patterns) < 3

    def test_pattern_recommendations(self):
        """Should provide recommendations for detected patterns"""
        patterns = PatternDetector.detect_patterns("password123")
        recommendations = PatternDetector.get_pattern_recommendations(patterns)
        assert recommendations is not None
        assert len(recommendations) > 0

    def test_common_words_detection(self):
        """Should detect common dictionary words"""
        patterns = PatternDetector.detect_patterns("passworduser")
        assert len(patterns) > 0

    def test_empty_password_no_patterns(self):
        """Empty password should have no patterns"""
        patterns = PatternDetector.detect_patterns("")
        assert len(patterns) == 0
