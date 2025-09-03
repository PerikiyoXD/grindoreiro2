# Extractor Module

> File extraction utilities for ZIP and MSI files

## 📦 Overview

The `grindoreiro.extractor` module provides utilities for extracting various file formats commonly found in Grandoreiro malware samples, including ZIP files containing MSI installers and MSI files themselves using the WiX Toolset.

## 🔧 FileExtractor Class

Main class for handling file extraction operations.

```python
from grindoreiro.extractor import FileExtractor
from pathlib import Path

# Create extractor with custom dark.exe path
extractor = FileExtractor(dark_path=Path('/path/to/dark.exe'))

# Extract ZIP file
extractor.extract_zip(Path('sample.zip'), Path('./extracted'))

# Extract MSI file
extractor.extract_msi(
    Path('installer.msi'),
    Path('./msi_output'),
    Path('./msi_script')
)
```

### Constructor

```python
def __init__(self, dark_path: Optional[Path] = None):
    """Initialize extractor with WiX dark.exe path.

    Args:
        dark_path: Path to WiX dark.exe (optional, uses config default)
    """
```

#### Parameters

- `dark_path` (Optional[Path]): Custom path to WiX dark.exe. If None, uses `config.dark_path`

### Methods

#### extract_zip

Extract contents of a ZIP file to specified directory.

```python
def extract_zip(self, zip_path: Path, output_dir: Path) -> None:
    """Extract ZIP file to output directory.

    Args:
        zip_path: Path to ZIP file to extract
        output_dir: Directory to extract files to

    Raises:
        FileNotFoundError: If ZIP file doesn't exist
        Exception: For extraction errors
    """
```

**Parameters:**
- `zip_path` (Path): Path to the ZIP file to extract
- `output_dir` (Path): Directory to extract files to

**Raises:**
- `FileNotFoundError`: If the ZIP file doesn't exist
- `Exception`: For ZIP extraction errors

#### extract_msi

Extract MSI file using WiX dark.exe.

```python
def extract_msi(self, msi_path: Path, extract_dir: Path, script_dir: Path) -> None:
    """Extract MSI file using WiX dark.exe.

    Args:
        msi_path: Path to MSI file to extract
        extract_dir: Directory for extracted files
        script_dir: Directory for WiX script output

    Raises:
        FileNotFoundError: If dark.exe or MSI file not found
        subprocess.CalledProcessError: If dark.exe fails
        Exception: For other extraction errors
    """
```

**Parameters:**
- `msi_path` (Path): Path to the MSI file to extract
- `extract_dir` (Path): Directory for extracted MSI contents
- `script_dir` (Path): Directory for WiX script (.wxs) output

**Raises:**
- `FileNotFoundError`: If dark.exe or MSI file doesn't exist
- `subprocess.CalledProcessError`: If dark.exe execution fails
- `Exception`: For other extraction errors

#### find_files_by_extension

Find all files with specified extension recursively.

```python
def find_files_by_extension(self, directory: Path, extension: str) -> List[Path]:
    """Find all files with given extension in directory recursively.

    Args:
        directory: Directory to search in
        extension: File extension to search for (without dot)

    Returns:
        List of paths to files with the specified extension
    """
```

**Parameters:**
- `directory` (Path): Directory to search in
- `extension` (str): File extension to search for (without dot, e.g., "dll")

**Returns:**
- `List[Path]`: List of paths to files with the specified extension

#### find_msi_file

Find the first MSI file in a directory.

```python
def find_msi_file(self, directory: Path) -> Optional[Path]:
    """Find the first MSI file in directory.

    Args:
        directory: Directory to search for MSI files

    Returns:
        Path to first MSI file found, or None if none found
    """
```

**Parameters:**
- `directory` (Path): Directory to search for MSI files

**Returns:**
- `Optional[Path]`: Path to first MSI file found, or None if none found

#### find_dll_files

Find malicious DLL files referenced in WiX scripts.

```python
def find_dll_files(self, directory: Path, exclude_patterns: Optional[List[str]] = None) -> List[Path]:
    """Find malicious DLL files referenced by CustomAction in WXS script.

    Args:
        directory: Directory containing extracted MSI files
        exclude_patterns: Patterns to exclude from results

    Returns:
        List of paths to malicious DLL files
    """
```

**Parameters:**
- `directory` (Path): Directory containing extracted MSI files
- `exclude_patterns` (Optional[List[str]]): Patterns to exclude from results

**Returns:**
- `List[Path]`: List of paths to malicious DLL files

**Notes:**
- Parses WiX script files (.wxs) for CustomAction entries
- Looks for DLLs with DllEntry="VIPS0033939" (malicious entry point)
- Excludes known legitimate DLLs like 'aicustact.dll'

#### copy_file

Copy a file from source to destination.

```python
def copy_file(self, source: Path, destination: Path) -> None:
    """Copy file from source to destination.

    Args:
        source: Source file path
        destination: Destination file path

    Raises:
        Exception: For file copy errors
    """
```

**Parameters:**
- `source` (Path): Source file path
- `destination` (Path): Destination file path

**Raises:**
- `Exception`: For file copy errors

## 📋 Usage Examples

### Basic ZIP Extraction

```python
from grindoreiro.extractor import FileExtractor

extractor = FileExtractor()
extractor.extract_zip(Path('sample.zip'), Path('./output'))
print("ZIP extracted successfully")
```

### MSI Extraction with WiX

```python
from grindoreiro.extractor import FileExtractor

extractor = FileExtractor(dark_path=Path('./tools/wix/dark.exe'))

# Extract MSI
extractor.extract_msi(
    Path('installer.msi'),
    Path('./msi_contents'),
    Path('./wix_scripts')
)

# Find extracted DLLs
dlls = extractor.find_dll_files(Path('./msi_contents'))
print(f"Found {len(dlls)} malicious DLLs")
```

### File Discovery

```python
from grindoreiro.extractor import FileExtractor

extractor = FileExtractor()

# Find all DLL files
dll_files = extractor.find_files_by_extension(Path('./extracted'), 'dll')

# Find MSI file
msi_file = extractor.find_msi_file(Path('./extracted'))
if msi_file:
    print(f"Found MSI: {msi_file}")
```

## 🔧 WiX Toolset Integration

The extractor integrates with the WiX Toolset for MSI extraction:

- **dark.exe**: Decompiles MSI files into directories and scripts
- **Script parsing**: Analyzes .wxs files for malicious components
- **Error handling**: Gracefully handles WiX tool errors and warnings

### WiX Command Structure

```bash
dark.exe installer.msi -x ./output -o ./script.wxs
```

## 📊 Directory Structure

After extraction, the following structure is created:

```
extraction_output/
├── Binary/           # MSI binary files (DLLs, EXEs)
├── SourceDir/        # MSI source files
└── script.wxs        # WiX script file
```

## ⚠️ Error Handling

The extractor handles various error conditions:

- **Missing dark.exe**: Raises `FileNotFoundError`
- **Invalid MSI files**: WiX tool reports errors
- **Permission issues**: Directory creation and file access errors
- **Corrupted archives**: ZIP/MSI corruption detection

## 🔗 Dependencies

- `zipfile`: For ZIP file handling
- `subprocess`: For executing WiX dark.exe
- `shutil`: For file operations
- `pathlib.Path`: For path handling
- `logging`: For debug and error messages</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\extractor.md
