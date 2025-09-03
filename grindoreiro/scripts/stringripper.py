"""String extraction utility for binary files."""

import argparse
import sys
from pathlib import Path

from ..analyzer import StringExtractor
from ..core import setup_logging


def main():
    """Main entry point for stringripper."""
    print("| String Ripper v2.0 /w love PXD |")

    parser = argparse.ArgumentParser(description="Extract strings from binary files")
    parser.add_argument("file", help="The file to search strings from")
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (default: <input>.strings)"
    )
    parser.add_argument(
        "--min-length", "-l",
        type=int,
        default=4,
        help="Minimum string length (default: 4)"
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

    input_file = Path(args.file)
    if not input_file.exists():
        print(f"Error: File {input_file} not found")
        sys.exit(1)

    try:
        extractor = StringExtractor(min_length=args.min_length)
        strings = extractor.extract_strings(input_file, args.output)

        output_file = args.output or input_file.with_suffix(f"{input_file.suffix}.strings")
        print(f"| Done! Generated strings file: {output_file}!")
        print(f"| Extracted {len(strings)} unique strings")

    except Exception as e:
        print(f"Error extracting strings: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
