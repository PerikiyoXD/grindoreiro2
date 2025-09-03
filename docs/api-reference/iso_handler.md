# ISO Handler Module

> ISO download and decoding utilities

## 📦 Overview

The `grindoreiro.iso_handler` module provides utilities for downloading ISO files from URLs and decoding them. Grandoreiro malware often uses double-base64 encoded ISO files that contain ZIP archives with additional malware payloads.

## 🔧 ISODownloader Class

Main class for downloading and decoding ISO files.

```python
from grindoreiro.iso_handler import ISODownloader
from pathlib import Path

# Create downloader with custom user agent
downloader = ISODownloader(user_agent="Custom User Agent")

# Download ISO file
iso_path = downloader.download_iso("http://example.com/file.iso", Path('./downloads'))

# Decode ISO (base64 encoded ZIP)
zip_path = downloader.decode_iso(iso_path, Path('./decoded'))
```

### Constructor

```python
def __init__(self, user_agent: Optional[str] = None):
    """Initialize ISO downloader.

    Args:
        user_agent: Custom HTTP user agent string (optional)
    """
```

#### Parameters

- `user_agent` (Optional[str]): Custom HTTP user agent string. If None, uses Firefox default

### Methods

#### download_with_user_agent

Download URL content with custom user agent.

```python
def download_with_user_agent(self, url: str) -> requests.Response:
    """Download URL with custom user agent.

    Args:
        url: URL to download

    Returns:
        HTTP response object

    Raises:
        requests.Timeout: If request times out
        requests.TooManyRedirects: If too many redirects
        requests.RequestException: For other request errors
    """
```

**Parameters:**
- `url` (str): URL to download

**Returns:**
- `requests.Response`: HTTP response object

**Raises:**
- `requests.Timeout`: If request times out (30s timeout)
- `requests.TooManyRedirects`: If too many redirects occur
- `requests.RequestException`: For other HTTP request errors

#### download_iso

Download ISO file from URL to specified directory.

```python
def download_iso(self, url: str, output_dir: Path) -> Path:
    """Download ISO file from URL.

    Args:
        url: URL of ISO file to download
        output_dir: Directory to save downloaded file

    Returns:
        Path to downloaded ISO file

    Raises:
        requests.RequestException: For download errors
        Exception: For file writing errors
    """
```

**Parameters:**
- `url` (str): URL of ISO file to download
- `output_dir` (Path): Directory to save downloaded file

**Returns:**
- `Path`: Path to downloaded ISO file

**Raises:**
- `requests.RequestException`: For HTTP download errors
- `Exception`: For file writing errors

#### decode_iso

Decode base64-encoded ISO file containing ZIP archive.

```python
def decode_iso(self, iso_path: Path, output_dir: Path) -> Path:
    """Decode ISO file (base64 encoded ZIP).

    Args:
        iso_path: Path to encoded ISO file
        output_dir: Directory for decoded output

    Returns:
        Path to decoded ZIP file

    Raises:
        FileNotFoundError: If ISO file doesn't exist
        Exception: For decoding or file errors
    """
```

**Parameters:**
- `iso_path` (Path): Path to encoded ISO file
- `output_dir` (Path): Directory for decoded output

**Returns:**
- `Path`: Path to decoded ZIP file

**Raises:**
- `FileNotFoundError`: If ISO file doesn't exist
- `Exception`: For base64 decoding or file errors

## 📋 Usage Examples

### Basic ISO Download

```python
from grindoreiro.iso_handler import ISODownloader

downloader = ISODownloader()
iso_path = downloader.download_iso(
    "http://malicious-site.com/payload.iso",
    Path('./downloads')
)
print(f"Downloaded: {iso_path}")
```

### Complete ISO Processing Pipeline

```python
from grindoreiro.iso_handler import ISODownloader
from grindoreiro.extractor import FileExtractor

# Download ISO
downloader = ISODownloader()
iso_path = downloader.download_iso(url, Path('./temp'))

# Decode ISO (double base64)
zip_path = downloader.decode_iso(iso_path, Path('./temp'))

# Extract ZIP contents
extractor = FileExtractor()
extractor.extract_zip(zip_path, Path('./extracted'))

print("ISO processing complete")
```

### Custom User Agent

```python
from grindoreiro.iso_handler import ISODownloader

# Use custom user agent to avoid detection
downloader = ISODownloader(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

iso_path = downloader.download_iso(url, output_dir)
```

## 🔧 Decoding Process

The ISO decoding process handles Grandoreiro's encoding scheme:

1. **First decode**: Base64 decode the ISO file content
2. **Intermediate save**: Save first decode as `encoded.b64`
3. **Second decode**: Base64 decode the intermediate file
4. **Final output**: Save as `decoded.zip`

### Encoding Scheme

```
ISO File (Base64) → Base64 Decode → Intermediate (Base64) → Base64 Decode → ZIP File
```

## 📊 File Formats

### Input Format
- **ISO files**: Base64-encoded text files
- **Content**: Double-encoded ZIP archives
- **Encoding**: UTF-8 text with base64 content

### Output Format
- **Decoded files**: Standard ZIP archives
- **Contents**: Typically contain executable files (.exe)
- **Location**: Specified output directory

## ⚠️ Error Handling

The handler provides robust error handling:

- **Network errors**: HTTP timeouts, connection failures
- **Invalid URLs**: Malformed URL detection
- **Encoding errors**: Invalid base64 data handling
- **File system errors**: Permission and disk space issues
- **Corrupted data**: Graceful handling of malformed content

### Common Error Scenarios

```python
try:
    iso_path = downloader.download_iso(url, output_dir)
    zip_path = downloader.decode_iso(iso_path, output_dir)
except requests.Timeout:
    print("Download timed out")
except ValueError:
    print("Invalid base64 encoding")
except Exception as e:
    print(f"Processing failed: {e}")
```

## 🔧 Configuration

### Default User Agent
```
Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0
```

### Network Settings
- **Timeout**: 30 seconds for HTTP requests
- **Redirects**: Automatic handling of HTTP redirects
- **SSL**: Default SSL verification enabled

## 📈 Performance Considerations

- **Memory usage**: Large ISO files loaded entirely into memory
- **Network**: Single-threaded downloads
- **Caching**: No built-in caching (use external cache systems)

## 🔗 Dependencies

- `base64`: For encoding/decoding operations
- `requests`: For HTTP downloads
- `pathlib.Path`: For file path handling
- `logging`: For debug and error messages</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\iso_handler.md
