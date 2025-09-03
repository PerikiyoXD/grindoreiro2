# Analyzer Module

> String extraction and URL analysis utilities

## 📦 Overview

The `grindoreiro.analyzer` module provides utilities for extracting strings from binary files and analyzing them for URLs and patterns commonly found in Grandoreiro malware samples.

## 🔧 StringExtractor Class

Main class for extracting strings from binary files.

```python
from grindoreiro.analyzer import StringExtractor

# Create extractor with custom minimum length
extractor = StringExtractor(min_length=6)

# Extract strings from a DLL file
strings = extractor.extract_strings(Path('malware.dll'))
print(f"Extracted {len(strings)} strings")
```

### Constructor

```python
def __init__(self, min_length: int = 4):
    """Initialize string extractor.

    Args:
        min_length: Minimum string length to extract (default: 4)
    """
```

#### Parameters

- `min_length` (int): Minimum length of strings to extract. Default is 4 characters.

### Methods

#### extract_strings

Extract strings from a binary file and optionally save to output file.

```python
def extract_strings(self, file_path: Path, output_path: Optional[Path] = None) -> List[str]:
    """Extract strings from binary file.

    Args:
        file_path: Path to the binary file to analyze
        output_path: Optional path to save strings to file

    Returns:
        List of extracted strings

    Raises:
        FileNotFoundError: If input file doesn't exist
        Exception: For file reading or processing errors
    """
```

**Parameters:**
- `file_path` (Path): Path to the binary file to analyze
- `output_path` (Optional[Path]): Path to save extracted strings. If None, uses `file_path` with `.strings` extension

**Returns:**
- `List[str]`: List of extracted strings

**Raises:**
- `FileNotFoundError`: If the input file doesn't exist
- `Exception`: For file reading or processing errors

## 🔍 URLAnalyzer Class

Analyzes extracted strings for URLs and C&C patterns.

```python
from grindoreiro.analyzer import URLAnalyzer

analyzer = URLAnalyzer()
urls = analyzer.find_urls(strings)
cnc_url = analyzer.find_cnc_url(urls)
```

### Constructor

```python
def __init__(self):
    """Initialize URL analyzer with default patterns."""
```

### Methods

#### find_urls

Find all HTTP/HTTPS URLs in a list of strings.

```python
def find_urls(self, strings: List[str]) -> Set[str]:
    """Find all URLs in list of strings.

    Args:
        strings: List of strings to search for URLs

    Returns:
        Set of unique URLs found
    """
```

**Parameters:**
- `strings` (List[str]): List of strings to search for URLs

**Returns:**
- `Set[str]`: Set of unique URLs found

#### find_cnc_url

Find C&C server URL based on Grandoreiro patterns.

```python
def find_cnc_url(self, urls: Set[str]) -> Optional[str]:
    """Find C&C URL based on known patterns.

    Args:
        urls: Set of URLs to search

    Returns:
        C&C URL if found, None otherwise
    """
```

**Parameters:**
- `urls` (Set[str]): Set of URLs to search for C&C patterns

**Returns:**
- `Optional[str]`: C&C URL if found, None otherwise

**Notes:**
- Looks for URLs containing "5050/index.php" pattern

#### find_download_url

Find download URL based on specified pattern.

```python
def find_download_url(self, urls: Set[str], pattern: str = "iso") -> Optional[str]:
    """Find download URL based on pattern.

    Args:
        urls: Set of URLs to search
        pattern: Pattern to match in URL (default: "iso")

    Returns:
        Download URL if found, None otherwise
    """
```

**Parameters:**
- `urls` (Set[str]): Set of URLs to search
- `pattern` (str): Pattern to match in URL. Default is "iso"

**Returns:**
- `Optional[str]`: Download URL if found, None otherwise

## 📋 Usage Examples

### Basic String Extraction

```python
from grindoreiro.analyzer import StringExtractor
from pathlib import Path

extractor = StringExtractor(min_length=5)
strings = extractor.extract_strings(Path('sample.dll'))
print(f"Found {len(strings)} strings")
```

### URL Analysis Pipeline

```python
from grindoreiro.analyzer import StringExtractor, URLAnalyzer

# Extract strings
extractor = StringExtractor()
strings = extractor.extract_strings(Path('malware.dll'))

# Analyze for URLs
url_analyzer = URLAnalyzer()
urls = url_analyzer.find_urls(strings)

# Find specific URLs
cnc_url = url_analyzer.find_cnc_url(urls)
download_url = url_analyzer.find_download_url(urls, "iso")

print(f"Found {len(urls)} URLs")
if cnc_url:
    print(f"C&C Server: {cnc_url}")
if download_url:
    print(f"Download URL: {download_url}")
```

## 🔧 Configuration

The analyzer uses the following default patterns:

- **ASCII strings**: Printable ASCII characters (A-Za-z0-9+/=\-:. ,_$%'()[\]<> )
- **Unicode strings**: Same pattern for UTF-16 encoded strings
- **HTTP patterns**: `http://[^\s]+`
- **HTTPS patterns**: `https://[^\s]+`
- **C&C pattern**: URLs containing "5050/index.php"

## 📊 Output Format

String extraction creates a `.strings` file with one string per line:

```
This is a sample string
http://example.com/malware
Another extracted string
```

## ⚠️ Error Handling

The analyzer handles common errors gracefully:

- **File not found**: Raises `FileNotFoundError`
- **Permission errors**: Raises appropriate exceptions
- **Encoding errors**: Uses error handling for malformed UTF-16 data
- **Empty files**: Returns empty list without error

## 🔗 Dependencies

- `pathlib.Path`: For file path handling
- `re`: For regex pattern matching
- `logging`: For debug and error messages</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\analyzer.md
