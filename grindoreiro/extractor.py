"""File extraction utilities for ZIP and MSI files."""

import zipfile
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional
import logging

from .core import get_logger, ensure_directory


logger = get_logger(__name__)


class FileExtractor:
    """Handles extraction of various file formats."""

    def __init__(self, dark_path: Optional[Path] = None):
        """Initialize extractor with WiX dark.exe path."""
        self.dark_path = dark_path
        self.logger = logger

    def extract_zip(self, zip_path: Path, output_dir: Path) -> None:
        """Extract ZIP file to output directory."""
        ensure_directory(output_dir)

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            self.logger.info(f"Extracted ZIP {zip_path} to {output_dir}")
        except Exception as e:
            self.logger.error(f"Failed to extract ZIP {zip_path}: {e}")
            raise

    def extract_msi(self, msi_path: Path, extract_dir: Path, script_dir: Path) -> None:
        """Extract MSI file using WiX dark.exe."""
        if not self.dark_path or not self.dark_path.exists():
            raise FileNotFoundError(f"dark.exe not found at {self.dark_path}")

        # Ensure directories exist with better error handling
        try:
            extract_dir.mkdir(parents=True, exist_ok=True)
            script_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directories: {extract_dir}, {script_dir}")
        except Exception as e:
            self.logger.error(f"Failed to create directories: {e}")
            raise

        # Verify directories are writable
        try:
            test_file_extract = extract_dir / ".test_write"
            test_file_extract.write_text("test")
            test_file_extract.unlink()

            test_file_script = script_dir / ".test_write"
            test_file_script.write_text("test")
            test_file_script.unlink()
            self.logger.info("Directory write permissions verified")
        except Exception as e:
            self.logger.error(f"Directory write permission check failed: {e}")
            raise

        try:
            # Use absolute paths to avoid working directory issues
            abs_msi_path = msi_path.resolve()
            abs_extract_dir = extract_dir.resolve()
            abs_script_dir = script_dir.resolve()
            abs_dark_path = self.dark_path.resolve()

            # Try with script directory first, but if it fails, try without it
            # Try with script file instead of script directory
            script_file = script_dir / "installer_script.wxs"
            cmd = [
                str(abs_dark_path),
                str(abs_msi_path),
                "-x", str(abs_extract_dir),
                "-o", str(script_file)
            ]

            self.logger.info(f"Running command: {' '.join(cmd)}")
            self.logger.info(f"Working directory: {Path.cwd()}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(Path.cwd()),  # Explicitly set working directory
                check=False  # Don't raise exception on non-zero exit
            )

            # Log all output for debugging
            if result.stdout:
                self.logger.info(f"Dark stdout: {result.stdout}")
            if result.stderr:
                self.logger.warning(f"Dark stderr: {result.stderr}")

            # If script extraction fails, try without script output
            if result.returncode != 0 and ("Acceso denegado" in str(result.stderr) or "Access denied" in str(result.stderr) or "denied" in str(result.stderr).lower()):
                self.logger.warning("Script extraction failed, retrying without script output")
                cmd_no_script = [
                    str(abs_dark_path),
                    str(abs_msi_path),
                    "-x", str(abs_extract_dir)
                ]

                self.logger.info(f"Retrying with command: {' '.join(cmd_no_script)}")
                result = subprocess.run(
                    cmd_no_script,
                    capture_output=True,
                    text=True,
                    cwd=str(Path.cwd()),
                    check=False
                )

                if result.stdout:
                    self.logger.info(f"Dark stdout (retry): {result.stdout}")
                if result.stderr:
                    self.logger.warning(f"Dark stderr (retry): {result.stderr}")

            if result.returncode != 0:
                self.logger.error(f"Dark.exe failed with exit code: {result.returncode}")
                # Check if files were actually extracted despite warnings/errors
                extracted_files = list(abs_extract_dir.glob("*"))
                if extracted_files and result.returncode == 283:
                    self.logger.info(f"Files were extracted despite warnings: {[f.name for f in extracted_files[:5]]}")
                    # Don't raise exception for exit code 283 if files were extracted
                elif result.returncode not in [283]:  # 283 seems to be warnings about patches
                    raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

            self.logger.info(f"Extracted MSI {msi_path}")

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to extract MSI {msi_path}: {e}")
            self.logger.error(f"Command: {e.cmd}")
            self.logger.error(f"Return code: {e.returncode}")
            if e.stdout:
                self.logger.error(f"Stdout: {e.stdout}")
            if e.stderr:
                self.logger.error(f"Stderr: {e.stderr}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error extracting MSI {msi_path}: {e}")
            raise

    def find_files_by_extension(self, directory: Path, extension: str) -> List[Path]:
        """Find all files with given extension in directory recursively."""
        return list(directory.rglob(f"*.{extension}"))

    def find_msi_file(self, directory: Path) -> Optional[Path]:
        """Find the first MSI file in directory."""
        msi_files = self.find_files_by_extension(directory, "msi")
        return msi_files[0] if msi_files else None

    def find_dll_files(self, directory: Path, exclude_patterns: Optional[List[str]] = None) -> List[Path]:
        """Find only the malicious DLL(s) referenced by CustomAction with DllEntry in the WXS script."""
        dll_files = []

        # Parse WXS script for CustomAction with BinaryKey and DllEntry
        script_dir = directory.parent / "msi_script"
        wxs_files = list(script_dir.glob("*.wxs")) if script_dir.exists() else []

        malicious_binary_keys = set()
        for wxs_file in wxs_files:
            try:
                with open(wxs_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                import re
                # Only CustomActions with BinaryKey and DllEntry="VIPS0033939" (malicious entry point)
                custom_actions = re.findall(r'<CustomAction[^>]*BinaryKey="([^"]+)"[^>]*DllEntry="VIPS0033939"', content, re.IGNORECASE)
                for binary_key in custom_actions:
                    if binary_key and binary_key.lower() not in ['aicustact.dll']:
                        malicious_binary_keys.add(binary_key)
            except Exception as e:
                self.logger.warning(f"Error parsing WXS file {wxs_file}: {e}")

        # Only return files matching those BinaryKeys
        for binary_key in malicious_binary_keys:
            binary_path = directory / "Binary" / binary_key
            if binary_path.exists():
                dll_files.append(binary_path)
                self.logger.info(f"Selected malicious DLL from WXS script: {binary_path}")

        # Optionally, fallback to .dll extension if nothing found (for legacy samples)
        if not dll_files:
            dll_files.extend(self.find_files_by_extension(directory, "dll"))

        if exclude_patterns:
            filtered = []
            for dll in dll_files:
                if not any(pattern.lower() in dll.name.lower() for pattern in exclude_patterns):
                    filtered.append(dll)
            return filtered

        return dll_files

    def copy_file(self, source: Path, destination: Path) -> None:
        """Copy file from source to destination."""
        try:
            shutil.copy2(source, destination)
            self.logger.info(f"Copied {source} to {destination}")
        except Exception as e:
            self.logger.error(f"Failed to copy {source} to {destination}: {e}")
            raise
