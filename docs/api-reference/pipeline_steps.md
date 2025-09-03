# Pipeline Steps Module

> Concrete pipeline steps for Grandoreiro analysis

## 📦 Overview

The `grindoreiro.pipeline_steps` module contains concrete implementations of pipeline steps that perform the actual analysis work. Each step handles a specific phase of the Grandoreiro malware analysis process.

## 🔧 Pipeline Step Classes

### InitializeStep

Initializes the analysis context and creates working directories.

```python
from grindoreiro.pipeline_steps import InitializeStep

step = InitializeStep()
result = step.execute(context)
```

#### Methods

##### can_execute

Always returns True - initialization is always possible.

##### execute

Creates working directory structure and calculates sample hash.

**Creates directories:**
- `extract`: For ZIP extraction
- `msi_output`: For MSI extraction
- `msi_script`: For WiX scripts
- `dll`: For DLL files
- `iso`: For ISO processing
- `exe`: For executable files

### ExtractZipStep

Extracts the ZIP file containing the MSI installer.

```python
from grindoreiro.pipeline_steps import ExtractZipStep

step = ExtractZipStep(dark_path=Path('./tools/wix/dark.exe'))
result = step.execute(context)
```

#### Constructor

```python
def __init__(self, dark_path: Optional[Path] = None):
    """Initialize ZIP extraction step.

    Args:
        dark_path: Path to WiX dark.exe (optional)
    """
```

#### Methods

##### can_execute

Returns True if initialization step completed successfully.

##### execute

Extracts ZIP file and collects metadata for all extracted files.

**Outputs:**
- Extracted files in working directory
- File metadata with hashes and sizes
- List of extracted files in context metadata

### ExtractMsiStep

Extracts the MSI file using WiX dark.exe.

```python
from grindoreiro.pipeline_steps import ExtractMsiStep

step = ExtractMsiStep(dark_path=Path('./tools/wix/dark.exe'))
result = step.execute(context)
```

#### Constructor

```python
def __init__(self, dark_path: Optional[Path] = None):
    """Initialize MSI extraction step.

    Args:
        dark_path: Path to WiX dark.exe (optional)
    """
```

#### Methods

##### can_execute

Returns True if ZIP extraction step completed successfully.

##### execute

Finds MSI file in extracted ZIP and extracts it using WiX.

**Outputs:**
- Extracted MSI contents
- WiX script files
- MSI metadata and hash

### ExtractDllStep

Extracts and copies the malicious DLL file.

```python
from grindoreiro.pipeline_steps import ExtractDllStep

step = ExtractDllStep(dark_path=Path('./tools/wix/dark.exe'))
result = step.execute(context)
```

#### Constructor

```python
def __init__(self, dark_path: Optional[Path] = None):
    """Initialize DLL extraction step.

    Args:
        dark_path: Path to WiX dark.exe (optional)
    """
```

#### Methods

##### can_execute

Returns True if MSI extraction step completed successfully.

##### execute

Finds malicious DLL files by parsing WiX scripts and copies the first one.

**Detection logic:**
- Parses .wxs files for CustomAction entries
- Looks for DllEntry="VIPS0033939" (malicious entry point)
- Excludes known legitimate DLLs

### AnalyzeStringsStep

Extracts strings from the malicious DLL file.

```python
from grindoreiro.pipeline_steps import AnalyzeStringsStep

step = AnalyzeStringsStep()
result = step.execute(context)
```

#### Constructor

```python
def __init__(self):
    """Initialize string analysis step."""
```

#### Methods

##### can_execute

Returns True if DLL extraction step completed successfully.

##### execute

Extracts strings from DLL and saves them to .strings file.

**Outputs:**
- Strings file alongside DLL
- String count in metadata
- List of extracted strings

### AnalyzeUrlsStep

Analyzes extracted strings for URLs and C&C patterns.

```python
from grindoreiro.pipeline_steps import AnalyzeUrlsStep

step = AnalyzeUrlsStep()
result = step.execute(context)
```

#### Constructor

```python
def __init__(self):
    """Initialize URL analysis step."""
```

#### Methods

##### can_execute

Returns True if string analysis step completed successfully.

##### execute

Analyzes strings for URLs and identifies C&C and download URLs.

**Detection patterns:**
- HTTP/HTTPS URL extraction
- C&C pattern: "5050/index.php"
- Download URL pattern: configurable (default: "iso")

### ProcessIsoStep

Downloads and processes ISO files from identified URLs.

```python
from grindoreiro.pipeline_steps import ProcessIsoStep

step = ProcessIsoStep(dark_path=Path('./tools/wix/dark.exe'))
result = step.execute(context)
```

#### Constructor

```python
def __init__(self, dark_path: Optional[Path] = None):
    """Initialize ISO processing step.

    Args:
        dark_path: Path to WiX dark.exe (optional)
    """
```

#### Methods

##### can_execute

Returns True if URL analysis found a download URL.

##### execute

Downloads ISO, decodes it (double base64), and extracts contents.

**Process:**
1. Check cache for existing ISO
2. Download ISO if not cached
3. Decode double-base64 encoding
4. Extract ZIP contents
5. Copy executable to output directory

### FinalizeStep

Finalizes the analysis and generates summary.

```python
from grindoreiro.pipeline_steps import FinalizeStep

step = FinalizeStep()
result = step.execute(context)
```

#### Constructor

```python
def __init__(self):
    """Initialize finalization step."""
```

#### Methods

##### can_execute

Always returns True - finalization is always possible.

##### execute

Updates network status and prepares final assessment.

**Outputs:**
- Network analysis status
- Stage completion summary
- Final metadata updates

## 📋 Usage Examples

### Creating a Complete Pipeline

```python
from grindoreiro.pipeline import AnalysisPipeline
from grindoreiro.pipeline_steps import *

# Create pipeline with all steps
pipeline = AnalysisPipeline()
pipeline.add_step(InitializeStep())
pipeline.add_step(ExtractZipStep())
pipeline.add_step(ExtractMsiStep())
pipeline.add_step(ExtractDllStep())
pipeline.add_step(AnalyzeStringsStep())
pipeline.add_step(AnalyzeUrlsStep())
pipeline.add_step(ProcessIsoStep())
pipeline.add_step(FinalizeStep())

# Execute
context = PipelineContext(Path('sample.zip'))
metadata = pipeline.execute(context)
```

### Custom Step Implementation

```python
from grindoreiro.pipeline_steps import PipelineStep
from grindoreiro.pipeline import PipelineContext, PipelineStage

class CustomAnalysisStep(PipelineStep):
    def __init__(self):
        super().__init__("custom_analysis")

    def can_execute(self, context: PipelineContext) -> bool:
        # Check if DLL analysis completed
        dll_result = context.get_stage_result(PipelineStage.EXTRACT_DLL)
        return dll_result and dll_result.success

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            dll_result = context.get_stage_result(PipelineStage.EXTRACT_DLL)
            dll_path = Path(dll_result.metadata["dll_copy"])

            # Perform custom analysis
            custom_result = analyze_dll_custom(dll_path)

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.ANALYZE_STRINGS,  # Use appropriate stage enum
                success=True,
                metadata={"custom_analysis": custom_result},
                duration=duration
            )

        except Exception as e:
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.ANALYZE_STRINGS,
                success=False,
                error_message=str(e),
                duration=duration
            )
```

## 🔧 Step Dependencies

### Execution Order

```
InitializeStep
    ↓
ExtractZipStep
    ↓
ExtractMsiStep
    ↓
ExtractDllStep
    ↓
AnalyzeStringsStep
    ↓
AnalyzeUrlsStep
    ↓
ProcessIsoStep
    ↓
FinalizeStep
```

### Conditional Execution

- **ExtractMsiStep**: Requires successful ZIP extraction
- **ExtractDllStep**: Requires successful MSI extraction
- **AnalyzeStringsStep**: Requires successful DLL extraction
- **AnalyzeUrlsStep**: Requires successful string analysis
- **ProcessIsoStep**: Requires download URL from URL analysis

## 📊 Metadata Updates

Each step updates the context metadata:

### InitializeStep
```python
metadata.update({
    "sample_hash": str,
    "work_dir": str,
    "temp_dir": str,
    "step_dirs": dict,
    "session_id": str
})
```

### ExtractZipStep
```python
metadata.extracted_files = [
    {
        "name": str,
        "path": str,
        "size": int,
        "sha256": str
    }
]
metadata.file_hashes["extracted_*"] = FileHash
```

### ExtractMsiStep
```python
metadata.msi_info = {
    "msi_path": str,
    "msi_size": int,
    "msi_sha256": str,
    "output_dir": str,
    "script_dir": str
}
metadata.file_hashes["msi"] = FileHash
```

### ExtractDllStep
```python
metadata.dll_info = {
    "original_path": str,
    "copied_path": str,
    "size": int,
    "name": str,
    "sha256": str
}
metadata.file_hashes["dll"] = FileHash
```

### AnalyzeStringsStep
```python
metadata.strings_count = int
```

### AnalyzeUrlsStep
```python
metadata.urls_found = List[str]
metadata.cnc_url = Optional[str]
metadata.download_url = Optional[str]
```

### ProcessIsoStep
```python
metadata.file_hashes["iso"] = FileHash
metadata.file_hashes["decoded_zip"] = FileHash
metadata.file_hashes["executable"] = FileHash
```

## ⚠️ Error Handling

### Common Failure Scenarios

- **WiX tool missing**: FileNotFoundError for dark.exe
- **Corrupted archives**: ZIP/MSI extraction failures
- **Network issues**: ISO download timeouts
- **Permission errors**: File access denied
- **Invalid encodings**: Base64 decoding failures

### Error Recovery

- **MSI extraction**: Retry without script output on failure
- **ISO processing**: Use cached files when available
- **String analysis**: Fallback to file reading if needed

## 🔧 Configuration

### File Paths
- **WiX dark.exe**: Configurable per step or use default
- **Working directories**: Auto-created in session temp directory
- **Output directory**: Uses config.output_dir for final files

### Cache System
- **ISO caching**: Automatic caching in data/cache/
- **Hash verification**: SHA256 comparison for cache hits

## 📈 Performance Considerations

### Execution Times
- **ExtractZipStep**: Fast (file copy operations)
- **ExtractMsiStep**: Variable (depends on MSI size)
- **ExtractDllStep**: Fast (file parsing and copy)
- **AnalyzeStringsStep**: Fast (memory-based string extraction)
- **AnalyzeUrlsStep**: Fast (regex matching)
- **ProcessIsoStep**: Slow (network download + decoding)

### Memory Usage
- **String extraction**: Loads entire DLL into memory
- **ISO processing**: Handles large files in chunks
- **Metadata storage**: Accumulates file hashes and metadata

## 🔗 Dependencies

- `pathlib.Path`: For file path handling
- `time`: For duration measurement
- `hashlib`: For file hashing
- `PipelineStep`: Base class from pipeline module
- `FileExtractor`: From extractor module
- `StringExtractor`: From analyzer module
- `URLAnalyzer`: From analyzer module
- `ISODownloader`: From iso_handler module
- `FileHash`: From core module</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\pipeline_steps.md
