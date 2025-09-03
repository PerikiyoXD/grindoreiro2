# Basic Usage

> Core functionality and essential commands for Grindoreiro

## 📋 Command Overview

Grindoreiro provides multiple ways to analyze Grandoreiro samples:

| Command | Purpose | Use Case |
|---------|---------|----------|
| `python grindoreiro.py` | Legacy entry point | Quick analysis |
| `python -m grindoreiro.cli` | Modern CLI interface | Full-featured analysis |
| `python demo_analysis.py` | Demonstration | Learning/testing |
| `python batch_analyze_all.py` | Batch processing | Multiple samples |

## 🔧 Core Analysis

### Single Sample Analysis

```bash
# Basic analysis
python grindoreiro.py sample.zip

# Using CLI module (recommended)
python -m grindoreiro.cli sample.zip

# With verbose output
python -m grindoreiro.cli sample.zip --verbose

# Keep temporary files for inspection
python -m grindoreiro.cli sample.zip --keep-temp
```

### Analysis Options

| Option | Description | Example |
|--------|-------------|---------|
| `--verbose` | Detailed logging | `--verbose` |
| `--keep-temp` | Preserve temp files | `--keep-temp` |
| `--dark-path` | Custom WiX path | `--dark-path /path/to/dark.exe` |
| `--samples-dir` | Custom samples dir | `--samples-dir ./my-samples` |
| `--output-dir` | Custom output dir | `--output-dir ./results` |

## 📁 Directory Structure

Grindoreiro organizes files in a specific structure:

```
data/
├── samples/          # Input: Your Grandoreiro samples
├── cache/           # Cache: Downloaded ISOs and resources
├── temp/            # Temp: Processing files (auto-cleaned)
└── output/          # Output: Analysis results and reports
```

### Sample Placement

Place your Grandoreiro samples in `./data/samples/`:

```bash
# Example structure
data/samples/
├── sample1.zip
├── sample2.zip
└── DOC__34867_FRT.zip
```

## 📊 Understanding Results

### Output Files

After analysis, check `./data/output/` for:

- **`sample_analysis.json`**: Complete analysis data
- **`sample_analysis.html`**: Interactive web report
- **`extracted_files/`**: Individual extracted components

### Analysis Stages

Grindoreiro processes samples through these stages:

1. **📦 Extraction**: Unpack ZIP containers
2. **📋 MSI Processing**: Decompile MSI installers
3. **🔍 String Analysis**: Extract readable strings
4. **🌐 URL Analysis**: Identify network indicators
5. **💿 ISO Handling**: Process embedded ISO files
6. **📊 Report Generation**: Create JSON/HTML reports

## 🛠️ Utility Tools

### String Extraction

Extract strings from any file:

```bash
# Basic extraction
python stringripper.py malware.dll

# With options
python stringripper.py malware.dll --min-length 8 --verbose

# Using module
python -m grindoreiro.scripts.stringripper malware.dll
```

### ISO Processing

Download and decode ISO files:

```bash
# Download and process ISO
python isoabduct.py https://example.com/malware.iso

# With custom output
python isoabduct.py https://example.com/malware.iso --output ./results

# Using module
python -m grindoreiro.scripts.isoabduct https://example.com/malware.iso
```

## 🔍 Monitoring Analysis

### Log Files

Check `grindoreiro.log` for detailed information:

```bash
# View recent logs
tail -f grindoreiro.log

# Search for specific entries
grep "ERROR" grindoreiro.log
```

### Verbose Mode

Use `--verbose` for detailed console output:

```bash
python -m grindoreiro.cli sample.zip --verbose
```

## 📈 Performance Tips

### Large Samples

For large samples, consider:

```bash
# Use verbose mode to monitor progress
python -m grindoreiro.cli large-sample.zip --verbose

# Check available disk space
df -h

# Monitor system resources
top  # or Task Manager on Windows
```

### Multiple Samples

For batch processing, see [Batch Processing](batch-processing.md).

## 🆘 Common Issues

### WiX Toolset Not Found

```
Error: WiX dark.exe not found at ./tools/wix/dark.exe
```

**Solution**: Install WiX Toolset as described in [Getting Started](getting-started.md)

### Permission Errors

```
PermissionError: [Errno 13] Permission denied
```

**Solution**: Run with appropriate permissions or use `--output-dir` with writeable location

### Memory Issues

For large samples, ensure sufficient RAM:

```bash
# Check available memory
free -h  # Linux
# or
systeminfo | findstr Memory  # Windows
```

## 📚 Related Topics

- [Batch Processing](batch-processing.md) - Analyzing multiple samples
- [HTML Reports](html-reports.md) - Viewing and understanding results
- [Configuration](configuration.md) - Customizing behavior
- [Troubleshooting](troubleshooting.md) - Solving common problems

## 🔧 Advanced Usage

For advanced scenarios, see:

- [CLI Interface](../tools/cli-interface.md) - Complete command reference
- [API Reference](../api-reference/core.md) - Programmatic usage
- [Extending Pipeline](../developer-guides/extending-pipeline.md) - Custom analysis steps

---

💡 **Tip**: Always use `--verbose` when learning or troubleshooting to see detailed progress information.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\user-guides\basic-usage.md
