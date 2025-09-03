# Core Module

> Core utilities, configuration, and foundational classes

## 📦 Overview

The `grindoreiro.core` module provides the foundational utilities, configuration management, and common classes used throughout the Grindoreiro toolkit.

## 🔧 Configuration

### Config Class

Main configuration class for Grindoreiro operations.

```python
from grindoreiro.core import Config

# Create default configuration
config = Config()

# Access configuration values
print(config.samples_dir)  # Path('./data/samples')
print(config.output_dir)   # Path('./data/output')
print(config.dark_path)    # Path('./tools/wix/dark.exe')
```

#### Configuration Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `dark_path` | `Path` | `./tools/wix/dark.exe` | Path to WiX dark.exe |
| `data_dir` | `Path` | `./data/` | Base data directory |
| `samples_dir` | `Path` | `./data/samples/` | Input samples directory |
| `cache_dir` | `Path` | `./data/cache/` | Cache directory |
| `temp_dir` | `Path` | `./data/temp/` | Temporary files directory |
| `output_dir` | `Path` | `./data/output/` | Output results directory |
| `wix_url` | `str` | WiX download URL | WiX Toolset download URL |
| `default_user_agent` | `str` | Firefox UA | Default HTTP user agent |

#### Methods

```python
# Ensure directories exist
config = Config()  # Automatically creates directories
```

## 📝 Logging

### Setup Logging

Initialize the logging system for Grindoreiro.

```python
from grindoreiro.core import setup_logging, get_logger

# Setup logging with default configuration
setup_logging()

# Setup with custom level
setup_logging(level='DEBUG')

# Get logger for current module
logger = get_logger(__name__)
logger.info("Analysis started")
```

#### Parameters

- `level` (str): Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `log_file` (str): Path to log file (optional)
- `format` (str): Log message format (optional)

### Get Logger

Get a configured logger instance.

```python
from grindoreiro.core import get_logger

# Get logger for current module
logger = get_logger(__name__)

# Get logger with custom name
logger = get_logger('custom.module')
```

## 📄 File Handling

### FileHash Class

Represents file hash information and metadata.

```python
from grindoreiro.core import FileHash
from pathlib import Path

# Create from file
file_hash = FileHash.from_file(Path('sample.zip'))

print(file_hash.sha256)      # File SHA256 hash
print(file_hash.size)        # File size in bytes
print(file_hash.file_type)   # Detected file type
```

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | File path |
| `sha256` | `str` | SHA256 hash |
| `size` | `int` | File size in bytes |
| `modified_time` | `datetime` | Last modification time |
| `file_type` | `str` | MIME type or file type |

#### Class Methods

```python
@classmethod
def from_file(cls, file_path: Path, file_type: Optional[str] = None) -> 'FileHash':
    """Create FileHash from file path."""
```

## 🛠️ Utility Functions

### Session Management

```python
from grindoreiro.core import generate_session_id, get_session_temp_dir

# Generate unique session ID
session_id = generate_session_id()
print(session_id)  # e.g., 'session_20231201_143052_abc123'

# Get session-specific temp directory
temp_dir = get_session_temp_dir()
print(temp_dir)    # Path('./data/temp/session_...')
```

### Directory Utilities

```python
from grindoreiro.core import ensure_directory

# Ensure directory exists (create if needed)
ensure_directory(Path('./data/custom'))

# With parents
ensure_directory(Path('./deep/nested/path'), parents=True)
```

### Hash Calculation

```python
from grindoreiro.core import calculate_file_sha256

# Calculate SHA256 hash
hash_value = calculate_file_sha256(Path('sample.zip'))
print(hash_value)  # e.g., 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
```

## 🔧 Constants and Types

### Type Definitions

```python
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

# Common type aliases used in the codebase
ConfigDict = Dict[str, Any]
FileList = List[Path]
HashDict = Dict[str, str]
```

### Constants

```python
# Default buffer size for file operations
DEFAULT_BUFFER_SIZE = 8192

# Default hash algorithm
DEFAULT_HASH_ALGO = 'sha256'

# Temporary file prefix
TEMP_PREFIX = 'grindoreiro_'

# Session ID format
SESSION_FORMAT = 'session_%Y%m%d_%H%M%S_%f'
```

## 📊 Data Classes

### Config Dataclass

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """Configuration for Grindoreiro operations."""
    dark_path: Path = Path("./tools/wix/dark.exe")
    data_dir: Path = Path("./data/")
    samples_dir: Path = Path("./data/samples/")
    cache_dir: Path = Path("./data/cache/")
    temp_dir: Path = Path("./data/temp/")
    output_dir: Path = Path("./data/output/")
    wix_url: str = "https://wixtoolset.org/releases/"
    default_user_agent: str = "Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0"

    def __post_init__(self):
        """Ensure directories exist."""
        for dir_path in [self.data_dir, self.samples_dir, self.cache_dir,
                        self.temp_dir, self.output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
```

### FileHash Dataclass

```python
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Optional

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
        import hashlib
        import mimetypes

        # Calculate hash
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)

        # Get file info
        stat = file_path.stat()
        file_type = file_type or mimetypes.guess_type(file_path)[0]

        return cls(
            path=file_path,
            sha256=sha256.hexdigest(),
            size=stat.st_size,
            modified_time=datetime.fromtimestamp(stat.st_mtime),
            file_type=file_type
        )
```

## 🔄 Error Handling

### Custom Exceptions

```python
class GrindoreiroError(Exception):
    """Base exception for Grindoreiro errors."""
    pass

class ConfigError(GrindoreiroError):
    """Configuration-related errors."""
    pass

class FileOperationError(GrindoreiroError):
    """File operation errors."""
    pass
```

### Error Context

```python
from contextlib import contextmanager

@contextmanager
def error_context(operation: str):
    """Context manager for error handling with context."""
    try:
        yield
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error during {operation}: {e}")
        raise GrindoreiroError(f"{operation} failed: {e}") from e
```

## 📚 Usage Examples

### Basic Configuration

```python
from grindoreiro.core import Config, setup_logging, get_logger

# Initialize
config = Config()
setup_logging()
logger = get_logger(__name__)

# Use configuration
logger.info(f"Using samples dir: {config.samples_dir}")
logger.info(f"Using output dir: {config.output_dir}")
```

### File Processing

```python
from grindoreiro.core import FileHash, calculate_file_sha256
from pathlib import Path

# Process a file
sample_path = Path('sample.zip')
file_hash = FileHash.from_file(sample_path)

print(f"File: {file_hash.path}")
print(f"SHA256: {file_hash.sha256}")
print(f"Size: {file_hash.size} bytes")
print(f"Type: {file_hash.file_type}")

# Direct hash calculation
hash_value = calculate_file_sha256(sample_path)
print(f"Direct hash: {hash_value}")
```

### Session Management

```python
from grindoreiro.core import generate_session_id, get_session_temp_dir, ensure_directory

# Create session
session_id = generate_session_id()
temp_dir = get_session_temp_dir()

# Ensure temp directory exists
ensure_directory(temp_dir)

print(f"Session: {session_id}")
print(f"Temp dir: {temp_dir}")
```

### Error Handling

```python
from grindoreiro.core import get_logger, error_context

logger = get_logger(__name__)

try:
    with error_context("file processing"):
        # Risky operation
        process_file("sample.zip")
except Exception as e:
    logger.error(f"Processing failed: {e}")
    # Handle error appropriately
```

## 🔗 Related Modules

- **[Processor Module](processor.md)** - Main processing logic
- **[Pipeline Module](pipeline.md)** - Pipeline architecture
- **[Extractor Module](extractor.md)** - File extraction utilities
- **[Analyzer Module](analyzer.md)** - String and URL analysis

## 📋 Module Contents

```python
# Main exports
__all__ = [
    "Config",
    "FileHash",
    "setup_logging",
    "get_logger",
    "generate_session_id",
    "get_session_temp_dir",
    "ensure_directory",
    "calculate_file_sha256",
    "GrindoreiroError",
    "ConfigError",
    "FileOperationError"
]
```

---

💡 **Note**: This module provides the foundation for all other Grindoreiro components. Most functionality in Grindoreiro depends on these core utilities.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\core.md
