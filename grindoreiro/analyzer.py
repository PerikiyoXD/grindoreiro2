"""String extraction and analysis utilities."""

import re
from pathlib import Path
from typing import List, Set, Optional
import logging

from .core import get_logger


logger = get_logger(__name__)


class StringExtractor:
    """Extracts and analyzes strings from binary files."""

    def __init__(self, min_length: int = 4):
        """Initialize string extractor with minimum string length."""
        self.min_length = min_length
        self.logger = logger

        # Character sets for string matching
        self.ascii_chars = br"A-Za-z0-9+/=\-:. ,_$%'()[\]<> "
        self.unicode_chars = r"A-Za-z0-9+/=\-:. ,_$%'()[\]<> "

        # Compile regex patterns
        self.ascii_pattern = re.compile(
            b'[%s]{%d,}' % (self.ascii_chars, self.min_length)
        )
        self.unicode_pattern = re.compile(
            '[%s]{%d,}' % (self.unicode_chars, self.min_length)
        )

    def extract_strings(self, file_path: Path, output_path: Optional[Path] = None) -> List[str]:
        """Extract strings from binary file and optionally save to file."""
        if output_path is None:
            output_path = file_path.with_suffix(f"{file_path.suffix}.strings")

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            strings = []

            # Extract ASCII strings
            for match in self.ascii_pattern.findall(data):
                try:
                    string = match.decode('ascii', errors='ignore').strip()
                    if string:
                        strings.append(string)
                except UnicodeDecodeError:
                    continue

            # Extract UTF-16 strings
            try:
                utf16_data = data.decode('utf-16', errors='ignore')
                for match in self.unicode_pattern.findall(utf16_data):
                    if match.strip():
                        strings.append(match.strip())
            except UnicodeDecodeError:
                self.logger.warning(f"Could not decode UTF-16 from {file_path}")

            # Remove duplicates while preserving order
            unique_strings = list(dict.fromkeys(strings))

            # Save to file
            with open(output_path, "w", encoding='utf-8') as f:
                for string in unique_strings:
                    f.write(f"{string}\n")

            self.logger.info(f"Extracted {len(unique_strings)} strings to {output_path}")
            return unique_strings

        except Exception as e:
            self.logger.error(f"Failed to extract strings from {file_path}: {e}")
            raise


class URLAnalyzer:
    """Analyzes strings for URLs and patterns."""

    def __init__(self):
        """Initialize URL analyzer."""
        self.logger = logger

        # Regex patterns for different URL types
        self.http_pattern = re.compile(r'http://[^\s]+')
        self.https_pattern = re.compile(r'https://[^\s]+')

    def find_urls(self, strings: List[str]) -> Set[str]:
        """Find all URLs in list of strings."""
        urls = set()

        for string in strings:
            # Find HTTP URLs
            http_matches = self.http_pattern.findall(string)
            urls.update(http_matches)

            # Find HTTPS URLs
            https_matches = self.https_pattern.findall(string)
            urls.update(https_matches)

        self.logger.info(f"Found {len(urls)} URLs")
        return urls

    def find_cnc_url(self, urls: Set[str]) -> Optional[str]:
        """Find C&C URL based on known patterns."""
        for url in urls:
            if "5050/index.php" in url:
                self.logger.info(f"Found C&C URL: {url}")
                return url
        return None

    def find_download_url(self, urls: Set[str], pattern: str = "iso") -> Optional[str]:
        """Find download URL based on pattern."""
        for url in urls:
            if pattern.lower() in url.lower():
                self.logger.info(f"Found download URL: {url}")
                return url
        return None
