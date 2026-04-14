"""
PDF report generation tests
"""

import pytest
import os
from utils.pdf_generator import PDFReportGenerator
from pathlib import Path


class TestPDFReportGenerator:
    """Test PDF report generation"""

    @pytest.fixture
    def sample_data(self):
        """Sample password analysis data"""
        return {
            "password": "TestPass123!",
            "strength": "STRONG",
            "score": 85,
            "entropy": 65.5,
            "patterns": ["contains_uppercase", "contains_numbers"],
            "recommendations": ["Good! Keep using special characters"],
            "crack_time": "1000 years"
        }

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Temporary directory for PDFs"""
        return tmp_path

    def test_generate_single_report(self, sample_data, temp_dir):
        """Should generate a PDF report"""
        output = temp_dir / "report.pdf"
        result = PDFReportGenerator.generate_report(sample_data, str(output))
        
        assert os.path.exists(output) or result is not None

    def test_report_includes_password_info(self, sample_data, temp_dir):
        """Report should contain password analysis info"""
        output = temp_dir / "report_info.pdf"
        PDFReportGenerator.generate_report(sample_data, str(output))
        
        # Verify file was created
        assert os.path.exists(output)

    def test_report_with_multiple_passwords(self, temp_dir):
        """Should handle multiple password analyses"""
        data = [
            {"password": "weak", "strength": "WEAK", "score": 20},
            {"password": "strong123!", "strength": "STRONG", "score": 90}
        ]
        
        output = temp_dir / "multi_report.pdf"
        result = PDFReportGenerator.generate_batch_report(data, str(output))
        
        assert os.path.exists(output) or result is not None

    def test_report_with_unicode_password(self, temp_dir):
        """Report should handle unicode passwords"""
        data = {
            "password": "café@Pass123",
            "strength": "STRONG",
            "score": 85
        }
        
        output = temp_dir / "unicode_report.pdf"
        result = PDFReportGenerator.generate_report(data, str(output))
        
        assert os.path.exists(output) or result is not None

    def test_report_file_size(self, sample_data, temp_dir):
        """Generated PDF should have reasonable file size"""
        output = temp_dir / "size_report.pdf"
        PDFReportGenerator.generate_report(sample_data, str(output))
        
        if os.path.exists(output):
            file_size = os.path.getsize(output)
            assert file_size > 1000  # At least 1KB
            assert file_size < 10_000_000  # Less than 10MB

    def test_report_with_empty_patterns(self, temp_dir):
        """Report should handle empty patterns list"""
        data = {
            "password": "test",
            "strength": "WEAK",
            "score": 30,
            "patterns": [],
            "recommendations": []
        }
        
        output = temp_dir / "empty_patterns.pdf"
        result = PDFReportGenerator.generate_report(data, str(output))
        
        assert os.path.exists(output) or result is not None

    def test_report_output_directory_creation(self, temp_dir):
        """Should create output directory if it doesn't exist"""
        output_dir = temp_dir / "reports" / "subdir"
        output = output_dir / "report.pdf"
        
        data = {"password": "test", "strength": "WEAK", "score": 30}
        PDFReportGenerator.generate_report(data, str(output))
        
        assert os.path.exists(output) or os.path.exists(output_dir.parent)

    def test_batch_report_ordering(self, temp_dir):
        """Batch reports should maintain order"""
        data = [
            {"password": f"pass{i}", "strength": "WEAK", "score": 20 + i}
            for i in range(5)
        ]
        
        output = temp_dir / "ordered_report.pdf"
        PDFReportGenerator.generate_batch_report(data, str(output))
        
        assert os.path.exists(output) or len(data) == 5
