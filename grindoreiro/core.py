"""Core utilities and configuration for Grindoreiro."""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import hashlib
import uuid
from datetime import datetime


@dataclass
class Config:
    """Configuration for Grindoreiro operations."""

    # Tool paths
    dark_path: Path = Path("./tools/wix/dark.exe")

    # Data directories
    data_dir: Path = Path("./data/")
    samples_dir: Path = Path("./data/samples/")
    cache_dir: Path = Path("./data/cache/")
    temp_dir: Path = Path("./data/temp/")
    output_dir: Path = Path("./data/output/")

    # External resources
    wix_url: str = "https://wixtoolset.org/releases/"
    default_user_agent: str = "Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0"

    def __post_init__(self):
        """Ensure directories exist."""
        for dir_path in [self.data_dir, self.samples_dir, self.cache_dir,
                        self.temp_dir, self.output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


@dataclass
class FileHash:
    """File hash information."""
    path: Path
    sha256: str
    size: int
    modified_time: Optional[datetime] = None
    file_type: Optional[str] = None

    @classmethod
    def from_file(cls, file_path: Path, file_type: Optional[str] = None) -> 'FileHash':
        """Create FileHash from file path."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        stat = file_path.stat()
        with open(file_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()

        modified_time = datetime.fromtimestamp(stat.st_mtime)

        return cls(
            path=file_path,
            sha256=sha256,
            size=stat.st_size,
            modified_time=modified_time,
            file_type=file_type
        )


# Global configuration instance
config = Config()


def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('grindoreiro.log')
        ]
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(f"grindoreiro.{name}")


def ensure_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger = get_logger(__name__)
        logger.warning(f"Could not create directory {path}: {e}")


def calculate_sha256(data: bytes) -> str:
    """Calculate SHA256 hash of bytes."""
    return hashlib.sha256(data).hexdigest()


def calculate_file_sha256(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def generate_session_id() -> str:
    """Generate a unique session ID for analysis."""
    return f"session_{uuid.uuid4().hex[:16]}"


def get_session_temp_dir(session_id: str) -> Path:
    """Get temporary directory for a session."""
    temp_dir = config.temp_dir / session_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Create a session manifest file for easy navigation
    manifest_file = temp_dir / "session_manifest.txt"
    if not manifest_file.exists():
        with open(manifest_file, "w", encoding="utf-8") as f:
            f.write(f"Session ID: {session_id}\n")
            f.write(f"Created: {datetime.now().isoformat()}\n")
            f.write(f"Temp Directory: {temp_dir}\n\n")
            f.write("Directory Structure:\n")
            f.write("- processing/          # Main processing directory\n")
            f.write("  - extract/          # ZIP extraction results\n")
            f.write("  - msi_output/       # MSI extraction results\n")
            f.write("  - msi_script/       # MSI script files\n")
            f.write("  - dll/              # DLL files\n")
            f.write("  - iso/              # ISO files\n")
            f.write("  - exe/              # Executable files\n")
            f.write("- session_manifest.txt # This file\n")

    return temp_dir


def cleanup_session_temp_dir(session_id: str, force: bool = False) -> None:
    """Clean up temporary directory for a session."""
    logger = get_logger(__name__)
    temp_dir = config.temp_dir / session_id
    if temp_dir.exists():
        try:
            # Update manifest with cleanup time
            manifest_file = temp_dir / "session_manifest.txt"
            if manifest_file.exists():
                with open(manifest_file, "a", encoding="utf-8") as f:
                    f.write(f"\nCleaned up: {datetime.now().isoformat()}\n")

            if not force:
                # Don't cleanup if there are any .debug files (indicating manual analysis)
                debug_files = list(temp_dir.rglob("*.debug"))
                if debug_files:
                    logger.info(f"Skipping cleanup of session {session_id} due to debug files: {[str(f) for f in debug_files]}")
                    return

            import shutil
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            logger.warning(f"Could not cleanup temp directory {temp_dir}: {e}")


def create_session_debug_marker(session_id: str, reason: str = "Manual analysis in progress") -> Path:
    """Create a debug marker file to prevent automatic cleanup."""
    temp_dir = config.temp_dir / session_id
    debug_file = temp_dir / ".debug"
    with open(debug_file, "w", encoding="utf-8") as f:
        f.write(f"Debug marker created: {datetime.now().isoformat()}\n")
        f.write(f"Reason: {reason}\n")
        f.write("Delete this file to allow automatic cleanup\n")
    return debug_file


def list_active_sessions() -> List[Dict[str, Any]]:
    """List all active sessions with their temp directories."""
    sessions = []
    if config.temp_dir.exists():
        for session_dir in config.temp_dir.iterdir():
            if session_dir.is_dir() and session_dir.name.startswith("session_"):
                manifest_file = session_dir / "session_manifest.txt"
                session_info = {
                    "session_id": session_dir.name,
                    "path": session_dir,
                    "exists": True,
                    "has_debug_marker": (session_dir / ".debug").exists(),
                    "created": None,
                    "size_mb": None
                }

                if manifest_file.exists():
                    try:
                        with open(manifest_file, "r", encoding="utf-8") as f:
                            content = f.read()
                            for line in content.split('\n'):
                                if line.startswith("Created:"):
                                    session_info["created"] = line.split(": ", 1)[1]
                    except:
                        pass

                # Calculate directory size
                try:
                    total_size = sum(f.stat().st_size for f in session_dir.rglob('*') if f.is_file())
                    session_info["size_mb"] = total_size / (1024 * 1024)
                except:
                    pass

                sessions.append(session_info)

    return sorted(sessions, key=lambda x: x.get("created") or "", reverse=True)


def get_cache_path(url: str) -> Path:
    """Get cache path for a URL."""
    # Create a safe filename from URL
    import re
    safe_name = re.sub(r'[^\w\-_\.]', '_', url)
    if len(safe_name) > 100:
        safe_name = safe_name[:100]
    return config.cache_dir / safe_name
