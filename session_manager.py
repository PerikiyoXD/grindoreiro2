#!/usr/bin/env python3
"""Session management utilities for Grindoreiro."""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

from grindoreiro.core import list_active_sessions, cleanup_session_temp_dir, create_session_debug_marker, config, get_logger


def list_sessions_command() -> None:
    """List all active sessions."""
    sessions = list_active_sessions()

    if not sessions:
        print("No active sessions found.")
        return

    print("Active Analysis Sessions:")
    print("=" * 80)
    for session in sessions:
        status = "🔒 DEBUG" if session["has_debug_marker"] else "🟢 ACTIVE"
        size_str = f"{session['size_mb']:.1f}MB" if session['size_mb'] else "Unknown"
        created_str = session['created'] or "Unknown"
        print(f"Session: {session['session_id']}")
        print(f"  📁 Path: {session['path']}")
        print(f"  📊 Status: {status}")
        print(f"  💾 Size: {size_str}")
        print(f"  🕒 Created: {created_str}")
        print()


def cleanup_sessions_command(session_ids: List[str] = None, force: bool = False) -> None:
    """Clean up session temp directories."""
    if session_ids:
        # Clean specific sessions
        for session_id in session_ids:
            print(f"Cleaning up session: {session_id}")
            cleanup_session_temp_dir(session_id, force=force)
    else:
        # Clean all sessions without debug markers
        sessions = list_active_sessions()
        cleaned_count = 0

        for session in sessions:
            if not session["has_debug_marker"] or force:
                print(f"Cleaning up session: {session['session_id']}")
                cleanup_session_temp_dir(session["session_id"], force=force)
                cleaned_count += 1
            else:
                print(f"Skipping session {session['session_id']} (has debug marker)")

        print(f"\nCleaned up {cleaned_count} sessions")


def debug_session_command(session_id: str, reason: str = None) -> None:
    """Create debug marker for a session."""
    try:
        debug_file = create_session_debug_marker(session_id, reason or "Manual analysis requested")
        print(f"Debug marker created: {debug_file}")
        print("Session will not be automatically cleaned up.")
        print("Delete the .debug file to allow automatic cleanup.")
    except Exception as e:
        print(f"Error creating debug marker: {e}")
        sys.exit(1)


def inspect_session_command(session_id: str) -> None:
    """Inspect a specific session directory."""
    temp_dir = config.temp_dir / session_id

    if not temp_dir.exists():
        print(f"Session directory not found: {temp_dir}")
        sys.exit(1)

    print(f"Session: {session_id}")
    print(f"Path: {temp_dir}")
    print()

    # Read manifest if available
    manifest_file = temp_dir / "session_manifest.txt"
    if manifest_file.exists():
        print("Session Manifest:")
        print("-" * 40)
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading manifest: {e}")
        print()

    # List directory contents
    print("Directory Contents:")
    print("-" * 40)

    def print_tree(path: Path, prefix: str = ""):
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "

                if item.is_dir():
                    print(f"{prefix}{connector}📁 {item.name}/")
                    if item.name.startswith('.'):
                        continue  # Skip hidden directories
                    extension = "    " if is_last else "│   "
                    print_tree(item, prefix + extension)
                else:
                    size = item.stat().st_size
                    size_str = f"({size:,} bytes)" if size > 0 else ""
                    print(f"{prefix}{connector}📄 {item.name} {size_str}")
        except PermissionError:
            print(f"{prefix}└── [Permission denied]")

    print_tree(temp_dir)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Grindoreiro Session Management Utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python session_manager.py list
  python session_manager.py cleanup
  python session_manager.py cleanup --force
  python session_manager.py cleanup session_abc123 session_def456
  python session_manager.py debug session_abc123 "Investigating false positive"
  python session_manager.py inspect session_abc123
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List command
    subparsers.add_parser('list', help='List all active sessions')

    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up session temp directories')
    cleanup_parser.add_argument('--force', action='store_true', help='Force cleanup even with debug markers')
    cleanup_parser.add_argument('sessions', nargs='*', help='Specific session IDs to clean (default: all)')

    # Debug command
    debug_parser = subparsers.add_parser('debug', help='Create debug marker for session')
    debug_parser.add_argument('session_id', help='Session ID')
    debug_parser.add_argument('reason', nargs='?', help='Reason for debugging')

    # Inspect command
    inspect_parser = subparsers.add_parser('inspect', help='Inspect session directory')
    inspect_parser.add_argument('session_id', help='Session ID to inspect')

    return parser


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'list':
        list_sessions_command()
    elif args.command == 'cleanup':
        cleanup_sessions_command(args.sessions if hasattr(args, 'sessions') else None, args.force if hasattr(args, 'force') else False)
    elif args.command == 'debug':
        debug_session_command(args.session_id, args.reason if hasattr(args, 'reason') else None)
    elif args.command == 'inspect':
        inspect_session_command(args.session_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
