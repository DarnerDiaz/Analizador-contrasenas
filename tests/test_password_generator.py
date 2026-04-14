"""
Tests for password generator module
"""

import pytest
from utils.password_generator import PasswordGenerator


class TestPasswordGenerator:
    """Test password generation"""

    def test_generate_basic_password(self):
        """Should generate a random password"""
        pwd = PasswordGenerator.generate_password()
        assert isinstance(pwd, str)
        assert len(pwd) > 0

    def test_generate_custom_length(self):
        """Should respect custom length"""
        for length in [8, 12, 16, 24]:
            pwd = PasswordGenerator.generate_password(length=length)
            assert len(pwd) == length

    def test_generate_with_all_char_types(self):
        """Generated password should contain all character types when enabled"""
        pwd = PasswordGenerator.generate_password(
            length=20,
            use_lowercase=True,
            use_uppercase=True,
            use_digits=True,
            use_special=True
        )
        assert any(c.islower() for c in pwd)
        assert any(c.isupper() for c in pwd)
        assert any(c.isdigit() for c in pwd)

    def test_generate_lowercase_only(self):
        """Should generate lowercase only when specified"""
        pwd = PasswordGenerator.generate_password(
            use_lowercase=True,
            use_uppercase=False,
            use_digits=False,
            use_special=False
        )
        assert pwd.islower()

    def test_generate_uppercase_only(self):
        """Should generate uppercase only when specified"""
        pwd = PasswordGenerator.generate_password(
            use_lowercase=False,
            use_uppercase=True,
            use_digits=False,
            use_special=False
        )
        assert pwd.isupper()

    def test_generate_with_exclusions(self):
        """Should exclude specified characters"""
        excluded = "aeiou"
        pwd = PasswordGenerator.generate_password(
            length=20,
            use_lowercase=True,
            exclude_chars=excluded
        )
        for char in excluded:
            assert char not in pwd

    def test_generate_randomness(self):
        """Each generated password should be different"""
        pwd1 = PasswordGenerator.generate_password()
        pwd2 = PasswordGenerator.generate_password()
        pwd3 = PasswordGenerator.generate_password()
        
        assert pwd1 != pwd2
        assert pwd2 != pwd3

    def test_generate_passphrase(self):
        """Should generate readable passphrase"""
        phrase = PasswordGenerator.generate_passphrase()
        assert isinstance(phrase, str)
        assert "-" in phrase  # Default separator

    def test_generate_passphrase_custom_separator(self):
        """Should respect custom separator"""
        phrase = PasswordGenerator.generate_passphrase(separator="_")
        assert "_" in phrase

    def test_generate_passphrase_custom_length(self):
        """Should generate specified word count"""
        phrase = PasswordGenerator.generate_passphrase(word_count=5)
        words = phrase.lower().split("-")
        assert len(words) == 5

    def test_generate_passphrase_lowercase(self):
        """Should generate lowercase when not capitalized"""
        phrase = PasswordGenerator.generate_passphrase(capitalize=False)
        # First char after separator should be lowercase
        words = phrase.split("-")
        for word in words:
            assert word[0].islower()

    def test_generate_batch(self):
        """Should generate multiple passwords"""
        batch = PasswordGenerator.generate_batch(count=5)
        assert len(batch) == 5
        assert all(isinstance(p, str) for p in batch)

    def test_generate_batch_all_different(self):
        """Batch passwords should all be different"""
        batch = PasswordGenerator.generate_batch(count=10)
        assert len(set(batch)) == 10  # No duplicates

    def test_suggest_password_weak(self):
        """Should suggest weak password (short, no special chars)"""
        suggestion = PasswordGenerator.suggest_password_for_strength("WEAK")
        assert suggestion['target_strength'] == "WEAK"
        assert len(suggestion['password']) == 8

    def test_suggest_password_strong(self):
        """Should suggest strong password (long, with special chars)"""
        suggestion = PasswordGenerator.suggest_password_for_strength("STRONG")
        assert suggestion['target_strength'] == "STRONG"
        assert len(suggestion['password']) >= 12

    def test_suggest_password_includes_passphrase(self):
        """Suggestions should include alternative passphrase"""
        suggestion = PasswordGenerator.suggest_password_for_strength("STRONG")
        assert 'passphrase' in suggestion
        assert isinstance(suggestion['passphrase'], str)

    def test_invalid_char_types_raises_error(self):
        """Should raise error if no character types selected"""
        with pytest.raises(ValueError):
            PasswordGenerator.generate_password(
                use_lowercase=False,
                use_uppercase=False,
                use_digits=False,
                use_special=False
            )

    def test_password_consistency(self):
        """Multiple calls should produce valid passwords"""
        for _ in range(10):
            pwd = PasswordGenerator.generate_password()
            assert isinstance(pwd, str)
            assert len(pwd) > 0
