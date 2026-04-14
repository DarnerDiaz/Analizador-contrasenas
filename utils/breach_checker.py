"""
Password breach database validator and checker
"""

from typing import Dict, List
import hashlib


class BreachChecker:
    """Check if password has been exposed in known breaches (HIBP-like)"""

    # Simulated breach database (in production, would query HIBP API)
    COMMON_BREACHES = {
        "password", "123456", "password123", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "sunshine",
        "princess", "qwerty", "abc123", "123123", "111111"
    }

    @staticmethod
    def check_password(password: str) -> Dict:
        """
        Check if password exists in breach database
        
        Args:
            password: Password to check
            
        Returns:
            Dict with breach status and count (simulated)
        """
        pwd_lower = password.lower()
        
        if pwd_lower in BreachChecker.COMMON_BREACHES:
            return {
                "is_breached": True,
                "breach_count": 15,
                "status": "CRITICAL - Password in multiple breaches",
                "recommendation": "DO NOT USE this password"
            }
        
        # Simulate checking by hash
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()[:8]
        
        # Simple simulation: passwords with certain hash patterns are "breached"
        if pwd_hash.startswith('a'):
            return {
                "is_breached": True,
                "breach_count": 3,
                "status": "WARNING - Password found in 3 breaches",
                "recommendation": "Consider using a different password"
            }
        
        return {
            "is_breached": False,
            "breach_count": 0,
            "status": "OK - Password not in breach databases",
            "recommendation": "This password appears safe to use"
        }

    @staticmethod
    def check_similar_passwords(password: str) -> List[Dict]:
        """
        Check for similar passwords that might be breached
        
        Args:
            password: Base password
            
        Returns:
            List of similar passwords found in breaches
        """
        similar = []
        
        # Check common variations
        variations = [
            password.lower(),
            password.upper(),
            password + "123",
            password + "2024",
            password + "!",
        ]
        
        for var in variations:
            if var.lower() in BreachChecker.COMMON_BREACHES:
                similar.append({
                    "password": var,
                    "risk": "HIGH",
                    "found_in_breach": True
                })
        
        return similar

    @staticmethod
    def estimate_breach_risk(password: str, score: float) -> Dict:
        """
        Estimate overall breach risk based on strength and appearance
        
        Args:
            password: Password to analyze
            score: Password strength score (0-100)
            
        Returns:
            Risk assessment
        """
        breach_info = BreachChecker.check_password(password)
        
        if breach_info['is_breached']:
            risk_level = "CRITICAL"
            risk_score = 95
        elif score < 40:
            risk_level = "HIGH"
            risk_score = 75
        elif score < 60:
            risk_level = "MEDIUM"
            risk_score = 45
        elif score < 80:
            risk_level = "LOW"
            risk_score = 25
        else:
            risk_level = "VERY_LOW"
            risk_score = 10
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "breach_status": breach_info['status'],
            "recommendation": breach_info['recommendation']
        }
