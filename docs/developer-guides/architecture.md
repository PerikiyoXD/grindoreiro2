# Architecture Guide

> Understanding Grindoreiro's modular architecture and design patterns

## 📦 Overview

Grindoreiro follows a modular, extensible architecture designed for malware analysis. This guide explains the core components, design patterns, and extension mechanisms.

## 🏗️ Core Architecture

### Modular Design Principles

Grindoreiro is built on several key architectural principles:

- **Modularity**: Components are loosely coupled and independently deployable
- **Extensibility**: Easy to add new analysis modules and processing steps
- **Configurability**: Highly configurable through files and environment variables
- **Testability**: Components designed for easy unit and integration testing
- **Performance**: Optimized for batch processing and large-scale analysis

### Main Components

```
grindoreiro/
├── core/           # Core functionality and configuration
├── cli/            # Command-line interface
├── processor/      # Main analysis processor
├── pipeline/       # Pipeline orchestration
├── extractor/      # File extraction utilities
├── analyzer/       # Analysis modules
├── iso_handler/    # ISO file handling
├── scripts/        # Standalone utilities
└── pipeline_steps/ # Processing pipeline steps
```

## 🔧 Core Components

### Configuration System (`core/`)

The configuration system provides centralized configuration management:

```python
# core/config.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
import os

@dataclass
class Config:
    """Central configuration class."""

    # File paths
    input_dir: str = "./data/samples"
    output_dir: str = "./data/output"
    temp_dir: str = "./data/temp"
    cache_dir: str = "./data/cache"

    # Processing options
    max_workers: int = 4
    timeout: int = 300
    verbose: bool = False

    # Analysis options
    extract_strings: bool = True
    extract_urls: bool = True
    calculate_hashes: bool = True

    # Reporting options
    generate_html: bool = True
    generate_json: bool = True

    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables."""
        return cls(
            input_dir=os.getenv('GRINDOREIRO_INPUT_DIR', cls.input_dir),
            output_dir=os.getenv('GRINDOREIRO_OUTPUT_DIR', cls.output_dir),
            max_workers=int(os.getenv('GRINDOREIRO_MAX_WORKERS', cls.max_workers)),
            verbose=os.getenv('GRINDOREIRO_VERBOSE', '').lower() == 'true'
        )

    @classmethod
    def from_file(cls, path: str) -> 'Config':
        """Create config from YAML file."""
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data.get('grindoreiro', {}))
```

**Key Features**:
- Environment variable support
- YAML configuration files
- Type hints and validation
- Default value handling

### Processor (`processor/`)

The processor orchestrates the analysis workflow:

```python
# processor/processor.py
from typing import Dict, Any, List
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import logging

from grindoreiro.core import Config
from grindoreiro.pipeline import Pipeline

class Processor:
    """Main analysis processor."""

    def __init__(self, config: Config):
        self.config = config
        self.pipeline = Pipeline(config)
        self.logger = logging.getLogger(__name__)

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file."""
        self.logger.info(f"Processing {file_path}")

        context = {
            'file_path': file_path,
            'config': self.config,
            'start_time': datetime.now()
        }

        try:
            # Run analysis pipeline
            result = self.pipeline.run(context)

            # Add metadata
            result['processing_time'] = (datetime.now() - context['start_time']).total_seconds()
            result['success'] = True

        except Exception as e:
            self.logger.error(f"Processing failed for {file_path}: {e}")
            result = {
                'file_path': str(file_path),
                'success': False,
                'error': str(e),
                'processing_time': (datetime.now() - context['start_time']).total_seconds()
            }

        return result

    def process_batch(self, file_paths: List[Path]) -> List[Dict[str, Any]]:
        """Process multiple files in parallel."""
        self.logger.info(f"Processing {len(file_paths)} files")

        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            results = list(executor.map(self.process_file, file_paths))

        return results
```

**Key Features**:
- Single file and batch processing
- Parallel execution with thread pools
- Error handling and logging
- Processing time tracking

### Pipeline System (`pipeline/`)

The pipeline system provides extensible analysis workflows:

```python
# pipeline/pipeline.py
from typing import Dict, Any, List, Callable
from grindoreiro.core import Config
from grindoreiro.pipeline_steps import PipelineStep

class Pipeline:
    """Analysis pipeline orchestrator."""

    def __init__(self, config: Config):
        self.config = config
        self.steps: List[PipelineStep] = []
        self._load_default_steps()

    def add_step(self, step: PipelineStep) -> None:
        """Add a processing step to the pipeline."""
        self.steps.append(step)

    def insert_step(self, index: int, step: PipelineStep) -> None:
        """Insert a step at a specific position."""
        self.steps.insert(index, step)

    def remove_step(self, step_name: str) -> None:
        """Remove a step by name."""
        self.steps = [s for s in self.steps if s.name != step_name]

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the pipeline."""
        for step in self.steps:
            try:
                context = step.process(context)
            except Exception as e:
                context['error'] = f"Step {step.name} failed: {e}"
                if not step.continue_on_error:
                    break
        return context

    def _load_default_steps(self) -> None:
        """Load default processing steps."""
        from grindoreiro.pipeline_steps import (
            FileValidationStep,
            HashCalculationStep,
            ExtractionStep,
            StringAnalysisStep,
            URLAnalysisStep,
            ReportGenerationStep
        )

        self.steps = [
            FileValidationStep(),
            HashCalculationStep(),
            ExtractionStep(),
            StringAnalysisStep(),
            URLAnalysisStep(),
            ReportGenerationStep()
        ]
```

**Key Features**:
- Extensible step system
- Step ordering and management
- Error handling per step
- Continue-on-error capability

### Pipeline Steps (`pipeline_steps/`)

Pipeline steps are modular analysis components:

```python
# pipeline_steps/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class PipelineStep(ABC):
    """Base class for pipeline steps."""

    def __init__(self, name: str = None, continue_on_error: bool = False):
        self.name = name or self.__class__.__name__
        self.continue_on_error = continue_on_error

    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process the context and return updated context."""
        pass

# pipeline_steps/extraction.py
from pathlib import Path
import zipfile
import tarfile
import logging

class ExtractionStep(PipelineStep):
    """Extract archives and compressed files."""

    def __init__(self):
        super().__init__("ExtractionStep")
        self.logger = logging.getLogger(__name__)

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']

        extracted_files = []
        extraction_dir = self._create_extraction_dir(file_path)

        try:
            if file_path.suffix.lower() in ['.zip']:
                extracted_files = self._extract_zip(file_path, extraction_dir)
            elif file_path.suffix.lower() in ['.tar', '.gz', '.bz2']:
                extracted_files = self._extract_tar(file_path, extraction_dir)
            elif file_path.suffix.lower() in ['.7z']:
                extracted_files = self._extract_7z(file_path, extraction_dir)
            elif file_path.suffix.lower() in ['.iso']:
                extracted_files = self._extract_iso(file_path, extraction_dir)

        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            context['extraction_error'] = str(e)

        context['extracted_files'] = extracted_files
        context['extraction_dir'] = extraction_dir

        return context

    def _extract_zip(self, file_path: Path, output_dir: Path) -> List[Path]:
        """Extract ZIP archive."""
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        return list(output_dir.rglob('*'))

    def _create_extraction_dir(self, file_path: Path) -> Path:
        """Create extraction directory."""
        extraction_dir = file_path.parent / f"{file_path.stem}_extracted"
        extraction_dir.mkdir(exist_ok=True)
        return extraction_dir
```

**Key Features**:
- Abstract base class for consistency
- Specialized extraction methods
- Error handling and logging
- File type detection

## 🔌 Extension Mechanisms

### Custom Pipeline Steps

To add custom analysis steps:

```python
# custom_steps.py
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any

class CustomAnalysisStep(PipelineStep):
    """Custom analysis step example."""

    def __init__(self, analysis_config: Dict[str, Any]):
        super().__init__("CustomAnalysisStep")
        self.config = analysis_config

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']

        # Perform custom analysis
        analysis_result = self._analyze_file(file_path)

        # Add results to context
        context['custom_analysis'] = analysis_result

        return context

    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Perform custom file analysis."""
        # Custom analysis logic here
        return {
            'custom_metric': 0.85,
            'findings': ['suspicious_pattern_1', 'suspicious_pattern_2'],
            'confidence': 'high'
        }

# Usage
from grindoreiro.pipeline import Pipeline
from grindoreiro.core import Config

config = Config()
pipeline = Pipeline(config)

# Add custom step
custom_step = CustomAnalysisStep({'threshold': 0.8})
pipeline.add_step(custom_step)
```

### Custom Extractors

To add support for new file formats:

```python
# custom_extractors.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class BaseExtractor(ABC):
    """Base class for file extractors."""

    @abstractmethod
    def can_extract(self, file_path: Path) -> bool:
        """Check if this extractor can handle the file."""
        pass

    @abstractmethod
    def extract(self, file_path: Path, output_dir: Path) -> List[Path]:
        """Extract files and return list of extracted files."""
        pass

class CustomFormatExtractor(BaseExtractor):
    """Extractor for custom file format."""

    def can_extract(self, file_path: Path) -> bool:
        # Check file signature or extension
        return file_path.suffix.lower() == '.custom'

    def extract(self, file_path: Path, output_dir: Path) -> List[Path]:
        # Custom extraction logic
        extracted_files = []

        # Extract files...
        # extracted_files.append(extracted_path)

        return extracted_files

# Integration
from grindoreiro.extractor import ExtractorManager

manager = ExtractorManager()
manager.register_extractor(CustomFormatExtractor())

# Use in pipeline
class CustomExtractionStep(PipelineStep):
    def __init__(self):
        self.extractor_manager = ExtractorManager()
        self.extractor_manager.register_extractor(CustomFormatExtractor())

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']
        extraction_dir = context['extraction_dir']

        if self.extractor_manager.can_extract(file_path):
            extracted_files = self.extractor_manager.extract(file_path, extraction_dir)
            context['extracted_files'].extend(extracted_files)

        return context
```

### Plugin System

Grindoreiro supports a plugin architecture for extensibility:

```python
# plugins/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class Plugin(ABC):
    """Base plugin class."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin."""
        pass

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the plugin."""
        pass

# plugins/registry.py
class PluginRegistry:
    """Plugin registry for managing plugins."""

    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        self.plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> Plugin:
        """Get a plugin by name."""
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List registered plugins."""
        return list(self.plugins.keys())

    def execute_plugin(self, name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a plugin."""
        plugin = self.get_plugin(name)
        if plugin:
            return plugin.execute(context)
        raise ValueError(f"Plugin {name} not found")

# Usage
registry = PluginRegistry()

# Register plugins
from plugins.custom_plugin import CustomPlugin
registry.register(CustomPlugin())

# Use in pipeline
class PluginStep(PipelineStep):
    def __init__(self, plugin_name: str, registry: PluginRegistry):
        super().__init__(f"PluginStep-{plugin_name}")
        self.plugin_name = plugin_name
        self.registry = registry

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self.registry.execute_plugin(self.plugin_name, context)
```

## 🧪 Testing Architecture

### Unit Testing

```python
# tests/test_pipeline.py
import pytest
from unittest.mock import Mock, patch
from grindoreiro.pipeline import Pipeline
from grindoreiro.core import Config

class TestPipeline:
    def test_pipeline_initialization(self):
        config = Config()
        pipeline = Pipeline(config)

        assert len(pipeline.steps) > 0
        assert all(isinstance(step, PipelineStep) for step in pipeline.steps)

    def test_add_step(self):
        config = Config()
        pipeline = Pipeline(config)

        initial_count = len(pipeline.steps)
        mock_step = Mock()
        pipeline.add_step(mock_step)

        assert len(pipeline.steps) == initial_count + 1
        assert pipeline.steps[-1] == mock_step

    def test_pipeline_execution(self):
        config = Config()
        pipeline = Pipeline(config)

        # Mock all steps
        for step in pipeline.steps:
            step.process = Mock(return_value={'test': 'data'})

        context = {'file_path': '/test/file.zip'}
        result = pipeline.run(context)

        assert 'test' in result
        assert result['test'] == 'data'

    @patch('grindoreiro.pipeline_steps.FileValidationStep')
    def test_step_error_handling(self, mock_validation_step):
        config = Config()
        pipeline = Pipeline(config)

        # Mock step to raise exception
        mock_step = Mock()
        mock_step.process.side_effect = Exception("Test error")
        mock_step.continue_on_error = True
        mock_step.name = "TestStep"

        pipeline.steps = [mock_step]

        context = {'test': 'data'}
        result = pipeline.run(context)

        assert 'error' in result
        assert 'Test error' in result['error']
```

### Integration Testing

```python
# tests/test_integration.py
import pytest
import tempfile
from pathlib import Path
from grindoreiro.processor import Processor
from grindoreiro.core import Config

class TestIntegration:
    def test_full_processing_pipeline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test file
            test_file = Path(temp_dir) / "test.zip"
            # Create a simple ZIP file for testing

            config = Config(
                input_dir=temp_dir,
                output_dir=temp_dir,
                temp_dir=temp_dir
            )

            processor = Processor(config)
            result = processor.process_file(test_file)

            assert result['success'] is True
            assert 'processing_time' in result
            assert result['processing_time'] > 0

    def test_batch_processing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create multiple test files
            test_files = []
            for i in range(3):
                test_file = Path(temp_dir) / f"test_{i}.zip"
                # Create test files
                test_files.append(test_file)

            config = Config(
                input_dir=temp_dir,
                output_dir=temp_dir,
                max_workers=2
            )

            processor = Processor(config)
            results = processor.process_batch(test_files)

            assert len(results) == 3
            assert all(result['success'] for result in results)

    def test_error_handling(self):
        config = Config()
        processor = Processor(config)

        # Test with non-existent file
        result = processor.process_file(Path("/non/existent/file.zip"))

        assert result['success'] is False
        assert 'error' in result
```

### Performance Testing

```python
# tests/test_performance.py
import time
import pytest
from grindoreiro.processor import Processor
from grindoreiro.core import Config

class TestPerformance:
    def test_processing_performance(self, benchmark):
        """Benchmark processing performance."""
        config = Config(max_workers=1)
        processor = Processor(config)

        def process_sample():
            # Create or use a test sample
            test_file = Path("test_sample.zip")
            return processor.process_file(test_file)

        result = benchmark(process_sample)

        assert result['success'] is True
        # Assert performance requirements
        assert result['processing_time'] < 10.0  # Should process in under 10 seconds

    def test_batch_performance(self):
        """Test batch processing performance."""
        config = Config(max_workers=4)
        processor = Processor(config)

        # Create test files
        test_files = [Path(f"sample_{i}.zip") for i in range(10)]

        start_time = time.time()
        results = processor.process_batch(test_files)
        end_time = time.time()

        total_time = end_time - start_time
        avg_time_per_file = total_time / len(test_files)

        assert all(result['success'] for result in results)
        # Assert reasonable performance
        assert avg_time_per_file < 5.0  # Average under 5 seconds per file
```

## 📊 Design Patterns

### Factory Pattern

Used for creating analysis components:

```python
# factories.py
from typing import Dict, Type, Any
from grindoreiro.pipeline_steps import PipelineStep

class StepFactory:
    """Factory for creating pipeline steps."""

    _registry: Dict[str, Type[PipelineStep]] = {}

    @classmethod
    def register(cls, name: str, step_class: Type[PipelineStep]) -> None:
        """Register a step class."""
        cls._registry[name] = step_class

    @classmethod
    def create(cls, name: str, **kwargs) -> PipelineStep:
        """Create a step instance."""
        if name not in cls._registry:
            raise ValueError(f"Unknown step: {name}")

        step_class = cls._registry[name]
        return step_class(**kwargs)

# Usage
StepFactory.register('extraction', ExtractionStep)
StepFactory.register('analysis', AnalysisStep)

step = StepFactory.create('extraction', config={'option': 'value'})
```

### Observer Pattern

Used for event handling and notifications:

```python
# observers.py
from typing import List, Callable, Any
from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface."""

    @abstractmethod
    def update(self, event: str, data: Any) -> None:
        """Handle event update."""
        pass

class Subject:
    """Subject that observers can subscribe to."""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        self._observers.remove(observer)

    def notify(self, event: str, data: Any) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(event, data)

# Usage
class ProcessingNotifier(Subject):
    def __init__(self):
        super().__init__()

    def notify_file_processed(self, file_path: str, result: Dict[str, Any]):
        self.notify('file_processed', {
            'file_path': file_path,
            'result': result
        })

class LogObserver(Observer):
    def update(self, event: str, data: Any):
        if event == 'file_processed':
            print(f"Processed {data['file_path']}: {data['result']['success']}")
```

### Strategy Pattern

Used for interchangeable analysis algorithms:

```python
# strategies.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class AnalysisStrategy(ABC):
    """Strategy interface for analysis methods."""

    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform analysis."""
        pass

class StringAnalysisStrategy(AnalysisStrategy):
    """String-based analysis strategy."""

    def analyze(self, data: bytes) -> Dict[str, Any]:
        strings = extract_strings(data)
        return {
            'type': 'string_analysis',
            'strings_found': len(strings),
            'suspicious_strings': find_suspicious(strings)
        }

class BehavioralAnalysisStrategy(AnalysisStrategy):
    """Behavioral analysis strategy."""

    def analyze(self, data: bytes) -> Dict[str, Any]:
        behavior = analyze_behavior(data)
        return {
            'type': 'behavioral_analysis',
            'behaviors_detected': behavior,
            'risk_score': calculate_risk_score(behavior)
        }

class AnalysisContext:
    """Context that uses analysis strategies."""

    def __init__(self, strategy: AnalysisStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: AnalysisStrategy):
        self.strategy = strategy

    def execute_analysis(self, data: Any) -> Dict[str, Any]:
        return self.strategy.analyze(data)

# Usage
context = AnalysisContext(StringAnalysisStrategy())
result1 = context.execute_analysis(file_data)

context.set_strategy(BehavioralAnalysisStrategy())
result2 = context.execute_analysis(file_data)
```

## 🔧 Best Practices

### Code Organization

1. **Separation of Concerns**: Each module has a single responsibility
2. **Dependency Injection**: Use dependency injection for testability
3. **Interface Segregation**: Keep interfaces small and focused
4. **Open/Closed Principle**: Open for extension, closed for modification

### Error Handling

1. **Graceful Degradation**: Continue processing when non-critical components fail
2. **Detailed Logging**: Log errors with context for debugging
3. **User-Friendly Messages**: Provide clear error messages to users
4. **Recovery Mechanisms**: Implement retry logic where appropriate

### Performance

1. **Lazy Loading**: Load components only when needed
2. **Caching**: Cache expensive operations and results
3. **Async Processing**: Use async for I/O-bound operations
4. **Resource Management**: Properly manage memory and file handles

### Testing

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **Mocking**: Use mocks for external dependencies
4. **Coverage**: Aim for high test coverage

### Documentation

1. **Code Comments**: Document complex logic and algorithms
2. **API Documentation**: Document public interfaces
3. **Architecture Docs**: Keep architecture documentation current
4. **Examples**: Provide usage examples and code samples

---

💡 **Pro Tip**: When extending Grindoreiro, follow the established patterns and ensure new components integrate seamlessly with the existing pipeline system.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\developer-guides\architecture.md
