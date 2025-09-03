# Batch Processing

> Analyzing multiple Grandoreiro samples efficiently

## 🎯 Overview

Batch processing allows you to analyze multiple samples simultaneously, saving time and providing consolidated results.

## 🚀 Quick Start

```bash
# Analyze all samples in parallel
python batch_analyze_all.py

# Analyze specific samples
python batch_analyze.py sample1.zip sample2.zip sample3.zip
```

## 📋 Available Tools

### Batch Analyze All

**Purpose**: Process all samples in `./data/samples/` with parallel execution

```bash
python batch_analyze_all.py
```

**Features**:
- ✅ Parallel processing (up to 4 concurrent processes)
- ✅ Automatic false negative analysis
- ✅ Progress tracking and error reporting
- ✅ Consolidated logging

### Batch Analyzer

**Purpose**: Process specific samples or custom file lists

```bash
# Multiple specific samples
python batch_analyze.py sample1.zip sample2.zip

# With custom output directory
python batch_analyze.py --output-dir ./custom-output sample1.zip

# Verbose mode
python batch_analyze.py --verbose sample1.zip sample2.zip
```

## ⚙️ Configuration

### Parallel Processing

`batch_analyze_all.py` automatically determines optimal parallelism:

- **CPU Detection**: Uses `min(CPU cores, sample count, 4)`
- **Memory Management**: Prevents excessive memory usage
- **Error Isolation**: Individual sample failures don't stop batch

### Custom Settings

```bash
# Custom WiX path
python batch_analyze_all.py --dark-path /custom/path/dark.exe

# Custom samples directory
python batch_analyze_all.py --samples-dir ./my-samples

# Custom output directory
python batch_analyze_all.py --output-dir ./batch-results
```

## 📊 Output Structure

Batch processing creates organized output:

```
data/output/
├── sample1_analysis.json
├── sample1_analysis.html
├── sample2_analysis.json
├── sample2_analysis.html
├── batch_report.html          # Consolidated batch report
├── false_negative_analysis.html  # False negative report
└── extracted_files/
    ├── sample1/
    └── sample2/
```

### Batch Report Features

The `batch_report.html` provides:

- 📊 **Summary Statistics**: Total samples, success/failure rates
- 🔍 **Sample Overview**: Quick access to individual reports
- 📈 **Performance Metrics**: Processing times and resource usage
- 🚨 **Error Summary**: Failed samples and error details

## 🔍 False Negative Analysis

After batch processing, `batch_analyze_all.py` automatically runs:

```bash
python batch_false_negative_analyzer.py
```

This analyzes results for:
- **Detection Gaps**: Samples that might have been missed
- **Pattern Analysis**: Common failure modes
- **Quality Assurance**: Verification of analysis completeness

## 📈 Performance Optimization

### Large Batch Processing

For large numbers of samples:

1. **Monitor Resources**:
   ```bash
   # Check system resources
   top  # Linux
   # or Task Manager on Windows
   ```

2. **Stagger Processing**:
   ```bash
   # Process in smaller batches
   python batch_analyze.py sample1.zip sample2.zip sample3.zip
   python batch_analyze.py sample4.zip sample5.zip sample6.zip
   ```

3. **Parallel Limits**:
   - Default: 4 concurrent processes
   - Adjust based on system capabilities
   - Monitor memory usage

### Disk Space Management

```bash
# Check available space
df -h  # Linux
# or
wmic logicaldisk get size,freespace  # Windows

# Clean temp files if needed
rm -rf data/temp/*
```

## 🆘 Troubleshooting

### Common Issues

#### No Samples Found
```
Error: No sample files found in ./data/samples
```

**Solutions**:
- Verify samples are in `./data/samples/`
- Check file extensions (should be `.zip`)
- Ensure proper permissions

#### WiX Toolset Missing
```
Error: WiX dark.exe not found
```

**Solutions**:
- Install WiX Toolset (see [Getting Started](getting-started.md))
- Use `--dark-path` to specify custom location
- Verify `dark.exe` is executable

#### Memory Issues
```
MemoryError: Out of memory
```

**Solutions**:
- Reduce concurrent processes
- Process samples individually
- Increase system RAM
- Use `--keep-temp false` to reduce disk usage

#### Permission Errors
```
PermissionError: Access denied
```

**Solutions**:
- Run with appropriate permissions
- Use `--output-dir` with writeable location
- Check antivirus exclusions

### Error Recovery

```bash
# Check logs for details
tail -f grindoreiro.log

# Re-run failed samples individually
python -m grindoreiro.cli failed-sample.zip --verbose

# Skip problematic samples
python batch_analyze.py $(ls data/samples/*.zip | grep -v problematic)
```

## 📊 Monitoring Progress

### Log Monitoring

```bash
# Follow batch progress
tail -f grindoreiro.log

# Search for specific sample
grep "sample1.zip" grindoreiro.log

# Count successful/failed
grep "SUCCESS\|FAILED" grindoreiro.log | sort | uniq -c
```

### Process Monitoring

```bash
# View running processes
ps aux | grep python

# Monitor resource usage
top -p $(pgrep -f batch_analyze)

# Check disk usage
du -sh data/
```

## 📋 Best Practices

### File Organization

```
data/
├── samples/
│   ├── batch1/           # Group related samples
│   ├── batch2/
│   └── quarantine/       # Suspicious samples
└── output/
    ├── batch1-results/
    └── batch2-results/
```

### Naming Conventions

- Use descriptive names: `DOC__34867_FRT.zip`
- Include dates: `2025-01-15_sample.zip`
- Add identifiers: `campaign-abc_sample.zip`

### Quality Assurance

1. **Verify Results**: Check `batch_report.html`
2. **Review Logs**: Scan for errors in `grindoreiro.log`
3. **Spot Check**: Manually verify random samples
4. **False Negative Review**: Examine `false_negative_analysis.html`

## 🔧 Advanced Features

### Custom Batch Scripts

Create custom batch processing:

```python
#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

samples = [
    "sample1.zip",
    "sample2.zip",
    # ... more samples
]

for sample in samples:
    cmd = [sys.executable, "-m", "grindoreiro.cli", sample, "--verbose"]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Failed: {sample}")
        # Handle error
```

### Integration with Other Tools

```bash
# Process samples and generate reports
python batch_analyze_all.py

# Export results for other tools
python -c "
import json
with open('data/output/batch_report.json', 'r') as f:
    data = json.load(f)
    # Process data for other tools
"
```

## 📚 Related Topics

- [Basic Usage](basic-usage.md) - Single sample analysis
- [HTML Reports](html-reports.md) - Understanding batch reports
- [Configuration](configuration.md) - Customizing batch behavior
- [CLI Interface](../tools/cli-interface.md) - Command-line options

## 📈 Scaling Up

For very large batches:

1. **Distributed Processing**: Split across multiple machines
2. **Queue Systems**: Use tools like Celery or RQ
3. **Cloud Resources**: Leverage cloud computing
4. **Database Storage**: Store results in databases
5. **Monitoring**: Implement comprehensive monitoring

---

💡 **Pro Tip**: Always run a small test batch first to verify your setup before processing large numbers of samples.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\user-guides\batch-processing.md
