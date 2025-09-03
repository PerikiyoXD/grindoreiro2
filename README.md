# GRINDOREIRO v1.0.0

> Malware analysis toolkit for Grandoreiro samples

A comprehensive toolkit for analyzing and unpacking Grandoreiro malware samples with batch processing, interactive HTML reports, and modern Python packaging.

[![GitHub](https://img.shields.io/badge/GitHub-PerikiyoXD/grindoreiro2-blue)](https://github.com/PerikiyoXD/grindoreiro2)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **🔄 Batch Processing**: Parallel analysis of multiple samples with progress tracking
- **📊 Interactive HTML Reports**: Deduplication, search, filtering, and export capabilities
- **🏗️ Modern Architecture**: Modular pipeline with proper error handling and logging
- **⚡ Fast Analysis**: Optimized processing with type hints and structured logging
- **🛠️ CLI Tools**: Comprehensive command-line interface with flexible options
- **📦 Easy Installation**: Modern Python packaging with uv support

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Analyze a single sample
python grindoreiro.py sample.zip

# 3. Analyze all samples in batch
python batch_analyze_all.py

# 4. Generate HTML reports
python batch_html_report.py
```

## 📦 Installation

### Prerequisites

1. **WiX Toolset** (for MSI decompilation):
   - Download from: https://wixtoolset.org/releases/
   - Extract `wix311-binaries.zip`
   - Place `dark.exe` in `./tools/wix/` directory

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or using uv (recommended):
uv pip install -r requirements.txt

# Optional: Install as package
pip install -e .
```

## 📖 Usage

### Core Commands

| Command | Description |
|---------|-------------|
| `python grindoreiro.py sample.zip` | Analyze single sample |
| `python batch_analyze_all.py` | Analyze all samples in parallel |
| `python batch_html_report.py` | Generate HTML reports |
| `python demo_analysis.py` | Run demonstration |

### Advanced Usage

```bash
# Custom paths and options
python -m grindoreiro.cli sample.zip \
  --dark-path /path/to/dark.exe \
  --samples-dir ./my_samples \
  --output-dir ./my_output \
  --verbose

# Individual tools
python stringripper.py file.dll --verbose --min-length 6
python isoabduct.py http://example.com/fake.iso --output ./output
```

## 📁 Project Structure

```
grindoreiro/
├── grindoreiro/              # Main package
│   ├── core.py               # Configuration & utilities
│   ├── cli.py                # Command-line interface
│   ├── processor.py          # Main processing logic
│   ├── extractor.py          # File extraction (ZIP, MSI)
│   ├── analyzer.py           # String analysis & URL extraction
│   ├── iso_handler.py        # ISO download/decoding
│   ├── pipeline.py           # Pipeline architecture
│   └── scripts/              # Standalone utilities
├── batch_*.py                # Batch processing tools
├── html_*.py                 # HTML report generators
├── demo_analysis.py          # Demonstration script
├── pyproject.toml            # Modern packaging
├── uv.lock                   # Dependency lock
└── requirements.txt          # Dependencies
```

## 🏗️ Architecture

### Pipeline Stages

1. **Extraction**: Unpack ZIP and MSI files
2. **Analysis**: Extract strings and URLs
3. **Processing**: Analyze patterns and indicators
4. **Reporting**: Generate JSON and HTML reports

### Key Components

- **Pipeline Architecture**: Modular processing with metadata collection
- **Error Handling**: Comprehensive exception handling
- **Type Safety**: Full type annotations throughout
- **Configuration**: Centralized settings with sensible defaults
- **Logging**: Structured logging with configurable levels

## 📊 HTML Reports

Interactive HTML reports with advanced features:

- **🔍 Search & Filter**: Real-time filtering of files, URLs, and strings
- **📋 Deduplication**: Automatic grouping of duplicate content
- **📤 Export**: Download findings as JSON or CSV
- **📱 Responsive**: Works on desktop and mobile devices
- **🎨 Modern UI**: Clean, professional interface

```bash
# Generate reports
python html_report_generator.py data/output/sample_analysis.json
python batch_html_report.py  # Generate all reports
```

See [`HTML_REPORT_README.md`](HTML_REPORT_README.md) for detailed documentation.

## ⚙️ Configuration

The tool uses sensible defaults but can be customized:

| Setting | Default | Description |
|---------|---------|-------------|
| WiX Path | `./tools/wix/dark.exe` | Path to WiX decompiler |
| Samples Dir | `./data/samples/` | Input directory |
| Output Dir | `./data/output/` | Results directory |
| User Agent | Firefox-compatible | HTTP user agent |

## 🛠️ Development

### Testing

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

### Building

```bash
# Build package
python -m build

# Install locally
pip install -e .
```

## 📋 Directory Structure

The tool organizes files as follows:

```
./data/
├── samples/          # Input: Original sample files
├── cache/           # Cache: Downloaded ISOs, etc.
├── temp/            # Temp: Auto-cleaned processing data
└── output/          # Output: Analysis results and reports
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is provided **as-is** for educational and research purposes.

**MIT License** - see [LICENSE](LICENSE) for details.

## 🔗 Links

- **GitHub**: https://github.com/PerikiyoXD/grindoreiro2
- **Issues**: https://github.com/PerikiyoXD/grindoreiro2/issues
- **WiX Toolset**: https://wixtoolset.org/releases/

---

*Built with ❤️ for malware analysis and research*
