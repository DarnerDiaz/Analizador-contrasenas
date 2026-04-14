"""
Comprehensive error handling and validation for password operations
"""

from typing import Dict, Optional, Tuple
from enum import Enum


class PasswordErrorCode(Enum):
    """Error codes for password operations"""
    INVALID_INPUT = "INVALID_INPUT"
    EMPTY_PASSWORD = "EMPTY_PASSWORD"
    INVALID_LENGTH = "INVALID_LENGTH"
    ENCRYPTION_FAILED = "ENCRYPTION_FAILED"
    DECRYPTION_FAILED = "DECRYPTION_FAILED"
    INVALID_MASTER_KEY = "INVALID_MASTER_KEY"
    GENERATION_FAILED = "GENERATION_FAILED"
    INVALID_CONFIG = "INVALID_CONFIG"


class PasswordException(Exception):
    """Base exception for password operations"""
    def __init__(self, code: PasswordErrorCode, message: str, details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(f"[{code.value}] {message}")


class ValidationHandler:
    """Centralized validation and error handling"""

    # Validation constraints
    MIN_PASSWORD_LENGTH = 1
    MAX_PASSWORD_LENGTH = 256
    MIN_MASTER_KEY_LENGTH = 1
    MAX_MASTER_KEY_LENGTH = 1000

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password input
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(password, str):
            return False, f"Password must be string, got {type(password).__name__}"
        
        if len(password) == 0:
            return False, "Password cannot be empty"
        
        if len(password) > ValidationHandler.MAX_PASSWORD_LENGTH:
            return False, f"Password exceeds maximum length of {ValidationHandler.MAX_PASSWORD_LENGTH}"
        
        return True, None

    @staticmethod
    def validate_master_key(master_key: str) -> Tuple[bool, Optional[str]]:
        """Validate master key for encryption"""
        if not isinstance(master_key, str):
            return False, f"Master key must be string, got {type(master_key).__name__}"
        
        if len(master_key) < ValidationHandler.MIN_MASTER_KEY_LENGTH:
            return False, f"Master key is too short (minimum {ValidationHandler.MIN_MASTER_KEY_LENGTH} chars)"
        
        if len(master_key) > ValidationHandler.MAX_MASTER_KEY_LENGTH:
            return False, f"Master key exceeds maximum length"
        
        return True, None

    @staticmethod
    def validate_batch_input(passwords: list) -> Tuple[bool, Optional[str]]:
        """Validate batch password input"""
        if not isinstance(passwords, (list, tuple)):
            return False, f"Input must be list or tuple, got {type(passwords).__name__}"
        
        for i, pwd in enumerate(passwords):
            valid, error = ValidationHandler.validate_password(pwd)
            if not valid:
                return False, f"Password at index {i} is invalid: {error}"
        
        return True, None

    @staticmethod
    def safe_operation(operation_func, *args, **kwargs) -> Dict:
        """
        Execute operation with comprehensive error handling
        
        Args:
            operation_func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Result dict with status and data/error info
        """
        try:
            result = operation_func(*args, **kwargs)
            return {
                "success": True,
                "data": result,
                "error": None
            }
        except PasswordException as e:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": e.code.value,
                    "message": e.message,
                    "details": e.details
                }
            }
        except (ValueError, TypeError) as e:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": PasswordErrorCode.INVALID_INPUT.value,
                    "message": str(e),
                    "details": {}
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "UNKNOWN_ERROR",
                    "message": f"Unexpected error: {str(e)}",
                    "details": {"exception_type": type(e).__name__}
                }
            }

    @staticmethod
    def retry_operation(operation_func, max_retries: int = 3, *args, **kwargs) -> Dict:
        """
        Retry operation with exponential backoff
        
        Args:
            operation_func: Function to retry
            max_retries: Maximum retry attempts
            
        Returns:
            Result of operation
        """
        import time
        
        last_error = None
        
        for attempt in range(max_retries):
            result = ValidationHandler.safe_operation(operation_func, *args, **kwargs)
            
            if result['success']:
                return result
            
            last_error = result['error']
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
        
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "RETRY_EXHAUSTED",
                "message": f"Operation failed after {max_retries} attempts",
                "details": {"last_error": last_error}
            }
        }
