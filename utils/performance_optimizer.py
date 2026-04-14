"""
Performance optimizations and caching for password analysis
"""

from functools import lru_cache
import time
from typing import Dict


class PerformanceOptimizer:
    """Optimization utilities for password analysis"""

    # Cache for frequently checked passwords
    _analysis_cache = {}
    _cache_max_size = 1000

    @staticmethod
    @lru_cache(maxsize=512)
    def optimized_entropy_calculation(password: str) -> float:
        """
        Cached entropy calculation for frequently analyzed passwords
        
        Args:
            password: Password to analyze
            
        Returns:
            Cached or newly calculated entropy
        """
        import math
        
        char_set_size = 0
        if any(c.islower() for c in password):
            char_set_size += 26
        if any(c.isupper() for c in password):
            char_set_size += 26
        if any(c.isdigit() for c in password):
            char_set_size += 10
        if any(not c.isalnum() for c in password):
            char_set_size += 32
        
        if char_set_size == 0:
            return 0.0
        
        entropy = len(password) * math.log2(char_set_size)
        return round(entropy, 2)

    @staticmethod
    def clear_cache():
        """Clear analysis cache"""
        PerformanceOptimizer._analysis_cache.clear()
        PerformanceOptimizer.optimized_entropy_calculation.cache_clear()

    @staticmethod
    def get_cache_stats() -> Dict:
        """Get cache statistics"""
        cache_info = PerformanceOptimizer.optimized_entropy_calculation.cache_info()
        return {
            "cache_size": len(PerformanceOptimizer._analysis_cache),
            "hits": cache_info.hits,
            "misses": cache_info.misses,
            "hit_ratio": cache_info.hits / (cache_info.hits + cache_info.misses) if (cache_info.hits + cache_info.misses) > 0 else 0
        }

    @staticmethod
    def batch_analyze_optimized(passwords: list, use_cache: bool = True) -> list:
        """
        Optimized batch analysis with caching
        
        Args:
            passwords: List of passwords
            use_cache: Whether to use caching
            
        Returns:
            Analysis results
        """
        results = []
        
        for pwd in passwords:
            if use_cache and pwd in PerformanceOptimizer._analysis_cache:
                results.append(PerformanceOptimizer._analysis_cache[pwd])
            else:
                entropy = PerformanceOptimizer.optimized_entropy_calculation(pwd)
                result = {"password": pwd, "entropy": entropy}
                
                if use_cache:
                    if len(PerformanceOptimizer._analysis_cache) >= PerformanceOptimizer._cache_max_size:
                        # Simple FIFO eviction
                        to_remove = list(PerformanceOptimizer._analysis_cache.keys())[0]
                        del PerformanceOptimizer._analysis_cache[to_remove]
                    
                    PerformanceOptimizer._analysis_cache[pwd] = result
                
                results.append(result)
        
        return results

    @staticmethod
    def time_analysis(passwords: list, operation_func) -> Dict:
        """
        Time analysis operations for performance benchmarking
        
        Args:
            passwords: Passwords to analyze
            operation_func: Function to time
            
        Returns:
            Timing results
        """
        start = time.perf_counter()
        results = operation_func(passwords)
        end = time.perf_counter()
        
        return {
            "total_time_ms": (end - start) * 1000,
            "passwords_count": len(passwords),
            "avg_time_per_password_ms": ((end - start) * 1000) / len(passwords) if passwords else 0,
            "results": results
        }
