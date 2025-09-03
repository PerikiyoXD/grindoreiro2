# Processor Module

> Main processing logic and orchestration

## 📦 Overview

The `grindoreiro.processor` module contains the main `GrandoreiroProcessor` class that orchestrates the entire analysis pipeline for Grandoreiro samples.

## 🔧 GrandoreiroProcessor Class

Main processor class that coordinates all analysis stages.

```python
from grindoreiro.processor import GrandoreiroProcessor
from pathlib import Path

# Create processor
processor = GrandoreiroProcessor()

# Process a sample
result = processor.process_sample(Path('sample.zip'))
print(f"Processing completed: {result.success}")
```

### Constructor

```python
def __init__(self, dark_path: Optional[Path] = None):
    """Initialize processor with dependencies.

    Args:
        dark_path: Path to WiX dark.exe (optional, uses config default)
    """
```

#### Parameters

- `dark_path` (Optional[Path]): Custom path to WiX dark.exe. If None, uses `config.dark_path`

### Methods

#### process_sample

Main method to process a Grandoreiro sample.

```python
def process_sample(self, sample_path: Path) -> ProcessingResult:
    """Process a Grandoreiro sample through the analysis pipeline.

    Args:
        sample_path: Path to the sample file to process

    Returns:
        ProcessingResult: Result of the processing operation

    Raises:
        ProcessingError: If processing fails critically
    """
```

**Parameters:**
- `sample_path` (Path): Path to the sample file (.zip)

**Returns:**
- `ProcessingResult`: Object containing processing results and metadata

**Example:**
```python
from pathlib import Path
from grindoreiro.processor import GrandoreiroProcessor

processor = GrandoreiroProcessor()
sample_path = Path('sample.zip')

try:
    result = processor.process_sample(sample_path)
    if result.success:
        print(f"✅ Analysis completed successfully")
        print(f"📁 Results saved to: {result.output_dir}")
    else:
        print(f"❌ Analysis failed: {result.error_message}")
except Exception as e:
    print(f"💥 Critical error: {e}")
```

## 📊 ProcessingResult Class

Result object returned by the processor.

```python
@dataclass
class ProcessingResult:
    """Result of a processing operation."""
    success: bool
    sample_path: Path
    output_dir: Path
    session_id: str
    processing_time: float
    error_message: Optional[str] = None
    stages_completed: List[str] = None
    stages_failed: List[str] = None
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | `bool` | Whether processing completed successfully |
| `sample_path` | `Path` | Path to the processed sample |
| `output_dir` | `Path` | Directory containing results |
| `session_id` | `str` | Unique session identifier |
| `processing_time` | `float` | Total processing time in seconds |
| `error_message` | `Optional[str]` | Error message if failed |
| `stages_completed` | `List[str]` | List of successfully completed stages |
| `stages_failed` | `List[str]` | List of failed stages |

## 🔄 Pipeline Integration

The processor integrates with the pipeline system:

```python
from grindoreiro.processor import GrandoreiroProcessor
from grindoreiro.pipeline import AnalysisPipeline

processor = GrandoreiroProcessor()

# Access the pipeline
pipeline = processor.pipeline

# Get pipeline steps
steps = pipeline.steps
for step in steps:
    print(f"Step: {step.name}")

# Access results manager
results_manager = processor.results_manager
```

## 🏗️ Pipeline Stages

The processor executes the following pipeline stages:

### 1. InitializeStep
- Creates working directories
- Sets up session context
- Initializes metadata

### 2. ExtractZipStep
- Extracts ZIP container
- Validates archive integrity
- Creates extraction directory

### 3. ExtractMsiStep
- Decompiles MSI installers using WiX
- Extracts embedded files
- Processes installation scripts

### 4. ExtractDllStep
- Extracts and analyzes DLL files
- Processes PE file structures
- Extracts embedded resources

### 5. AnalyzeStringsStep
- Extracts readable strings
- Filters by minimum length
- Identifies potential indicators

### 6. AnalyzeUrlsStep
- Extracts URLs and domains
- Categorizes by protocol
- Identifies C2 servers

### 7. ProcessIsoStep
- Downloads ISO files
- Extracts ISO contents
- Processes embedded payloads

### 8. FinalizeStep
- Cleans up temporary files
- Generates final reports
- Updates metadata

## ⚙️ Configuration

### Processor Configuration

```python
from grindoreiro.processor import GrandoreiroProcessor
from grindoreiro.core import Config

# Custom configuration
config = Config()
config.temp_dir = Path('./custom/temp')
config.output_dir = Path('./custom/output')

# Create processor with custom config
processor = GrandoreiroProcessor()
processor.config = config
```

### WiX Integration

```python
from pathlib import Path

# Custom WiX path
custom_dark_path = Path('/opt/wix/dark.exe')
processor = GrandoreiroProcessor(dark_path=custom_dark_path)

# Verify WiX availability
if not custom_dark_path.exists():
    print("Warning: Custom WiX path does not exist")
```

## 📊 Results Management

### Accessing Results

```python
from grindoreiro.processor import GrandoreiroProcessor

processor = GrandoreiroProcessor()
result = processor.process_sample(Path('sample.zip'))

# Check results
if result.success:
    print(f"✅ Success! Results in: {result.output_dir}")

    # List result files
    import os
    for file in os.listdir(result.output_dir):
        print(f"  - {file}")
else:
    print(f"❌ Failed: {result.error_message}")
    print(f"Failed stages: {result.stages_failed}")
```

### Results Structure

```
data/output/
├── sample_analysis.json          # Complete analysis data
├── sample_analysis.html          # Interactive HTML report
├── extracted_files/              # Extracted components
│   ├── msi_content/
│   ├── dll_files/
│   └── iso_content/
└── metadata.json                 # Processing metadata
```

## 🛠️ Advanced Usage

### Custom Processing

```python
from grindoreiro.processor import GrandoreiroProcessor
from grindoreiro.pipeline import PipelineContext

class CustomProcessor(GrandoreiroProcessor):
    def process_sample(self, sample_path):
        # Pre-processing
        self.logger.info("Starting custom processing")

        # Call parent processing
        result = super().process_sample(sample_path)

        # Post-processing
        if result.success:
            self.post_process_results(result)

        return result

    def post_process_results(self, result):
        # Custom post-processing logic
        pass
```

### Error Handling

```python
from grindoreiro.processor import GrandoreiroProcessor, ProcessingError

processor = GrandoreiroProcessor()

try:
    result = processor.process_sample(Path('sample.zip'))
except ProcessingError as e:
    print(f"Processing error: {e}")
    # Handle processing-specific errors
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle unexpected errors
```

### Progress Monitoring

```python
import time
from grindoreiro.processor import GrandoreiroProcessor

processor = GrandoreiroProcessor()

# Monitor processing progress
start_time = time.time()
result = processor.process_sample(Path('sample.zip'))
end_time = time.time()

print(f"Processing time: {end_time - start_time:.2f} seconds")
print(f"Stages completed: {len(result.stages_completed)}")
print(f"Stages failed: {len(result.stages_failed) if result.stages_failed else 0}")
```

## 🔧 Pipeline Customization

### Adding Custom Steps

```python
from grindoreiro.processor import GrandoreiroProcessor
from grindoreiro.pipeline import PipelineStep, PipelineContext

class CustomAnalysisStep(PipelineStep):
    def __init__(self):
        super().__init__("custom_analysis")

    def execute(self, context):
        # Custom analysis logic
        self.logger.info("Running custom analysis")
        # ... analysis code ...
        return StageResult.success()

# Add to processor
processor = GrandoreiroProcessor()
processor.pipeline.add_step(CustomAnalysisStep())
```

### Modifying Pipeline

```python
from grindoreiro.processor import GrandoreiroProcessor

processor = GrandoreiroProcessor()

# Remove a step
processor.pipeline.remove_step("analyze_urls")

# Replace a step
from grindoreiro.pipeline_steps import AnalyzeUrlsStep

class CustomUrlAnalyzer(AnalyzeUrlsStep):
    def execute(self, context):
        # Custom URL analysis
        return super().execute(context)

processor.pipeline.replace_step("analyze_urls", CustomUrlAnalyzer())
```

## 📈 Performance Considerations

### Memory Management

```python
# For large samples, monitor memory usage
import psutil
import os

def monitor_memory():
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    print(f"Memory usage: {memory_usage:.2f} MB")

processor = GrandoreiroProcessor()
monitor_memory()
result = processor.process_sample(Path('large-sample.zip'))
monitor_memory()
```

### Parallel Processing

```python
# For multiple samples, use batch processing
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def process_single_sample(sample_path):
    processor = GrandoreiroProcessor()
    return processor.process_sample(sample_path)

samples = [Path('sample1.zip'), Path('sample2.zip')]
max_workers = min(multiprocessing.cpu_count(), len(samples))

with ProcessPoolExecutor(max_workers=max_workers) as executor:
    results = list(executor.map(process_single_sample, samples))
```

## 🐛 Error Handling

### Common Errors

```python
from grindoreiro.processor import GrandoreiroProcessor, ProcessingError

processor = GrandoreiroProcessor()

try:
    result = processor.process_sample(Path('sample.zip'))
except ProcessingError as e:
    if "WiX" in str(e):
        print("WiX toolset not found. Please install WiX.")
    elif "permission" in str(e).lower():
        print("Permission denied. Check file permissions.")
    else:
        print(f"Processing error: {e}")
except FileNotFoundError:
    print("Sample file not found.")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Recovery Strategies

```python
def safe_process_sample(processor, sample_path, max_retries=3):
    """Process sample with retry logic."""
    for attempt in range(max_retries):
        try:
            return processor.process_sample(sample_path)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait before retry

processor = GrandoreiroProcessor()
result = safe_process_sample(processor, Path('sample.zip'))
```

## 📚 Related Modules

- **[Core Module](core.md)** - Configuration and utilities
- **[Pipeline Module](pipeline.md)** - Pipeline architecture
- **[Extractor Module](extractor.md)** - File extraction
- **[Analyzer Module](analyzer.md)** - String and URL analysis

## 📋 Module Contents

```python
# Main exports
__all__ = [
    "GrandoreiroProcessor",
    "ProcessingResult",
    "ProcessingError"
]

# Classes
class GrandoreiroProcessor:
    """Main processor for Grandoreiro malware analysis."""

class ProcessingResult:
    """Result of a processing operation."""

class ProcessingError(Exception):
    """Processing-specific exceptions."""
```

---

💡 **Note**: The `GrandoreiroProcessor` is the main entry point for sample analysis. It coordinates all pipeline stages and manages the overall analysis workflow.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\processor.md
