# Troubleshooting

> Solving common issues and problems with Grindoreiro

## 🔍 Quick Diagnosis

### Check System Status

```bash
# Verify Python installation
python --version
python -c "import grindoreiro; print('Grindoreiro imported successfully')"

# Check dependencies
pip list | grep -E "(requests|chardet)"

# Verify file permissions
ls -la data/
ls -la tools/wix/dark.exe
```

### Common Quick Fixes

```bash
# Clear cache and temp files
rm -rf data/cache/* data/temp/*

# Reset permissions
chmod +x tools/wix/dark.exe
chmod -R 755 data/

# Check disk space
df -h
```

## 🚨 Critical Errors

### WiX Toolset Issues

**Error**: `WiX dark.exe not found`

**Symptoms**:
```
Error: Could not find WiX dark.exe at ./tools/wix/dark.exe
dark.exe is not recognized as an internal or external command
```

**Solutions**:

1. **Install WiX Toolset**:
   ```bash
   # Download from official site
   wget https://wixtoolset.org/downloads/v3.11.2.4516/wix311-binaries.zip
   unzip wix311-binaries.zip -d tools/wix/
   ```

2. **Verify Installation**:
   ```bash
   ls -la tools/wix/dark.exe
   ./tools/wix/dark.exe  # Test execution
   ```

3. **Custom Path**:
   ```bash
   python -m grindoreiro.cli sample.zip --dark-path /custom/path/dark.exe
   ```

4. **Windows PATH**:
   ```cmd
   set PATH=%PATH%;C:\path\to\wix
   ```

### Memory Errors

**Error**: `MemoryError` or `Out of memory`

**Symptoms**:
- Analysis fails on large files
- System becomes unresponsive
- Python crashes unexpectedly

**Solutions**:

1. **Increase System Memory**:
   ```bash
   # Check current memory
   free -h  # Linux
   systeminfo | findstr Memory  # Windows
   ```

2. **Process Smaller Batches**:
   ```bash
   # Instead of batch_analyze_all.py
   python batch_analyze.py sample1.zip sample2.zip
   ```

3. **Reduce Parallelism**:
   ```bash
   export GRINDOREIRO_MAX_WORKERS=1
   python batch_analyze_all.py
   ```

4. **Monitor Memory Usage**:
   ```bash
   # Linux
   top -p $(pgrep python)
   # Windows
   # Use Task Manager or Process Explorer
   ```

### Permission Errors

**Error**: `PermissionError` or `Access denied`

**Symptoms**:
- Cannot write to output directory
- Cannot execute dark.exe
- Cannot read sample files

**Solutions**:

1. **Fix File Permissions**:
   ```bash
   # Make executable
   chmod +x tools/wix/dark.exe

   # Fix directory permissions
   chmod -R 755 data/
   chown -R $USER:$USER data/
   ```

2. **Use Sudo (not recommended)**:
   ```bash
   sudo python -m grindoreiro.cli sample.zip
   ```

3. **Custom Directories**:
   ```bash
   python -m grindoreiro.cli sample.zip --output-dir ./my-output
   ```

4. **Windows Permissions**:
   ```cmd
   # Run as Administrator
   # or check security permissions in Properties
   ```

## 🌐 Network Issues

### Connection Problems

**Error**: `ConnectionError` or `TimeoutError`

**Symptoms**:
- ISO downloads fail
- Network requests timeout
- SSL certificate errors

**Solutions**:

1. **Check Network Connectivity**:
   ```bash
   ping google.com
   curl -I https://example.com
   ```

2. **Proxy Configuration**:
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ```

3. **SSL Issues**:
   ```bash
   # Disable SSL verification (not recommended for production)
   export GRINDOREIRO_SSL_VERIFY=false
   ```

4. **Timeout Settings**:
   ```bash
   export GRINDOREIRO_TIMEOUT=120
   export GRINDOREIRO_MAX_RETRIES=5
   ```

### DNS Resolution

**Error**: `Name resolution failure`

**Solutions**:
```bash
# Check DNS
nslookup example.com

# Use different DNS
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

## 📁 File System Issues

### Disk Space

**Error**: `No space left on device`

**Solutions**:
```bash
# Check disk usage
df -h

# Clean up temp files
rm -rf data/temp/*
rm -rf data/cache/*

# Find large files
find data/ -type f -size +100M

# Monitor disk usage
du -sh data/
```

### File Corruption

**Error**: `BadZipFile` or `Corrupted file`

**Symptoms**:
- ZIP files won't open
- MSI files are corrupted
- Analysis fails unexpectedly

**Solutions**:

1. **Verify File Integrity**:
   ```bash
   # Check ZIP integrity
   unzip -t sample.zip

   # Check file size
   ls -lh sample.zip

   # Calculate hash
   sha256sum sample.zip
   ```

2. **Redownload Samples**:
   ```bash
   # If downloaded from internet
   wget -c https://source.com/sample.zip
   ```

3. **File System Check**:
   ```bash
   # Linux
   fsck /dev/sda1
   # Windows
   chkdsk C:
   ```

## 🔧 Analysis Issues

### Pipeline Failures

**Error**: `Pipeline step failed`

**Symptoms**:
- Analysis stops at specific stage
- Partial results generated
- Error logs show stage failure

**Solutions**:

1. **Check Logs**:
   ```bash
   tail -f grindoreiro.log
   grep "ERROR" grindoreiro.log
   ```

2. **Run Individual Steps**:
   ```bash
   # Test extraction only
   python -c "
   from grindoreiro.extractor import FileExtractor
   extractor = FileExtractor()
   # Test code
   "
   ```

3. **Verbose Mode**:
   ```bash
   python -m grindoreiro.cli sample.zip --verbose --keep-temp
   ```

### String Analysis Issues

**Error**: No strings found or incorrect strings

**Solutions**:

1. **Adjust String Length**:
   ```bash
   python stringripper.py file.dll --min-length 3
   ```

2. **Check File Type**:
   ```bash
   file sample.zip
   ```

3. **Manual Verification**:
   ```bash
   strings file.dll | head -20
   ```

## 📊 Report Generation Issues

### HTML Report Problems

**Error**: Report not generated or displays incorrectly

**Solutions**:

1. **Check JSON Input**:
   ```bash
   python -c "import json; json.load(open('data/output/sample_analysis.json'))"
   ```

2. **Browser Issues**:
   ```bash
   # Try different browser
   # Check console for JavaScript errors
   # Disable browser extensions
   ```

3. **Template Issues**:
   ```bash
   # Check template file
   ls -la report_template.html
   ```

### Batch Report Issues

**Error**: Batch report incomplete or missing

**Solutions**:

1. **Verify Individual Reports**:
   ```bash
   ls -la data/output/*_analysis.json
   ```

2. **Check Batch Script**:
   ```bash
   python batch_html_report.py --verbose
   ```

3. **Memory Issues**:
   ```bash
   # Large batches may need more memory
   python batch_html_report.py --max-memory 2048
   ```

## 🐛 Debugging Techniques

### Enable Debug Logging

```bash
# Maximum verbosity
export GRINDOREIRO_LOG_LEVEL=DEBUG
python -m grindoreiro.cli sample.zip --verbose

# Log to file
export GRINDOREIRO_LOG_FILE=debug.log
```

### Step-by-Step Debugging

```python
# debug.py
import logging
logging.basicConfig(level=logging.DEBUG)

from grindoreiro.core import get_logger
from grindoreiro.processor import GrandoreiroProcessor

logger = get_logger(__name__)

# Step-by-step execution
processor = GrandoreiroProcessor()
context = processor.pipeline.create_context("sample.zip")

# Execute individual steps
for step in processor.pipeline.steps:
    try:
        result = step.execute(context)
        logger.info(f"Step {step.name}: {result.status}")
    except Exception as e:
        logger.error(f"Step {step.name} failed: {e}")
        break
```

### Profiling Performance

```python
# profile.py
import cProfile
import pstats

def profile_analysis():
    cProfile.run('main()', 'profile.stats')
    stats = pstats.Stats('profile.stats')
    stats.sort_stats('cumulative').print_stats(20)

if __name__ == '__main__':
    profile_analysis()
```

## 🛠️ Advanced Troubleshooting

### Environment Isolation

```bash
# Create isolated environment
python -m venv debug_env
source debug_env/bin/activate
pip install -r requirements.txt

# Test in isolation
python -m grindoreiro.cli sample.zip
```

### Dependency Conflicts

```bash
# Check for conflicts
pip check

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Use specific versions
pip install requests==2.25.1 chardet==4.0.0
```

### System Compatibility

```bash
# Check system info
uname -a
python --version
pip --version

# Test basic functionality
python -c "import sys; print(sys.platform)"
```

## 📞 Getting Help

### Log Analysis

```bash
# Extract error patterns
grep "ERROR\|CRITICAL" grindoreiro.log | tail -10

# Find most common errors
grep "ERROR" grindoreiro.log | sed 's/.*ERROR//' | sort | uniq -c | sort -nr
```

### Support Information

When reporting issues, include:

```bash
# System information
uname -a
python --version
pip list | grep -E "(requests|chardet|grindoreiro)"

# Error details
tail -50 grindoreiro.log

# Configuration
cat grindoreiro.ini 2>/dev/null || echo "No config file"

# Sample information
ls -la sample.zip
file sample.zip
```

## 🚨 Emergency Procedures

### Data Recovery

```bash
# Recover from temp files
find data/temp/ -name "*.extracted" -exec cp {} data/output/ \;

# Restore from backup
cp -r backup/data/* data/
```

### System Cleanup

```bash
# Complete cleanup
rm -rf data/temp/*
rm -rf data/cache/*
rm -rf __pycache__/
find . -name "*.pyc" -delete

# Reset to clean state
git clean -fd
git reset --hard HEAD
```

### Last Resort

```bash
# Nuclear option - complete reinstall
rm -rf venv/
rm -rf data/output/*
rm -rf data/cache/*
pip uninstall grindoreiro -y
pip install -r requirements.txt
```

## 📋 Prevention

### Best Practices

1. **Regular Backups**:
   ```bash
   # Automate backups
   crontab -e
   # Add: 0 2 * * * tar -czf backup-$(date +%Y%m%d).tar.gz data/
   ```

2. **Monitor Resources**:
   ```bash
   # Set up monitoring
   # Check disk space, memory, and logs regularly
   ```

3. **Test Environment**:
   ```bash
   # Always test with small samples first
   python demo_analysis.py
   ```

## 📚 Related Topics

- [Getting Started](getting-started.md) - Initial setup
- [Basic Usage](basic-usage.md) - Common operations
- [Configuration](configuration.md) - Settings and customization
- [Batch Processing](batch-processing.md) - Large-scale issues

---

💡 **Pro Tip**: Enable verbose logging (`--verbose`) and check `grindoreiro.log` for detailed error information before seeking help.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\user-guides\troubleshooting.md
