"""ISO download and decoding utility."""

import argparse
import sys
from pathlib import Path

from ..iso_handler import ISODownloader
from ..extractor import FileExtractor
from ..core import setup_logging


def main():
    """Main entry point for isoabduct."""
    print("""
          @
    ISO (/^\)BDUCT!
        /(o)\ <[Gather and decode]
       /_____\\
    """)

    parser = argparse.ArgumentParser(description="Download and decode ISO files")
    parser.add_argument("URL", help="URL to download and decode")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("."),
        help="Output directory"
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        help="Use local fake ISO file instead of downloading"
    )
    parser.add_argument(
        "-u", "--user-agent",
        default="Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0",
        help="Custom user agent string"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    log_level = 10 if args.verbose else 20
    setup_logging(log_level)

    try:
        downloader = ISODownloader(args.user_agent)
        extractor = FileExtractor()

        if args.input:
            # Use local file
            iso_path = args.input
            print(f"Using local file: {iso_path}")
        else:
            # Download ISO
            iso_path = downloader.download_iso(args.URL, args.output)

        # Decode ISO
        zip_path = downloader.decode_iso(iso_path, args.output)

        # Extract ZIP
        extract_dir = args.output / "extracted"
        extractor.extract_zip(zip_path, extract_dir)

        print(f"Successfully decoded and extracted to {extract_dir}")

    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
