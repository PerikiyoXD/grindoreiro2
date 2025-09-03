# Configuration

> Customizing Grindoreiro behavior and settings

## 🎯 Overview

Grindoreiro uses sensible defaults but can be extensively customized through configuration files, environment variables, and command-line options.

## ⚙️ Configuration Sources

Configuration is loaded from multiple sources (in order of precedence):

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration file** (`grindoreiro.ini` or `config.json`)
4. **Default values** (lowest priority)

## 📁 Directory Configuration

### Default Structure

```
grindoreiro/
├── data/
│   ├── samples/          # Input samples
│   ├── cache/           # Cached downloads
│   ├── temp/            # Temporary files
│   └── output/          # Analysis results
├── tools/
│   └── wix/            # WiX Toolset
│       └── dark.exe
└── grindoreiro.ini     # Configuration file
```

### Custom Directories

```bash
# Command-line override
python -m grindoreiro.cli sample.zip \
  --samples-dir ./my-samples \
  --output-dir ./my-results \
  --cache-dir ./my-cache

# Environment variables
export GRINDOREIRO_SAMPLES_DIR=./my-samples
export GRINDOREIRO_OUTPUT_DIR=./my-results
export GRINDOREIRO_CACHE_DIR=./my-cache
```

## 🔧 Core Configuration

### WiX Toolset Path

**Purpose**: Location of WiX decompiler for MSI files

```bash
# Default
./tools/wix/dark.exe

# Custom path
python -m grindoreiro.cli sample.zip --dark-path /opt/wix/dark.exe

# Environment
export GRINDOREIRO_DARK_PATH=/opt/wix/dark.exe
```

### User Agent

**Purpose**: HTTP user agent for ISO downloads

```bash
# Default
Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0

# Custom
export GRINDOREIRO_USER_AGENT="Custom Agent/1.0"
```

## 📄 Configuration File

### INI Format

Create `grindoreiro.ini`:

```ini
[paths]
samples_dir = ./data/samples
output_dir = ./data/output
cache_dir = ./data/cache
temp_dir = ./data/temp
dark_path = ./tools/wix/dark.exe

[network]
user_agent = Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0
timeout = 30
max_retries = 3

[processing]
max_workers = 4
keep_temp = false
verbose = false

[logging]
level = INFO
file = grindoreiro.log
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### JSON Format

Create `config.json`:

```json
{
  "paths": {
    "samples_dir": "./data/samples",
    "output_dir": "./data/output",
    "cache_dir": "./data/cache",
    "temp_dir": "./data/temp",
    "dark_path": "./tools/wix/dark.exe"
  },
  "network": {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0",
    "timeout": 30,
    "max_retries": 3
  },
  "processing": {
    "max_workers": 4,
    "keep_temp": false,
    "verbose": false
  },
  "logging": {
    "level": "INFO",
    "file": "grindoreiro.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

## 🌐 Network Configuration

### Proxy Settings

```bash
# HTTP proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# No proxy for local
export NO_PROXY=localhost,127.0.0.1,.local
```

### Timeout Settings

```python
# In configuration file
[network]
timeout = 60
max_retries = 5
retry_delay = 2
```

### SSL Configuration

```python
# Custom SSL certificates
export REQUESTS_CA_BUNDLE=/path/to/ca-bundle.crt

# Disable SSL verification (not recommended)
export GRINDOREIRO_SSL_VERIFY=false
```

## 📊 Processing Configuration

### Parallel Processing

```ini
[processing]
max_workers = 2          # Limit concurrent processes
worker_timeout = 300     # Process timeout in seconds
memory_limit = 1024      # Memory limit per process (MB)
```

### Resource Management

```ini
[processing]
temp_cleanup = true      # Auto-clean temp files
cache_cleanup = 7        # Cache cleanup after days
disk_space_check = true  # Check available disk space
min_disk_space = 1024    # Minimum disk space (MB)
```

### Analysis Options

```ini
[analysis]
string_min_length = 4    # Minimum string length
url_extract = true       # Extract URLs
file_hash = true         # Calculate file hashes
metadata_extract = true  # Extract metadata
```

## 📝 Logging Configuration

### Log Levels

```ini
[logging]
level = DEBUG            # DEBUG, INFO, WARNING, ERROR, CRITICAL
file = grindoreiro.log   # Log file path
max_size = 10485760      # Max log size (10MB)
backup_count = 5         # Number of backup files
```

### Log Format

```ini
[logging]
format = %(asctime)s [%(levelname)s] %(name)s: %(message)s
date_format = %Y-%m-%d %H:%M:%S
```

### Multiple Handlers

```python
# Advanced logging configuration
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'grindoreiro.log',
            'formatter': 'detailed'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    }
}
```

## 🔧 Advanced Configuration

### Custom Pipeline Steps

```python
# config.py
from grindoreiro.pipeline import PipelineStep

class CustomStep(PipelineStep):
    def __init__(self):
        super().__init__("custom")

    def execute(self, context):
        # Custom processing logic
        pass

# Register custom step
PIPELINE_STEPS = [
    'grindoreiro.pipeline_steps.InitializeStep',
    'my_package.CustomStep',
    # ... other steps
]
```

### Plugin System

```python
# plugins/__init__.py
PLUGINS = [
    'plugins.custom_analyzer',
    'plugins.enhanced_reporting',
]

# plugins/custom_analyzer.py
from grindoreiro.analyzer import Analyzer

class CustomAnalyzer(Analyzer):
    def analyze(self, data):
        # Custom analysis logic
        return results
```

## 🐳 Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install WiX Toolset
RUN mkdir -p /opt/wix && \
    wget -O /tmp/wix.zip https://wixtoolset.org/downloads/v3.11.2.4516/wix311-binaries.zip && \
    unzip /tmp/wix.zip -d /opt/wix && \
    rm /tmp/wix.zip

# Set environment
ENV GRINDOREIRO_DARK_PATH=/opt/wix/dark.exe
ENV GRINDOREIRO_SAMPLES_DIR=/data/samples
ENV GRINDOREIRO_OUTPUT_DIR=/data/output

# Copy application
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Create directories
RUN mkdir -p /data/samples /data/output /data/cache /data/temp

VOLUME ["/data"]
CMD ["python", "-m", "grindoreiro.cli"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  grindoreiro:
    build: .
    volumes:
      - ./data:/data
      - ./config:/app/config
    environment:
      - GRINDOREIRO_VERBOSE=true
      - GRINDOREIRO_MAX_WORKERS=2
    command: python batch_analyze_all.py
```

## 🔒 Security Configuration

### File Permissions

```bash
# Secure configuration file
chmod 600 grindoreiro.ini

# Secure sensitive directories
chmod 700 data/cache
chmod 700 data/temp
```

### Credential Management

```python
# Secure credential storage
import keyring

# Store sensitive data
keyring.set_password("grindoreiro", "api_key", "your-api-key")

# Retrieve in code
api_key = keyring.get_password("grindoreiro", "api_key")
```

## 📊 Monitoring Configuration

### Health Checks

```python
# health_check.py
def check_system_health():
    checks = {
        'disk_space': check_disk_space(),
        'memory': check_memory(),
        'network': check_network(),
        'dependencies': check_dependencies()
    }
    return all(checks.values())
```

### Metrics Collection

```python
# metrics.py
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        # Log or store metrics
        return result
    return wrapper
```

## 🧪 Testing Configuration

### Test Configuration

```ini
[testing]
mock_network = true
test_data_dir = ./test/data
cleanup_after_test = true
parallel_tests = true
```

### CI/CD Configuration

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest
```

## 📚 Configuration Examples

### Development Setup

```ini
[paths]
samples_dir = ./dev/samples
output_dir = ./dev/output
cache_dir = ./dev/cache

[logging]
level = DEBUG
file = dev.log

[processing]
keep_temp = true
verbose = true
```

### Production Setup

```ini
[paths]
samples_dir = /var/grindoreiro/samples
output_dir = /var/grindoreiro/output
cache_dir = /var/grindoreiro/cache

[logging]
level = WARNING
file = /var/log/grindoreiro.log

[processing]
max_workers = 8
keep_temp = false
```

### Cloud Setup

```ini
[paths]
samples_dir = s3://bucket/samples
output_dir = s3://bucket/output
cache_dir = /tmp/grindoreiro-cache

[network]
timeout = 120
max_retries = 10

[processing]
max_workers = 16
```

## 🔧 Configuration Validation

### Schema Validation

```python
# config_schema.py
import jsonschema

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "paths": {
            "type": "object",
            "properties": {
                "samples_dir": {"type": "string"},
                "output_dir": {"type": "string"},
                # ... more properties
            }
        }
    }
}

def validate_config(config):
    jsonschema.validate(config, CONFIG_SCHEMA)
```

### Runtime Validation

```python
# config_validator.py
def validate_paths(config):
    """Validate that configured paths exist and are accessible."""
    from pathlib import Path

    paths_to_check = [
        config.get('samples_dir'),
        config.get('output_dir'),
        config.get('cache_dir')
    ]

    for path_str in paths_to_check:
        if path_str:
            path = Path(path_str)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            if not path.is_dir():
                raise ValueError(f"Path is not a directory: {path}")
```

## 📚 Related Topics

- [Basic Usage](basic-usage.md) - Using configured settings
- [Batch Processing](batch-processing.md) - Batch configuration
- [Troubleshooting](troubleshooting.md) - Configuration issues
- [Core Module](../api-reference/core.md) - Configuration API

---

💡 **Pro Tip**: Use environment variables for sensitive configuration and configuration files for complex settings.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\user-guides\configuration.md
