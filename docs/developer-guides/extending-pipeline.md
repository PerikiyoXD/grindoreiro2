# Extending the Pipeline

> How to add custom analysis steps and extend Grindoreiro's capabilities

## 📦 Overview

Grindoreiro's pipeline system is designed to be extensible, allowing you to add custom analysis steps, extractors, and processing logic. This guide shows how to extend the pipeline with your own components.

## 🛠️ Adding Custom Pipeline Steps

### Basic Pipeline Step

The simplest way to extend Grindoreiro is by creating a custom pipeline step:

```python
# custom_step.py
from pathlib import Path
from typing import Dict, Any
from grindoreiro.pipeline_steps import PipelineStep

class CustomAnalysisStep(PipelineStep):
    """Custom analysis step for malware detection."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CustomAnalysisStep")
        self.config = config or {}

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process the file and add analysis results to context."""

        file_path = context['file_path']

        # Perform your custom analysis
        analysis_result = self._analyze_file(file_path)

        # Add results to context
        context['custom_analysis'] = analysis_result

        return context

    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Perform custom file analysis."""

        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Your analysis logic here
            suspicious_patterns = self._find_suspicious_patterns(file_data)
            entropy_score = self._calculate_entropy(file_data)
            file_type = self._detect_file_type(file_data)

            return {
                'suspicious_patterns': suspicious_patterns,
                'entropy_score': entropy_score,
                'detected_type': file_type,
                'risk_level': self._calculate_risk_level(suspicious_patterns, entropy_score),
                'analysis_time': 0.0  # You can time your analysis
            }

        except Exception as e:
            return {
                'error': str(e),
                'suspicious_patterns': [],
                'entropy_score': 0.0,
                'detected_type': 'unknown',
                'risk_level': 'unknown'
            }

    def _find_suspicious_patterns(self, data: bytes) -> List[str]:
        """Find suspicious patterns in file data."""
        patterns = []

        # Check for common malware signatures
        suspicious_sequences = [
            b'\xE8\x00\x00\x00\x00',  # CALL instruction
            b'\xEB\xFE',              # Infinite loop
            b'\xCC\xCC\xCC\xCC',      # INT 3 breakpoints
        ]

        for seq in suspicious_sequences:
            if seq in data:
                patterns.append(f"Found suspicious sequence: {seq.hex()}")

        return patterns

    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of the data."""
        if not data:
            return 0.0

        from collections import Counter
        import math

        byte_counts = Counter(data)
        data_len = len(data)

        entropy = 0.0
        for count in byte_counts.values():
            probability = count / data_len
            entropy -= probability * math.log2(probability)

        return entropy

    def _detect_file_type(self, data: bytes) -> str:
        """Detect file type from magic bytes."""
        if len(data) < 4:
            return 'unknown'

        # Check magic bytes
        if data.startswith(b'MZ'):
            return 'windows_executable'
        elif data.startswith(b'\x7FELF'):
            return 'elf_executable'
        elif data.startswith(b'PK\x03\x04'):
            return 'zip_archive'
        elif data.startswith(b'%PDF'):
            return 'pdf_document'
        else:
            return 'unknown'

    def _calculate_risk_level(self, patterns: List[str], entropy: float) -> str:
        """Calculate risk level based on analysis."""
        risk_score = len(patterns) * 2

        if entropy > 7.0:
            risk_score += 3  # High entropy often indicates encryption/packing
        elif entropy > 5.0:
            risk_score += 1

        if risk_score >= 5:
            return 'high'
        elif risk_score >= 3:
            return 'medium'
        elif risk_score >= 1:
            return 'low'
        else:
            return 'clean'
```

### Integrating Custom Steps

To use your custom step in the pipeline:

```python
# integrate_custom_step.py
from grindoreiro.pipeline import Pipeline
from grindoreiro.core import Config
from custom_step import CustomAnalysisStep

def create_custom_pipeline():
    """Create a pipeline with custom analysis steps."""

    config = Config()
    pipeline = Pipeline(config)

    # Add your custom step
    custom_config = {
        'sensitivity': 'high',
        'enable_entropy_analysis': True,
        'custom_patterns': ['pattern1', 'pattern2']
    }

    custom_step = CustomAnalysisStep(custom_config)
    pipeline.add_step(custom_step)

    return pipeline

# Usage
pipeline = create_custom_pipeline()

# Process a file
context = {'file_path': Path('malicious_sample.exe')}
result = pipeline.run(context)

print("Custom analysis results:")
print(result.get('custom_analysis', {}))
```

## 🔧 Advanced Pipeline Extensions

### Conditional Processing Steps

Create steps that only execute under certain conditions:

```python
# conditional_step.py
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any, Callable

class ConditionalStep(PipelineStep):
    """Step that only executes if condition is met."""

    def __init__(self, condition: Callable[[Dict[str, Any]], bool], step: PipelineStep):
        super().__init__(f"Conditional-{step.name}")
        self.condition = condition
        self.step = step

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.condition(context):
            return self.step.process(context)
        else:
            # Skip this step
            return context

# Usage
def should_analyze_executable(context: Dict[str, Any]) -> bool:
    """Only analyze if file is an executable."""
    file_path = context['file_path']
    return file_path.suffix.lower() in ['.exe', '.dll', '.scr']

# Wrap existing step with condition
from grindoreiro.pipeline_steps import StringAnalysisStep
conditional_string_analysis = ConditionalStep(
    should_analyze_executable,
    StringAnalysisStep()
)
```

### Parallel Processing Steps

Create steps that process data in parallel:

```python
# parallel_step.py
from concurrent.futures import ThreadPoolExecutor
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any, List

class ParallelAnalysisStep(PipelineStep):
    """Step that performs analysis in parallel."""

    def __init__(self, analysis_functions: List[Callable], max_workers: int = 4):
        super().__init__("ParallelAnalysisStep")
        self.analysis_functions = analysis_functions
        self.max_workers = max_workers

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']

        # Prepare analysis tasks
        tasks = []
        for func in self.analysis_functions:
            tasks.append((func, file_path))

        # Execute in parallel
        results = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_func = {
                executor.submit(self._run_analysis, func, path): func.__name__
                for func, path in tasks
            }

            for future in future_to_func:
                func_name = future_to_func[future]
                try:
                    result = future.result()
                    results[func_name] = result
                except Exception as e:
                    results[func_name] = {'error': str(e)}

        context['parallel_analysis'] = results
        return context

    def _run_analysis(self, analysis_func: Callable, file_path) -> Dict[str, Any]:
        """Run a single analysis function."""
        return analysis_func(file_path)

# Usage
def entropy_analysis(file_path):
    # Entropy analysis implementation
    return {'entropy': 7.2}

def pattern_analysis(file_path):
    # Pattern analysis implementation
    return {'patterns': ['suspicious_1', 'suspicious_2']}

parallel_step = ParallelAnalysisStep([
    entropy_analysis,
    pattern_analysis
])
```

### Composite Steps

Create steps that combine multiple analyses:

```python
# composite_step.py
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any, List

class CompositeStep(PipelineStep):
    """Step that combines multiple sub-steps."""

    def __init__(self, sub_steps: List[PipelineStep], name: str = "CompositeStep"):
        super().__init__(name)
        self.sub_steps = sub_steps

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all sub-steps in sequence."""

        results = {}
        for step in self.sub_steps:
            try:
                context = step.process(context)
                results[step.name] = {'success': True}
            except Exception as e:
                results[step.name] = {
                    'success': False,
                    'error': str(e)
                }
                if not step.continue_on_error:
                    break

        context['composite_results'] = results
        return context

# Usage
from grindoreiro.pipeline_steps import (
    FileValidationStep,
    HashCalculationStep,
    StringAnalysisStep
)

composite_step = CompositeStep([
    FileValidationStep(),
    HashCalculationStep(),
    StringAnalysisStep()
], name="BasicAnalysisComposite")
```

## 📊 Custom Extractors

### Adding New File Format Support

Extend Grindoreiro to handle new archive/compressed formats:

```python
# custom_extractor.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
import logging

class BaseExtractor(ABC):
    """Base class for custom extractors."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def can_extract(self, file_path: Path) -> bool:
        """Check if this extractor can handle the file."""
        pass

    @abstractmethod
    def extract(self, file_path: Path, output_dir: Path) -> List[Path]:
        """Extract files and return list of extracted file paths."""
        pass

class RARExtractor(BaseExtractor):
    """Extractor for RAR archives."""

    def can_extract(self, file_path: Path) -> bool:
        """Check if file is a RAR archive."""
        if file_path.suffix.lower() != '.rar':
            return False

        try:
            with open(file_path, 'rb') as f:
                header = f.read(7)
                return header.startswith(b'Rar!\x1a\x07')
        except:
            return False

    def extract(self, file_path: Path, output_dir: Path) -> List[Path]:
        """Extract RAR archive."""
        try:
            import rarfile

            extracted_files = []

            with rarfile.RarFile(file_path) as rf:
                for file_info in rf.infolist():
                    if not file_info.is_dir():
                        rf.extract(file_info, output_dir)
                        extracted_path = output_dir / file_info.filename
                        if extracted_path.exists():
                            extracted_files.append(extracted_path)

            return extracted_files

        except ImportError:
            self.logger.error("rarfile module not installed")
            raise
        except Exception as e:
            self.logger.error(f"RAR extraction failed: {e}")
            raise

class SevenZipExtractor(BaseExtractor):
    """Extractor for 7-Zip archives."""

    def can_extract(self, file_path: Path) -> bool:
        """Check if file is a 7-Zip archive."""
        if file_path.suffix.lower() not in ['.7z', '.xz', '.bz2']:
            return False

        try:
            with open(file_path, 'rb') as f:
                header = f.read(6)
                return header == b'\x37\x7A\xBC\xAF\x27\x1C'
        except:
            return False

    def extract(self, file_path: Path, output_dir: Path) -> List[Path]:
        """Extract 7-Zip archive."""
        try:
            import py7zr

            extracted_files = []

            with py7zr.SevenZipFile(file_path, mode='r') as zf:
                zf.extractall(output_dir)

                # Get list of extracted files
                for file_info in zf.list():
                    if not file_info.is_dir:
                        extracted_path = output_dir / file_info.filename
                        if extracted_path.exists():
                            extracted_files.append(extracted_path)

            return extracted_files

        except ImportError:
            self.logger.error("py7zr module not installed")
            raise
        except Exception as e:
            self.logger.error(f"7-Zip extraction failed: {e}")
            raise

# Integration with pipeline
class CustomExtractionStep(PipelineStep):
    """Pipeline step that uses custom extractors."""

    def __init__(self):
        super().__init__("CustomExtractionStep")
        self.extractors = [
            RARExtractor(),
            SevenZipExtractor(),
            # Add more extractors here
        ]

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']
        extraction_dir = context.get('extraction_dir')

        if not extraction_dir:
            extraction_dir = file_path.parent / f"{file_path.stem}_extracted"
            extraction_dir.mkdir(exist_ok=True)
            context['extraction_dir'] = extraction_dir

        extracted_files = context.get('extracted_files', [])

        for extractor in self.extractors:
            if extractor.can_extract(file_path):
                try:
                    new_files = extractor.extract(file_path, extraction_dir)
                    extracted_files.extend(new_files)
                    self.logger.info(f"Extracted {len(new_files)} files using {extractor.__class__.__name__}")
                except Exception as e:
                    self.logger.error(f"Extraction failed with {extractor.__class__.__name__}: {e}")

        context['extracted_files'] = extracted_files
        return context
```

## 🔍 Custom Analyzers

### Behavioral Analysis

Create custom behavioral analysis components:

```python
# behavioral_analyzer.py
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any, List
import re

class BehavioralAnalyzer(PipelineStep):
    """Analyze file behavior patterns."""

    def __init__(self):
        super().__init__("BehavioralAnalyzer")
        self.behavior_patterns = self._load_behavior_patterns()

    def _load_behavior_patterns(self) -> Dict[str, List[str]]:
        """Load behavioral analysis patterns."""
        return {
            'persistence': [
                r'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
                r'SCHTASKS\.exe',
                r'REG\.exe ADD',
                r'netsh\.exe',
            ],
            'communication': [
                r'HttpSendRequest',
                r'InternetConnect',
                r'WSASocket',
                r'socket\(\)',
            ],
            'anti_analysis': [
                r'IsDebuggerPresent',
                r'CheckRemoteDebuggerPresent',
                r'VMware|VirtualBox',
                r'Sleep\(\d+\)',
            ],
            'file_operations': [
                r'CreateFile',
                r'WriteFile',
                r'DeleteFile',
                r'MoveFile',
            ],
            'process_manipulation': [
                r'CreateProcess',
                r'OpenProcess',
                r'TerminateProcess',
                r'InjectDll',
            ]
        }

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']

        # Get strings from previous analysis
        strings = context.get('strings', [])

        # Analyze behavior
        behavior_analysis = self._analyze_behavior(strings)

        context['behavior_analysis'] = behavior_analysis
        return context

    def _analyze_behavior(self, strings: List[str]) -> Dict[str, Any]:
        """Analyze behavioral patterns in strings."""

        detected_behaviors = {}
        risk_score = 0

        for category, patterns in self.behavior_patterns.items():
            detected_behaviors[category] = []

            for pattern in patterns:
                matches = []
                for string in strings:
                    if re.search(pattern, string, re.IGNORECASE):
                        matches.append(string)

                if matches:
                    detected_behaviors[category].extend(matches)
                    # Increase risk score based on category
                    risk_multipliers = {
                        'persistence': 3,
                        'communication': 2,
                        'anti_analysis': 2,
                        'file_operations': 1,
                        'process_manipulation': 3
                    }
                    risk_score += len(matches) * risk_multipliers.get(category, 1)

        # Determine risk level
        if risk_score >= 10:
            risk_level = 'high'
        elif risk_score >= 5:
            risk_level = 'medium'
        elif risk_score >= 1:
            risk_level = 'low'
        else:
            risk_level = 'clean'

        return {
            'detected_behaviors': detected_behaviors,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'total_indicators': sum(len(behaviors) for behaviors in detected_behaviors.values())
        }
```

### Signature-Based Analysis

Create custom signature matching:

```python
# signature_analyzer.py
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any, List
import hashlib

class SignatureAnalyzer(PipelineStep):
    """Analyze files against custom signatures."""

    def __init__(self, signature_file: str = None):
        super().__init__("SignatureAnalyzer")
        self.signatures = self._load_signatures(signature_file)

    def _load_signatures(self, signature_file: str = None) -> Dict[str, Dict[str, Any]]:
        """Load signature database."""
        if signature_file:
            # Load from file
            pass

        # Default signatures
        return {
            'trojan_downloader': {
                'hash_md5': 'd41d8cd98f00b204e9800998ecf8427e',
                'description': 'Known trojan downloader',
                'severity': 'high'
            },
            'ransomware_encryptor': {
                'hash_sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                'description': 'Ransomware file encryptor',
                'severity': 'critical'
            }
        }

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']
        file_hashes = context.get('file_hashes', {})

        # Calculate hashes if not already done
        if not file_hashes:
            file_hashes = self._calculate_hashes(file_path)

        # Check against signatures
        matches = self._check_signatures(file_hashes)

        context['signature_matches'] = matches
        context['file_hashes'] = file_hashes

        return context

    def _calculate_hashes(self, file_path) -> Dict[str, str]:
        """Calculate file hashes."""
        hash_md5 = hashlib.md5()
        hash_sha1 = hashlib.sha1()
        hash_sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
                hash_sha1.update(chunk)
                hash_sha256.update(chunk)

        return {
            'md5': hash_md5.hexdigest(),
            'sha1': hash_sha1.hexdigest(),
            'sha256': hash_sha256.hexdigest()
        }

    def _check_signatures(self, file_hashes: Dict[str, str]) -> List[Dict[str, Any]]:
        """Check file hashes against signature database."""
        matches = []

        for signature_name, signature_data in self.signatures.items():
            for hash_type, signature_hash in signature_data.items():
                if hash_type in file_hashes and file_hashes[hash_type] == signature_hash:
                    matches.append({
                        'signature_name': signature_name,
                        'matched_hash_type': hash_type,
                        'matched_hash': signature_hash,
                        'description': signature_data.get('description', ''),
                        'severity': signature_data.get('severity', 'unknown')
                    })

        return matches
```

## 🔌 Plugin System

### Creating Plugins

Grindoreiro supports a plugin architecture for advanced extensions:

```python
# plugins/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class Plugin(ABC):
    """Base plugin interface."""

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

# plugins/machine_learning_plugin.py
import joblib
import numpy as np
from plugins.base import Plugin

class MLAnomalyDetector(Plugin):
    """Machine learning-based anomaly detection plugin."""

    @property
    def name(self) -> str:
        return "ml_anomaly_detector"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the ML model."""
        model_path = config.get('model_path', 'models/anomaly_detector.pkl')
        self.model = joblib.load(model_path)
        self.threshold = config.get('threshold', 0.5)

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute anomaly detection."""
        file_path = context['file_path']

        # Extract features
        features = self._extract_features(file_path)

        # Make prediction
        prediction = self.model.predict_proba([features])[0]
        anomaly_score = prediction[1]  # Probability of being anomalous

        result = {
            'anomaly_score': anomaly_score,
            'is_anomaly': anomaly_score > self.threshold,
            'confidence': abs(anomaly_score - 0.5) * 2  # Confidence in classification
        }

        context['ml_anomaly_detection'] = result
        return context

    def _extract_features(self, file_path) -> np.ndarray:
        """Extract features for ML model."""
        # Feature extraction logic
        features = []

        with open(file_path, 'rb') as f:
            data = f.read()

        # File size
        features.append(len(data))

        # Entropy
        features.append(self._calculate_entropy(data))

        # Byte frequency features
        byte_freq = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
        byte_freq = byte_freq / len(data)  # Normalize
        features.extend(byte_freq)

        return np.array(features)

    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy."""
        if not data:
            return 0.0

        from collections import Counter
        import math

        byte_counts = Counter(data)
        data_len = len(data)

        entropy = 0.0
        for count in byte_counts.values():
            probability = count / data_len
            entropy -= probability * math.log2(probability)

        return entropy

# plugins/registry.py
class PluginRegistry:
    """Registry for managing plugins."""

    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        self.plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> Plugin:
        """Get plugin by name."""
        return self.plugins.get(name)

    def initialize_plugins(self, config: Dict[str, Any]) -> None:
        """Initialize all registered plugins."""
        for plugin in self.plugins.values():
            plugin_config = config.get(plugin.name, {})
            plugin.initialize(plugin_config)

    def execute_plugin(self, name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific plugin."""
        plugin = self.get_plugin(name)
        if plugin:
            return plugin.execute(context)
        raise ValueError(f"Plugin {name} not found")

# Usage
registry = PluginRegistry()
registry.register(MLAnomalyDetector())

# Initialize plugins
config = {
    'ml_anomaly_detector': {
        'model_path': 'models/anomaly_detector.pkl',
        'threshold': 0.7
    }
}
registry.initialize_plugins(config)

# Use in pipeline
class PluginStep(PipelineStep):
    def __init__(self, plugin_name: str, registry: PluginRegistry):
        super().__init__(f"Plugin-{plugin_name}")
        self.plugin_name = plugin_name
        self.registry = registry

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self.registry.execute_plugin(self.plugin_name, context)
```

## 🧪 Testing Custom Extensions

### Unit Testing Custom Steps

```python
# tests/test_custom_step.py
import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from custom_step import CustomAnalysisStep

class TestCustomAnalysisStep:
    def test_step_initialization(self):
        config = {'sensitivity': 'high'}
        step = CustomAnalysisStep(config)

        assert step.name == "CustomAnalysisStep"
        assert step.config == config

    def test_process_success(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b'MZ\x90\x00\x03\x00\x00\x00')

        step = CustomAnalysisStep()
        context = {'file_path': test_file}

        result = step.process(context)

        assert 'custom_analysis' in result
        assert result['custom_analysis']['detected_type'] == 'windows_executable'
        assert 'risk_level' in result['custom_analysis']

    def test_process_file_error(self, tmp_path):
        # Test with non-existent file
        step = CustomAnalysisStep()
        context = {'file_path': Path('/non/existent/file.exe')}

        result = step.process(context)

        assert 'custom_analysis' in result
        assert 'error' in result['custom_analysis']

    @patch('custom_step.CustomAnalysisStep._calculate_entropy')
    def test_entropy_calculation(self, mock_entropy, tmp_path):
        mock_entropy.return_value = 7.5

        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b'test data')

        step = CustomAnalysisStep()
        context = {'file_path': test_file}

        result = step.process(context)

        assert result['custom_analysis']['entropy_score'] == 7.5
        mock_entropy.assert_called_once()
```

### Integration Testing

```python
# tests/test_integration_custom.py
import pytest
from pathlib import Path
from grindoreiro.pipeline import Pipeline
from grindoreiro.core import Config
from custom_step import CustomAnalysisStep

class TestCustomIntegration:
    def test_custom_step_in_pipeline(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b'MZ\x90\x00\x03\x00\x00\x00\xEB\xFE')  # MZ header + infinite loop

        # Create pipeline with custom step
        config = Config()
        pipeline = Pipeline(config)
        pipeline.add_step(CustomAnalysisStep())

        # Process file
        context = {'file_path': test_file}
        result = pipeline.run(context)

        # Verify custom analysis was performed
        assert 'custom_analysis' in result
        custom_result = result['custom_analysis']

        # Should detect Windows executable
        assert custom_result['detected_type'] == 'windows_executable'

        # Should find suspicious pattern (infinite loop)
        assert len(custom_result['suspicious_patterns']) > 0

        # Should have risk assessment
        assert 'risk_level' in custom_result

    def test_multiple_custom_steps(self, tmp_path):
        test_file = tmp_path / "test.exe"
        test_file.write_bytes(b'MZ\x90\x00\x03\x00\x00\x00')

        config = Config()
        pipeline = Pipeline(config)

        # Add multiple custom steps
        pipeline.add_step(CustomAnalysisStep({'analysis_type': 'basic'}))
        pipeline.add_step(CustomAnalysisStep({'analysis_type': 'advanced'}))

        context = {'file_path': test_file}
        result = pipeline.run(context)

        # Should have results from both steps
        assert 'custom_analysis' in result
        # Note: Second step would overwrite first in this simple example
        # In practice, you'd want to handle this differently
```

## 📊 Performance Considerations

### Optimizing Custom Steps

```python
# optimized_step.py
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any
import time
import functools

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        # You could log this or add to context
        result['_execution_time'] = execution_time

        return result
    return wrapper

class OptimizedAnalysisStep(PipelineStep):
    """Optimized analysis step with performance considerations."""

    def __init__(self, use_cache: bool = True, max_file_size: int = 100 * 1024 * 1024):
        super().__init__("OptimizedAnalysisStep")
        self.use_cache = use_cache
        self.max_file_size = max_file_size
        self.cache = {}

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']

        # Check file size
        if file_path.stat().st_size > self.max_file_size:
            context['analysis_skipped'] = f"File too large: {file_path.stat().st_size} bytes"
            return context

        # Check cache
        if self.use_cache:
            cache_key = self._get_cache_key(file_path)
            if cache_key in self.cache:
                context['cached_analysis'] = self.cache[cache_key]
                return context

        # Perform analysis with timing
        analysis_result = self._perform_analysis(file_path)

        # Cache result
        if self.use_cache:
            self.cache[cache_key] = analysis_result

        context['optimized_analysis'] = analysis_result
        return context

    @timing_decorator
    def _perform_analysis(self, file_path: Path) -> Dict[str, Any]:
        """Perform the actual analysis with timing."""
        # Analysis logic here
        return {'result': 'analysis_complete'}

    def _get_cache_key(self, file_path: Path) -> str:
        """Generate cache key for file."""
        stat = file_path.stat()
        return f"{file_path}:{stat.st_size}:{stat.st_mtime}"
```

### Memory Management

```python
# memory_efficient_step.py
from grindoreiro.pipeline_steps import PipelineStep
from typing import Dict, Any
import os
import tempfile

class MemoryEfficientStep(PipelineStep):
    """Step that handles large files efficiently."""

    def __init__(self, chunk_size: int = 8192):
        super().__init__("MemoryEfficientStep")
        self.chunk_size = chunk_size

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_path = context['file_path']

        # For large files, process in chunks
        if file_path.stat().st_size > 100 * 1024 * 1024:  # 100MB
            result = self._process_large_file(file_path)
        else:
            result = self._process_small_file(file_path)

        context['memory_efficient_analysis'] = result
        return context

    def _process_small_file(self, file_path: Path) -> Dict[str, Any]:
        """Process small files by loading entirely into memory."""
        with open(file_path, 'rb') as f:
            data = f.read()

        return self._analyze_data(data)

    def _process_large_file(self, file_path: Path) -> Dict[str, Any]:
        """Process large files by streaming."""
        result = {
            'file_too_large': True,
            'chunks_processed': 0,
            'partial_results': []
        }

        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break

                partial_result = self._analyze_chunk(chunk)
                result['partial_results'].append(partial_result)
                result['chunks_processed'] += 1

        return result

    def _analyze_data(self, data: bytes) -> Dict[str, Any]:
        """Analyze complete data."""
        # Analysis logic
        return {'complete_analysis': True, 'data_size': len(data)}

    def _analyze_chunk(self, chunk: bytes) -> Dict[str, Any]:
        """Analyze a chunk of data."""
        # Partial analysis logic
        return {'chunk_size': len(chunk), 'has_suspicious': b'\xEB\xFE' in chunk}
```

## 🔧 Best Practices

### Extension Development

1. **Follow Conventions**: Use the same patterns as built-in components
2. **Error Handling**: Implement proper error handling and logging
3. **Configuration**: Make components configurable
4. **Documentation**: Document your extensions thoroughly
5. **Testing**: Write comprehensive tests for your extensions

### Performance

1. **Memory Efficiency**: Handle large files appropriately
2. **Caching**: Implement caching for expensive operations
3. **Parallelization**: Use parallel processing when possible
4. **Resource Management**: Clean up resources properly

### Integration

1. **Pipeline Compatibility**: Ensure compatibility with existing pipeline
2. **Context Handling**: Properly handle and update context
3. **Step Ordering**: Consider dependencies between steps
4. **Error Propagation**: Handle errors gracefully without breaking pipeline

### Maintenance

1. **Versioning**: Version your extensions
2. **Backward Compatibility**: Maintain compatibility when updating
3. **Deprecation**: Deprecate old functionality properly
4. **Updates**: Plan for future updates and improvements

---

💡 **Pro Tip**: When creating custom extensions, start with a simple implementation and gradually add complexity. Always test your extensions thoroughly before using them in production.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\developer-guides\extending-pipeline.md
