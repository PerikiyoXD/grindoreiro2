"""Basic tests for Grindoreiro components."""

import tempfile
import shutil
from pathlib import Path
import pytest

from grindoreiro.core import calculate_sha256, ensure_directory
from grindoreiro.analyzer import StringExtractor, URLAnalyzer


class TestCore:
    """Test core utilities."""

    def test_calculate_sha256(self):
        """Test SHA256 calculation."""
        test_data = b"Hello, World!"
        expected = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
        assert calculate_sha256(test_data) == expected

    def test_ensure_directory(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "test_subdir"
            ensure_directory(test_dir)
            assert test_dir.exists()
            assert test_dir.is_dir()


class TestStringExtractor:
    """Test string extraction functionality."""

    def test_extract_strings_from_text_file(self):
        """Test string extraction from a text file."""
        extractor = StringExtractor(min_length=4)

        # Create a test file with some strings
        test_content = b"Hello World\nThis is a test file\nWith some strings\n"
        test_content += b"Short\n"  # This is 5 characters, should be included
        test_content += b"Another longer string here\n"
        test_content += b"Hi\n"  # This is only 2 characters, should be filtered out

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(test_content)
            test_file = Path(f.name)

        try:
            strings = extractor.extract_strings(test_file)

            # Check that we extracted the expected strings
            assert "Hello World" in strings
            assert "This is a test file" in strings
            assert "With some strings" in strings
            assert "Another longer string here" in strings
            assert "Short" in strings  # 5 characters, should be included
            assert "Hi" not in strings  # Only 2 characters, should be filtered out

        finally:
            test_file.unlink()


class TestURLAnalyzer:
    """Test URL analysis functionality."""

    def test_find_urls(self):
        """Test URL extraction from strings."""
        analyzer = URLAnalyzer()

        test_strings = [
            "Check out http://example.com/page",
            "Also https://secure.example.com/path",
            "No URL here",
            "Multiple http://site1.com and https://site2.com urls"
        ]

        urls = analyzer.find_urls(test_strings)

        assert "http://example.com/page" in urls
        assert "https://secure.example.com/path" in urls
        assert "http://site1.com" in urls
        assert "https://site2.com" in urls

    def test_find_cnc_url(self):
        """Test C&C URL detection."""
        analyzer = URLAnalyzer()

        test_urls = {
            "http://malicious.com/5050/index.php",
            "https://normal.com/page",
            "http://another.com/5050/index.php"
        }

        cnc_url = analyzer.find_cnc_url(test_urls)
        assert cnc_url == "http://malicious.com/5050/index.php"

    def test_find_download_url(self):
        """Test download URL detection."""
        analyzer = URLAnalyzer()

        test_urls = {
            "http://example.com/fake.iso",
            "https://another.com/iso/download",
            "http://normal.com/page"
        }

        download_url = analyzer.find_download_url(test_urls, "iso")
        assert download_url in ["http://example.com/fake.iso", "https://another.com/iso/download"]


if __name__ == "__main__":
    # Run basic tests
    test_core = TestCore()
    test_core.test_calculate_sha256()
    test_core.test_ensure_directory()
    print("Core tests passed!")

    test_extractor = TestStringExtractor()
    test_extractor.test_extract_strings_from_text_file()
    print("String extractor tests passed!")

    test_analyzer = TestURLAnalyzer()
    test_analyzer.test_find_urls()
    test_analyzer.test_find_cnc_url()
    test_analyzer.test_find_download_url()
    print("URL analyzer tests passed!")

    print("All basic tests passed!")
