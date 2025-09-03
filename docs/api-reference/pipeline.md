# Pipeline Module

> Pipeline architecture for Grandoreiro analysis

## 📦 Overview

The `grindoreiro.pipeline` module implements a flexible pipeline architecture for orchestrating the complete Grandoreiro malware analysis workflow. It provides a stage-based processing system with comprehensive metadata tracking and error handling.

## 🔧 Core Classes

### PipelineStage Enum

Defines the processing stages in the analysis pipeline.

```python
from grindoreiro.pipeline import PipelineStage

# Available stages
print(PipelineStage.INITIALIZE)      # initialize
print(PipelineStage.EXTRACT_ZIP)     # extract_zip
print(PipelineStage.EXTRACT_MSI)     # extract_msi
print(PipelineStage.EXTRACT_DLL)     # extract_dll
print(PipelineStage.ANALYZE_STRINGS) # analyze_strings
print(PipelineStage.ANALYZE_URLS)    # analyze_urls
print(PipelineStage.PROCESS_ISO)     # process_iso
print(PipelineStage.FINALIZE)        # finalize
```

### StageStatus Enum

Defines the possible statuses for pipeline stages.

```python
from grindoreiro.pipeline import StageStatus

# Status values
print(StageStatus.PENDING)   # pending
print(StageStatus.RUNNING)   # running
print(StageStatus.COMPLETED) # completed
print(StageStatus.FAILED)    # failed
print(StageStatus.SKIPPED)   # skipped
```

### StageResult Class

Represents the result of a pipeline stage execution.

```python
@dataclass
class StageResult:
    stage: PipelineStage
    status: StageStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[Path] = field(default_factory=list)
```

### SampleMetadata Class

Comprehensive metadata container for sample analysis.

```python
@dataclass
class SampleMetadata:
    sample_path: Path
    sample_name: str
    sample_size: int
    sha256_hash: str
    analysis_start: datetime

    # Session and file information
    session_id: str = ""
    extracted_files: List[Dict[str, Any]] = field(default_factory=list)
    file_hashes: Dict[str, FileHash] = field(default_factory=dict)

    # Analysis results
    strings_count: int = 0
    urls_found: List[str] = field(default_factory=list)
    cnc_url: Optional[str] = None
    download_url: Optional[str] = None

    # Processing and assessment
    stages: List[StageResult] = field(default_factory=list)
    threat_level: str = "unknown"
    malware_family: str = "unknown"
    analysis_summary: str = ""
```

### PipelineContext Class

Context object that maintains state throughout the pipeline execution.

```python
from grindoreiro.pipeline import PipelineContext

# Create context for a sample
context = PipelineContext(Path('sample.zip'))

# Access metadata
print(f"Session: {context.session_id}")
print(f"Sample: {context.metadata.sample_name}")
print(f"Size: {context.metadata.sample_size} bytes")
```

#### Constructor

```python
def __init__(self, sample_path: Union[str, Path]):
    """Initialize pipeline context.

    Args:
        sample_path: Path to the sample file to analyze
    """
```

#### Methods

##### add_stage_result

Add a stage result to the context.

```python
def add_stage_result(self, result: StageResult) -> None:
    """Add a stage result to the context.

    Args:
        result: StageResult to add
    """
```

##### get_stage_result

Get result for a specific stage.

```python
def get_stage_result(self, stage: PipelineStage) -> Optional[StageResult]:
    """Get result for a specific stage.

    Args:
        stage: Pipeline stage to get result for

    Returns:
        StageResult if found, None otherwise
    """
```

##### update_metadata

Update metadata with new information.

```python
def update_metadata(self, **kwargs) -> None:
    """Update metadata with new information.

    Args:
        **kwargs: Key-value pairs to update in metadata
    """
```

##### mark_completed

Mark the analysis as completed and calculate duration.

```python
def mark_completed(self) -> None:
    """Mark the analysis as completed."""
```

### PipelineStep Abstract Class

Abstract base class for pipeline steps.

```python
from grindoreiro.pipeline import PipelineStep, PipelineContext, StageResult

class CustomStep(PipelineStep):
    def __init__(self):
        super().__init__("custom_step")

    def can_execute(self, context: PipelineContext) -> bool:
        return True

    def execute(self, context: PipelineContext) -> StageResult:
        # Implementation here
        pass
```

#### Abstract Methods

##### execute

Execute the pipeline step.

```python
@abstractmethod
def execute(self, context: PipelineContext) -> StageResult:
    """Execute the pipeline step.

    Args:
        context: Pipeline execution context

    Returns:
        StageResult with execution results
    """
```

##### can_execute

Check if this step can be executed.

```python
@abstractmethod
def can_execute(self, context: PipelineContext) -> bool:
    """Check if this step can be executed.

    Args:
        context: Pipeline execution context

    Returns:
        True if step can execute, False otherwise
    """
```

#### Helper Methods

##### create_result

Create a stage result with common parameters.

```python
def create_result(self, stage: PipelineStage, success: bool = False,
                 error_message: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None,
                 artifacts: Optional[List[Path]] = None,
                 duration: Optional[float] = None) -> StageResult:
    """Create a stage result.

    Args:
        stage: Pipeline stage
        success: Whether stage succeeded
        error_message: Error message if failed
        metadata: Additional metadata
        artifacts: File artifacts produced
        duration: Execution duration in seconds

    Returns:
        StageResult object
    """
```

### AnalysisPipeline Class

Main pipeline orchestrator that manages step execution.

```python
from grindoreiro.pipeline import AnalysisPipeline

# Create pipeline
pipeline = AnalysisPipeline()

# Add steps (steps are added in pipeline_steps.py)
# pipeline.add_step(InitializeStep())
# pipeline.add_step(ExtractZipStep())
# etc.

# Execute pipeline
metadata = pipeline.execute(context)
```

#### Constructor

```python
def __init__(self):
    """Initialize analysis pipeline."""
```

#### Methods

##### add_step

Add a step to the pipeline.

```python
def add_step(self, step: PipelineStep) -> None:
    """Add a step to the pipeline.

    Args:
        step: PipelineStep to add
    """
```

##### execute

Execute the entire pipeline.

```python
def execute(self, context: PipelineContext) -> SampleMetadata:
    """Execute the entire pipeline.

    Args:
        context: Pipeline execution context

    Returns:
        Complete sample metadata with analysis results
    """
```

##### _generate_summary

Generate analysis summary (internal method).

```python
def _generate_summary(self, context: PipelineContext) -> None:
    """Generate analysis summary.

    Args:
        context: Pipeline execution context
    """
```

### ResultsManager Class

Manages analysis results and reporting.

```python
from grindoreiro.pipeline import ResultsManager

# Create results manager
manager = ResultsManager(Path('./output'))

# Save metadata as JSON
json_path = manager.save_metadata(metadata)

# Generate human-readable report
report = manager.generate_report(metadata)
```

#### Constructor

```python
def __init__(self, output_dir: Path):
    """Initialize results manager.

    Args:
        output_dir: Directory for output files
    """
```

#### Methods

##### save_metadata

Save metadata to file in specified format.

```python
def save_metadata(self, metadata: SampleMetadata, format: str = "json") -> Path:
    """Save metadata to file.

    Args:
        metadata: Sample metadata to save
        format: Output format (currently only 'json' supported)

    Returns:
        Path to saved file
    """
```

##### _save_json

Save metadata as JSON (internal method).

```python
def _save_json(self, metadata: SampleMetadata) -> Path:
    """Save metadata as JSON.

    Args:
        metadata: Sample metadata to save

    Returns:
        Path to saved JSON file
    """
```

##### generate_report

Generate a human-readable analysis report.

```python
def generate_report(self, metadata: SampleMetadata) -> str:
    """Generate a human-readable report.

    Args:
        metadata: Sample metadata

    Returns:
        Formatted report string
    """
```

## 📋 Usage Examples

### Basic Pipeline Execution

```python
from grindoreiro.pipeline import PipelineContext, AnalysisPipeline
from grindoreiro.pipeline_steps import (
    InitializeStep, ExtractZipStep, ExtractMsiStep,
    ExtractDllStep, AnalyzeStringsStep, AnalyzeUrlsStep,
    ProcessIsoStep, FinalizeStep
)

# Create pipeline
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

print(f"Analysis complete: {metadata.analysis_summary}")
```

### Custom Pipeline Step

```python
from grindoreiro.pipeline import PipelineStep, PipelineContext, PipelineStage

class CustomAnalysisStep(PipelineStep):
    def __init__(self):
        super().__init__("custom_analysis")

    def can_execute(self, context: PipelineContext) -> bool:
        # Check if previous steps succeeded
        dll_result = context.get_stage_result(PipelineStage.EXTRACT_DLL)
        return dll_result and dll_result.success

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            # Custom analysis logic here
            result = perform_custom_analysis(context)

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.ANALYZE_STRINGS,  # Use appropriate stage
                success=True,
                metadata={"custom_result": result},
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

## 🔧 Pipeline Architecture

### Stage Dependencies

```
INITIALIZE → EXTRACT_ZIP → EXTRACT_MSI → EXTRACT_DLL
                                      ↓
ANALYZE_STRINGS → ANALYZE_URLS → PROCESS_ISO
                                      ↓
FINALIZE
```

### Error Handling

- **Stage failures**: Don't stop pipeline unless critical
- **ISO processing**: Can fail due to network issues, non-critical
- **Exception handling**: Comprehensive error catching and logging
- **Recovery**: Attempt alternative approaches when possible

### Metadata Tracking

- **File hashes**: SHA256 for all extracted files
- **Timestamps**: Start/end times for each stage
- **Artifacts**: Track all generated files
- **Assessment**: Automatic threat level determination

## 📊 Output Formats

### JSON Metadata

```json
{
  "sample_info": {
    "name": "sample.zip",
    "size": 12345,
    "sha256": "abc123..."
  },
  "processing_stages": [
    {
      "stage": "extract_zip",
      "status": "completed",
      "success": true,
      "duration": 0.5
    }
  ],
  "assessment": {
    "threat_level": "high",
    "malware_family": "Grandoreiro"
  }
}
```

### Text Report

```
MALWARE ANALYSIS REPORT
==================================================
Sample: sample.zip
SHA256: abc123...
Size: 12,345 bytes
Threat Level: HIGH
Malware Family: Grandoreiro
==================================================
```

## ⚠️ Error Handling

The pipeline provides robust error handling:

- **Stage isolation**: Failures in one stage don't crash the pipeline
- **Graceful degradation**: Continue analysis even with partial failures
- **Detailed logging**: Comprehensive error messages and debugging info
- **Recovery mechanisms**: Alternative approaches for common failure scenarios

## 🔗 Dependencies

- `abc`: For abstract base classes
- `dataclasses`: For data structure definitions
- `datetime`: For timestamp handling
- `enum`: For stage and status enumerations
- `pathlib.Path`: For file path handling
- `typing`: For type hints
- `json`: For metadata serialization
- `logging`: For debug and error messages</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\api-reference\pipeline.md
