# CLI Module

> Command-line interface for Grindoreiro

## 📦 Overview

The `grindoreiro.cli` module provides the command-line interface for the Grindoreiro malware analysis toolkit. It handles argument parsing, configuration, and orchestrates the analysis process.

## 🔧 Main Functions

### create_parser

Create and configure the argument parser.

```python
from grindoreiro.cli import create_parser

parser = create_parser()
args = parser.parse_args()
```

**Returns:**
- `argparse.ArgumentParser`: Configured argument parser

**Arguments:**
- `--dark-path`: Path to WiX dark.exe
- `--samples-dir`: Custom samples directory
- `--output-dir`: Custom output directory
- `--keep-temp`: Keep temporary files
- `--verbose`: Enable verbose logging
- `--list-sessions`: List active analysis sessions

### main

Main entry point for the CLI application.

```python
from grindoreiro.cli import main

# Run CLI
main()
```

**Process:**
1. Parse command-line arguments
2. Setup logging based on verbosity
3. Handle special commands (list-sessions)
4. Update configuration from arguments
5. Validate WiX dark.exe availability
6. Process sample through GrandoreiroProcessor
7. Handle errors and exit appropriately

## 📋 Usage Examples

### Basic Sample Analysis

```bash
python -m grindoreiro sample.zip
```

### With Custom WiX Path

```bash
python -m grindoreiro --dark-path /path/to/dark.exe sample.zip
```

### Verbose Output

```bash
python -m grindoreiro --verbose sample.zip
```

### Keep Temporary Files

```bash
python -m grindoreiro --keep-temp sample.zip
```

### List Active Sessions

```bash
python -m grindoreiro --list-sessions
```

## 🔧 Argument Details

### Positional Arguments

#### sample
- **Type**: `str`
- **Required**: Yes
- **Description**: Path to Grandoreiro sample ZIP file

### Optional Arguments

#### --dark-path
- **Type**: `Path`
- **Default**: `config.dark_path` (./tools/wix/dark.exe)
- **Description**: Path to WiX dark.exe for MSI extraction

#### --samples-dir
- **Type**: `Path`
- **Default**: `config.samples_dir` (./data/samples/)
- **Description**: Directory containing sample files

#### --output-dir
- **Type**: `Path`
- **Default**: `config.output_dir` (./data/output/)
- **Description**: Directory for analysis output files

#### --keep-temp
- **Type**: `bool` (flag)
- **Default**: `False`
- **Description**: Keep temporary files after analysis

#### --verbose, -v
- **Type**: `bool` (flag)
- **Default**: `False`
- **Description**: Enable verbose (DEBUG level) logging

#### --list-sessions
- **Type**: `bool` (flag)
- **Default**: `False`
- **Description**: List all active analysis sessions

## 📊 Session Management

### list_active_sessions

Get information about active analysis sessions.

```python
from grindoreiro.core import list_active_sessions

sessions = list_active_sessions()
for session in sessions:
    print(f"Session: {session['session_id']}")
    print(f"Path: {session['path']}")
    print(f"Size: {session['size_mb']:.1f}MB")
    print(f"Created: {session['created']}")
```

**Returns:**
- `List[Dict]`: List of session information dictionaries

**Session Info:**
- `session_id`: Unique session identifier
- `path`: Path to session working directory
- `size_mb`: Size of session directory in MB
- `created`: Session creation timestamp
- `has_debug_marker`: Whether session has debug files

## 🔧 Configuration Integration

The CLI integrates with the configuration system:

### Configuration Updates

```python
# Update from command-line arguments
if args.samples_dir:
    config.samples_dir = args.samples_dir
if args.output_dir:
    config.output_dir = args.output_dir
```

### Default Values

- **WiX Path**: Uses `config.dark_path` if not specified
- **Directories**: Uses `config.samples_dir` and `config.output_dir`
- **User Agent**: Uses `config.default_user_agent`

## ⚠️ Error Handling

### Validation Errors

#### Missing dark.exe
```python
if not dark_path.exists():
    print(f"Error: dark.exe not found at {dark_path}")
    print("Please download WiX Toolset from: https://wixtoolset.org/releases/")
    sys.exit(1)
```

#### Processing Errors
```python
try:
    processor = GrandoreiroProcessor(dark_path)
    processor.process_sample(args.sample, keep_temp=args.keep_temp)
except Exception as e:
    print(f"Error processing sample: {e}")
    if args.verbose:
        import traceback
        traceback.print_exc()
    sys.exit(1)
```

### Exit Codes

- **0**: Success
- **1**: Error (missing files, processing failures)

## 📝 Logging Configuration

### Log Levels

- **Normal**: INFO level (20)
- **Verbose**: DEBUG level (10)

### Setup Process

```python
log_level = 10 if args.verbose else 20  # DEBUG or INFO
setup_logging(log_level)
```

## 🔧 Integration with Processor

### GrandoreiroProcessor Usage

```python
from grindoreiro.processor import GrandoreiroProcessor

processor = GrandoreiroProcessor(dark_path)
processor.process_sample(sample_path, keep_temp=args.keep_temp)
```

**Parameters:**
- `sample_path`: Path to sample ZIP file
- `keep_temp`: Whether to preserve temporary files

## 📋 Command-line Help

### Help Output

```bash
python -m grindoreiro --help
```

```
usage: grindoreiro [-h] [--dark-path DARK_PATH] [--samples-dir SAMPLES_DIR]
                   [--output-dir OUTPUT_DIR] [--keep-temp] [--verbose]
                   [--list-sessions]
                   sample

Grindoreiro - Malware Analysis Toolkit

positional arguments:
  sample                Path to Grandoreiro sample ZIP file

optional arguments:
  -h, --help            show this help message and exit
  --dark-path DARK_PATH Path to WiX dark.exe (default: ./tools/wix/dark.exe)
  --samples-dir SAMPLES_DIR
                        Samples directory (default: ./data/samples/)
  --output-dir OUTPUT_DIR
                        Output directory (default: ./data/output/)
  --keep-temp           Keep temporary files after analysis for manual inspection
  --verbose, -v         Enable verbose logging
  --list-sessions       List all active analysis sessions

Examples:
  python -m grindoreiro sample.zip
  python -m grindoreiro --dark-path /path/to/dark.exe sample.zip
  python -m grindoreiro --verbose sample.zip
```

## 🔗 Dependencies

- `argparse`: For command-line argument parsing
- `sys`: For system exit handling
- `pathlib.Path`: For file path handling
- `grindoreiro.core`: For configuration and logging
- `grindoreiro.processor`: For main processing logic</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\cli.md
