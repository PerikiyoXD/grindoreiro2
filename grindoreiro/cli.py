"""Command-line interface for Grindoreiro."""

import argparse
import sys
from pathlib import Path

from .core import setup_logging, config
from .processor import GrandoreiroProcessor


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Grindoreiro - Malware Analysis Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m grindoreiro sample.zip
  python -m grindoreiro --dark-path /path/to/dark.exe sample.zip
  python -m grindoreiro --verbose sample.zip
        """
    )

    parser.add_argument(
        "sample",
        help="Path to Grandoreiro sample ZIP file"
    )

    parser.add_argument(
        "--dark-path",
        type=Path,
        help="Path to WiX dark.exe (default: ./tools/wix/dark.exe)"
    )

    parser.add_argument(
        "--samples-dir",
        type=Path,
        help=f"Samples directory (default: {config.samples_dir})"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        help=f"Output directory (default: {config.output_dir})"
    )

    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary files after analysis for manual inspection"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--list-sessions",
        action="store_true",
        help="List all active analysis sessions"
    )

    return parser


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    log_level = 10 if args.verbose else 20  # DEBUG or INFO
    setup_logging(log_level)

    # Handle list-sessions command
    if args.list_sessions:
        from .core import list_active_sessions
        sessions = list_active_sessions()

        if not sessions:
            print("No active sessions found.")
            return

        print("Active Analysis Sessions:")
        print("=" * 80)
        for session in sessions:
            status = "DEBUG" if session["has_debug_marker"] else "ACTIVE"
            size_str = f"{session['size_mb']:.1f}MB" if session['size_mb'] else "Unknown"
            created_str = session['created'] or "Unknown"
            print(f"Session: {session['session_id']}")
            print(f"  Path: {session['path']}")
            print(f"  Status: {status}")
            print(f"  Size: {size_str}")
            print(f"  Created: {created_str}")
            print()

        return

    # Update configuration if provided
    if args.samples_dir:
        config.samples_dir = args.samples_dir
    if args.output_dir:
        config.output_dir = args.output_dir

    # Check if dark.exe exists
    dark_path = args.dark_path or config.dark_path
    if not dark_path.exists():
        print(f"Error: dark.exe not found at {dark_path}")
        print("Please download WiX Toolset from: https://wixtoolset.org/releases/")
        sys.exit(1)

    # Process sample
    try:
        processor = GrandoreiroProcessor(dark_path)
        processor.process_sample(args.sample, keep_temp=args.keep_temp)
    except Exception as e:
        print(f"Error processing sample: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
