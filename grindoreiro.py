#!/usr/bin/env python3
"""Legacy entry point for Grindoreiro - redirects to new CLI."""

import sys
import os
from pathlib import Path

# Add current directory to path to import grindoreiro package
sys.path.insert(0, str(Path(__file__).parent))

from grindoreiro.cli import main

if __name__ == "__main__":
    print("""
   _____      _           _                _
  / ____|    (_)         | |              (_)
 | |  __ _ __ _ _ __   __| | ___  _ __ ___ _ _ __ ___
 | | |_ | '__| | '_ \ / _` |/ _ \| '__/ _ \ | '__/ _ \
 | |__| | |  | | | | | (_| | (_) | | |  __/ | | | (_) |
  \_____|_|  |_|_| |_|\__,_|\___/|_|  \___|_|_|  \___/
                              \Grinding grandoreiro!\
    """)

    # Check if dark.exe exists
    dark_path = Path("./tools/wix/dark.exe")
    if not dark_path.exists():
        print(f"Error: dark.exe wasn't found at '{dark_path}'.")
        print("Please download WiX Toolset from: https://wixtoolset.org/releases/")
        print("Extract wix311-binaries.zip and place dark.exe in ./tools/wix/")
        sys.exit(1)

    # Run the new CLI
    main()
    
    
