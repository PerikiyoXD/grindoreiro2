# GRINDOREIRO v2.0
Python utilities to unpack Grandoreiro .ZIPs with .MSI sample.

This is a refactored and improved version of the original Grindoreiro toolkit for analyzing and unpacking Grandoreiro malware samples.

## Features

- **Pipeline Architecture**: Modular processing pipeline with proper metadata collection
- **Comprehensive Results**: Detailed analysis results with JSON output and human-readable reports
- **Stage-based Processing**: Each processing stage is isolated and can be monitored independently
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Proper Error Handling**: Comprehensive exception handling and logging
- **Type Hints**: Full type annotations for better code maintainability
- **Configuration Management**: Centralized configuration with sensible defaults
- **CLI Interface**: Improved command-line interface with better argument handling
- **Logging**: Structured logging with configurable verbosity levels

## Components

- `grindoreiro.py`: Main entry point (legacy compatibility)
- `grindoreiro/`: Main package
  - `core.py`: Configuration and utilities
  - `extractor.py`: File extraction utilities
  - `analyzer.py`: String analysis and URL extraction
  - `iso_handler.py`: ISO download and decoding
  - `processor.py`: Main processing orchestration
  - `pipeline.py`: Pipeline architecture and results management
  - `pipeline_steps.py`: Concrete pipeline step implementations
  - `cli.py`: Command-line interface
  - `scripts/`: Standalone utility scripts

## Installation

### Prerequisites

Download the latest WiX Toolset from: https://wixtoolset.org/releases/
- Extract `wix311-binaries.zip`
- Place `dark.exe` in `./tools/wix/` directory

### Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install as package:
   ```bash
   pip install -e .
   ```

## Directory Structure

The tool organizes files in the following structure:

```
./data/
├── samples/          # Original sample files
├── cache/           # Cached downloads (ISOs, etc.)
├── temp/            # Temporary processing data (auto-cleaned)
└── output/          # Final results and reports
```

## Usage

### Main Tool

Process a Grandoreiro sample:
```bash
python grindoreiro.py sample.zip
# or if installed as package:
grindoreiro sample.zip
```

### Advanced Usage

```bash
# Specify custom paths
python -m grindoreiro.cli sample.zip --dark-path /path/to/dark.exe --verbose

# Use custom directories
python -m grindoreiro.cli sample.zip --samples-dir ./my_samples --output-dir ./my_output

# Enable debug logging
python -m grindoreiro.cli sample.zip --verbose
```

### Individual Tools

#### String Extractor
```bash
python stringripper.py file.dll
# or
python -m grindoreiro.scripts.stringripper file.dll --verbose --min-length 6
```

#### ISO Handler
```bash
python isoabduct.py http://example.com/fake.iso
# or
python -m grindoreiro.scripts.isoabduct http://example.com/fake.iso --output ./output
```

## Project Structure

```
grindoreiro/
├── grindoreiro/
│   ├── __init__.py
│   ├── __main__.py
│   ├── core.py          # Configuration and utilities
│   ├── extractor.py     # File extraction (ZIP, MSI)
│   ├── analyzer.py      # String analysis and URL extraction
│   ├── iso_handler.py   # ISO download/decoding
│   ├── processor.py     # Main processing logic
│   ├── cli.py           # Command-line interface
│   └── scripts/
│       ├── stringripper.py
│       └── isoabduct.py
├── grindoreiro.py       # Legacy entry point
├── stringripper.py      # Standalone string extractor
├── isoabduct.py         # Standalone ISO handler
├── setup.py
├── requirements.txt
└── README.md
```

## Configuration

The tool uses sensible defaults but can be configured:

- **WiX Path**: `./tools/wix/dark.exe`
- **Samples Directory**: `./samples/`
- **Output Directory**: `./output/`
- **User Agent**: Firefox-compatible string

## Development

### Running Tests

```bash
python -m pytest
```

### Code Quality

```bash
# Type checking
python -m mypy grindoreiro/

# Linting
python -m flake8 grindoreiro/

# Formatting
python -m black grindoreiro/
```

## Changes from v1.0

- **Refactored Architecture**: Modular design with clear separation of concerns
- **Error Handling**: Proper exception handling instead of bare `except` clauses
- **Logging**: Structured logging with configurable levels
- **Type Safety**: Full type hints throughout the codebase
- **Configuration**: Centralized configuration management
- **CLI Improvements**: Better argument parsing and help messages
- **Documentation**: Comprehensive docstrings and improved README
- **Maintainability**: Cleaner code structure and better naming conventions

## License

This project is provided as-is for educational and research purposes.
