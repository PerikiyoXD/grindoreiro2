"""ISO download and decoding utilities."""

import base64
import requests
from pathlib import Path
from typing import Optional
import logging
import sys

from .core import get_logger


logger = get_logger(__name__)


class ISODownloader:
    """Handles downloading and decoding of ISO files."""

    def __init__(self, user_agent: Optional[str] = None):
        """Initialize ISO downloader."""
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0"
        self.logger = logger

    def download_with_user_agent(self, url: str) -> requests.Response:
        """Download URL with custom user agent."""
        headers = {"User-Agent": self.user_agent}

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            self.logger.error("Request timed out")
            raise
        except requests.exceptions.TooManyRedirects:
            self.logger.error("Too many redirects")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise

    def download_iso(self, url: str, output_dir: Path) -> Path:
        """Download ISO file from URL."""
        self.logger.info(f"Downloading ISO from {url}")

        try:
            response = self.download_with_user_agent(url)
            filename = url.rsplit('/', 1)[-1]
            output_path = output_dir / filename

            with open(output_path, "w", encoding='utf-8') as f:
                f.write(response.text)

            self.logger.info(f"Saved ISO to {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Failed to download ISO: {e}")
            raise

    def decode_iso(self, iso_path: Path, output_dir: Path) -> Path:
        """Decode ISO file (base64 encoded ZIP)."""
        self.logger.info(f"Decoding ISO {iso_path}")

        try:
            with open(iso_path, "r", encoding='utf-8') as f:
                data = f.read()

            # First base64 decode
            self.logger.debug("First base64 decode")
            decoded1 = base64.b64decode(data)

            encoded_path = output_dir / "encoded.b64"
            with open(encoded_path, "wb") as f:
                f.write(decoded1)

            # Second base64 decode
            self.logger.debug("Second base64 decode")
            decoded2 = base64.b64decode(decoded1)

            zip_path = output_dir / "decoded.zip"
            with open(zip_path, "wb") as f:
                f.write(decoded2)

            self.logger.info(f"Decoded ZIP saved to {zip_path}")
            return zip_path

        except Exception as e:
            self.logger.error(f"Failed to decode ISO {iso_path}: {e}")
            raise
