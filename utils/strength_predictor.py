"""
Advanced password strength prediction and suggestions
"""

from typing import Dict, List
from utils.password_analyzer import PasswordAnalyzer


class PasswordStrengthPredictor:
    """Predicts password strength and provides personalized recommendations"""

    # Character requirements for different strengths
    REQUIREMENTS = {
        "VERY_WEAK": {
            "min_length": 6,
            "lowercase": False,
            "uppercase": False,
            "digits": False,
            "special": False
        },
        "WEAK": {
            "min_length": 8,
            "lowercase": True,
            "uppercase": False,
            "digits": True,
            "special": False
        },
        "MODERATE": {
            "min_length": 10,
            "lowercase": True,
            "uppercase": True,
            "digits": True,
            "special": False
        },
        "STRONG": {
            "min_length": 12,
            "lowercase": True,
            "uppercase": True,
            "digits": True,
            "special": True
        },
        "VERY_STRONG": {
            "min_length": 14,
            "lowercase": True,
            "uppercase": True,
            "digits": True,
            "special": True
        }
    }

    @staticmethod
    def predict_next_strength_level(password: str) -> Dict:
        """
        Predicts what's needed to reach the next strength level
        
        Args:
            password: Current password
            
        Returns:
            Dict with current level, next level, and required changes
        """
        analysis = PasswordAnalyzer.analyze_password(password)
        current_strength = analysis['strength']
        
        # Map strength to next level
        strength_order = ["VERY_WEAK", "WEAK", "MODERATE", "STRONG", "VERY_STRONG"]
        current_idx = strength_order.index(current_strength)
        
        if current_idx == len(strength_order) - 1:
            return {
                "current_level": current_strength,
                "next_level": None,
                "already_maximum": True
            }
        
        next_strength = strength_order[current_idx + 1]
        current_reqs = PasswordStrengthPredictor.REQUIREMENTS[current_strength]
        next_reqs = PasswordStrengthPredictor.REQUIREMENTS[next_strength]
        
        needed_changes = []
        
        if len(password) < next_reqs["min_length"]:
            needed_changes.append(
                f"Increase length to at least {next_reqs['min_length']} characters"
            )
        
        if next_reqs["special"] and not current_reqs["special"]:
            if not any(not c.isalnum() for c in password):
                needed_changes.append("Add at least one special character (!@#$%^&*)")
        
        return {
            "current_level": current_strength,
            "next_level": next_strength,
            "required_changes": needed_changes,
            "current_score": analysis['score']
        }

    @staticmethod
    def generate_suggestions(password: str) -> List[str]:
        """
        Generate specific improvement suggestions
        
        Args:
            password: Password to analyze
            
        Returns:
            List of specific suggestions for improvement
        """
        suggestions = []
        analysis = PasswordAnalyzer.analyze_password(password)
        
        if len(password) < 12:
            suggestions.append(f"Add more characters ({12 - len(password)} more needed for strong)")
        
        if not any(c.isupper() for c in password):
            suggestions.append("Include uppercase letters (A-Z)")
        
        if not any(c.isdigit() for c in password):
            suggestions.append("Include numbers (0-9)")
        
        if not any(not c.isalnum() for c in password):
            suggestions.append("Include special characters (!@#$)")
        
        if len(set(password)) < len(password) / 2:
            suggestions.append("Use more diverse characters (reduce repetition)")
        
        return suggestions or ["Password is strong! No improvements needed."]

    @staticmethod
    def compare_passwords(password1: str, password2: str) -> Dict:
        """
        Compare two passwords and recommend the stronger one
        
        Args:
            password1: First password
            password2: Second password
            
        Returns:
            Comparison results with recommendation
        """
        analysis1 = PasswordAnalyzer.analyze_password(password1)
        analysis2 = PasswordAnalyzer.analyze_password(password2)
        
        if analysis1['score'] > analysis2['score']:
            winner = 1
            margin = analysis1['score'] - analysis2['score']
        elif analysis2['score'] > analysis1['score']:
            winner = 2
            margin = analysis2['score'] - analysis1['score']
        else:
            winner = 0
            margin = 0
        
        return {
            "password1_score": analysis1['score'],
            "password1_strength": analysis1['strength'],
            "password2_score": analysis2['score'],
            "password2_strength": analysis2['strength'],
            "winner": winner,
            "margin": margin
        }

    @staticmethod
    def estimate_improvement_effort(password: str) -> Dict:
        """
        Estimate how much improvement is needed for next level
        
        Args:
            password: Current password
            
        Returns:
            Difficulty assessment
        """
        analysis = PasswordAnalyzer.analyze_password(password)
        score = analysis['score']
        strength = analysis['strength']
        
        if strength == "VERY_STRONG":
            improvement_needed = 0
            effort = "None"
        elif score >= 80:
            improvement_needed = 100 - score
            effort = "Low"
        elif score >= 60:
            improvement_needed = 100 - score
            effort = "Medium"
        elif score >= 40:
            improvement_needed = 100 - score
            effort = "Medium-High"
        else:
            improvement_needed = 100 - score
            effort = "High"
        
        return {
            "current_score": score,
            "improvement_needed": improvement_needed,
            "effort_level": effort,
            "target_score": 100
        }
