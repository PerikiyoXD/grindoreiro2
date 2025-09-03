# Getting Started

> Quick start guide for new users of Grindoreiro

## 🎯 Prerequisites

Before you begin, ensure you have:

- **Python 3.7+** installed
- **WiX Toolset** for MSI decompilation
- Basic familiarity with command-line tools

## 📦 Installation

### 1. Clone or Download

```bash
git clone https://github.com/PerikiyoXD/grindoreiro2.git
cd grindoreiro2
```

### 2. Install WiX Toolset

Download the latest WiX Toolset from [wixtoolset.org](https://wixtoolset.org/releases/):

1. Download `wix311-binaries.zip`
2. Extract to `./tools/wix/` directory
3. Ensure `dark.exe` is in `./tools/wix/dark.exe`

### 3. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install as package
pip install -e .
```

### 4. Verify Installation

```bash
# Test basic functionality
python demo_analysis.py

# Check CLI help
python -m grindoreiro.cli --help
```

## 🚀 Your First Analysis

### Quick Demo

Run the demonstration to see Grindoreiro in action:

```bash
python demo_analysis.py
```

This will:
- Create a test file with sample data
- Extract strings and URLs
- Show the analysis process

### Analyze a Real Sample

```bash
# Basic analysis
python grindoreiro.py path/to/sample.zip

# With verbose output
python grindoreiro.py path/to/sample.zip --verbose

# Using the CLI module
python -m grindoreiro.cli path/to/sample.zip
```

## 📊 Understanding the Output

After analysis, you'll find results in `./data/output/`:

```
data/output/
├── sample_analysis.json    # Detailed analysis results
├── sample_analysis.html    # Interactive HTML report
└── extracted_files/        # Extracted components
```

### Key Output Files

- **JSON Results**: Complete analysis data in structured format
- **HTML Report**: Interactive web-based report with search and filtering
- **Extracted Files**: Individual components extracted from the sample

## 🎯 Next Steps

1. **Learn Basic Commands**: See [Basic Usage](../user-guides/basic-usage.md)
2. **Configure the Tool**: Check [Configuration](../user-guides/configuration.md)
3. **Generate Reports**: Learn about [HTML Reports](../user-guides/html-reports.md)
4. **Batch Processing**: See [Batch Processing](../user-guides/batch-processing.md)

## 🆘 Need Help?

- **Check the Logs**: Look for error messages in `grindoreiro.log`
- **Verbose Mode**: Use `--verbose` flag for detailed output
- **Troubleshooting**: See [Troubleshooting](../user-guides/troubleshooting.md)

## 📚 Further Reading

- [Basic Usage](../user-guides/basic-usage.md) - Core functionality
- [Architecture](../developer-guides/architecture.md) - How it works
- [API Reference](../api-reference/core.md) - Technical details

---

🎉 **Congratulations!** You're ready to start analyzing Grandoreiro samples with Grindoreiro.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\user-guides\getting-started.md
