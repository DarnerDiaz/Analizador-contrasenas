"""
Secure password generation and suggestion
"""

import random
import string
from typing import Dict, List


class PasswordGenerator:
    """Generate secure, randomized passwords"""

    # Character sets
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    @staticmethod
    def generate_password(
        length: int = 14,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        exclude_chars: str = ""
    ) -> str:
        """
        Generate a random secure password
        
        Args:
            length: Password length
            use_lowercase: Include lowercase letters
            use_uppercase: Include uppercase letters
            use_digits: Include digits
            use_special: Include special characters
            exclude_chars: Characters to exclude
            
        Returns:
            Generated password
        """
        available_chars = ""
        
        if use_lowercase:
            available_chars += PasswordGenerator.LOWERCASE
        if use_uppercase:
            available_chars += PasswordGenerator.UPPERCASE
        if use_digits:
            available_chars += PasswordGenerator.DIGITS
        if use_special:
            available_chars += PasswordGenerator.SPECIAL
        
        # Remove excluded characters
        for char in exclude_chars:
            available_chars = available_chars.replace(char, "")
        
        if not available_chars:
            raise ValueError("No character types selected for password generation")
        
        # Ensure at least one char from each enabled type
        password_chars = []
        
        if use_lowercase:
            password_chars.append(random.choice(PasswordGenerator.LOWERCASE))
        if use_uppercase:
            password_chars.append(random.choice(PasswordGenerator.UPPERCASE))
        if use_digits:
            password_chars.append(random.choice(PasswordGenerator.DIGITS))
        if use_special:
            password_chars.append(random.choice(PasswordGenerator.SPECIAL))
        
        # Fill remaining length with random characters
        for _ in range(length - len(password_chars)):
            password_chars.append(random.choice(available_chars))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password_chars)
        
        return ''.join(password_chars)

    @staticmethod
    def generate_passphrase(
        word_count: int = 4,
        separator: str = "-",
        capitalize: bool = True
    ) -> str:
        """
        Generate memorable passphrase
        
        Args:
            word_count: Number of words
            separator: Separator between words
            capitalize: Capitalize each word
            
        Returns:
            Generated passphrase
        """
        common_words = [
            "apple", "banana", "cherry", "dragon", "eagle", "forest",
            "guitar", "house", "island", "jungle", "kitchen", "laptop",
            "mountain", "notebook", "ocean", "palace", "quantum", "river",
            "sunset", "thunder", "umbrella", "valley", "window", "yellow",
            "zebra", "anchor", "beacon", "castle", "danger", "energy"
        ]
        
        words = [random.choice(common_words) for _ in range(word_count)]
        
        if capitalize:
            words = [w.capitalize() for w in words]
        
        return separator.join(words)

    @staticmethod
    def generate_batch(
        count: int = 5,
        length: int = 14,
        **kwargs
    ) -> List[str]:
        """
        Generate multiple passwords
        
        Args:
            count: Number of passwords to generate
            length: Password length
            **kwargs: Other parameters for generate_password
            
        Returns:
            List of generated passwords
        """
        return [
            PasswordGenerator.generate_password(length, **kwargs)
            for _ in range(count)
        ]

    @staticmethod
    def suggest_password_for_strength(target_strength: str) -> Dict:
        """
        Suggest password based on target strength level
        
        Args:
            target_strength: Target strength level
            
        Returns:
            Generated password with metadata
        """
        strength_configs = {
            "WEAK": {"length": 8, "use_special": False},
            "MODERATE": {"length": 10, "use_special": False},
            "STRONG": {"length": 12, "use_special": True},
            "VERY_STRONG": {"length": 16, "use_special": True}
        }
        
        config = strength_configs.get(target_strength, strength_configs["STRONG"])
        
        return {
            "password": PasswordGenerator.generate_password(**config),
            "target_strength": target_strength,
            "config": config,
            "passphrase": PasswordGenerator.generate_passphrase()
        }
