# Contributing Guide

> How to contribute to Grindoreiro development

## 📦 Overview

Welcome to Grindoreiro! This guide explains how to contribute to the project, whether you're fixing bugs, adding features, improving documentation, or helping with testing.

## 🚀 Getting Started

### Development Environment Setup

1. **Clone the repository**:
```bash
git clone https://github.com/your-org/grindoreiro.git
cd grindoreiro
```

2. **Set up Python environment**:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. **Install pre-commit hooks**:
```bash
pre-commit install
```

4. **Run initial tests**:
```bash
pytest
```

### Project Structure

```
grindoreiro/
├── core/              # Core functionality
├── cli/               # Command-line interface
├── processor/         # Main processing logic
├── pipeline/          # Pipeline orchestration
├── extractor/         # File extraction utilities
├── analyzer/          # Analysis modules
├── scripts/           # Standalone utilities
├── pipeline_steps/    # Processing steps
├── docs/              # Documentation
├── tests/             # Test suite
└── tools/             # Development tools
```

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment information**:
   - Python version
   - Operating system
   - Grindoreiro version
5. **Error messages** and stack traces
6. **Sample files** if applicable (be careful with sensitive data)

**Example bug report**:
```markdown
**Title**: ZIP extraction fails on large files

**Description**:
When processing ZIP files larger than 2GB, the extraction step fails with a MemoryError.

**Steps to reproduce**:
1. Create a ZIP file > 2GB
2. Run `grindoreiro analyze large_file.zip`
3. Observe MemoryError

**Expected behavior**:
Large ZIP files should be extracted without memory issues.

**Environment**:
- Python 3.9.7
- Windows 10
- Grindoreiro 1.0.0

**Error**:
```
MemoryError: Unable to allocate 2.1 GiB for array
```
```

### Feature Requests

For feature requests, include:

1. **Clear description** of the proposed feature
2. **Use case** and why it's needed
3. **Proposed implementation** if you have ideas
4. **Alternatives considered**
5. **Impact assessment** on existing functionality

## 🛠️ Development Workflow

### 1. Choose an Issue

- Check the [issue tracker](https://github.com/your-org/grindoreiro/issues) for open issues
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
# Create and switch to a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-number-description
```

### 3. Make Changes

Follow these guidelines:

- **Write tests first** (TDD approach)
- **Follow coding standards** (black, isort, flake8)
- **Add documentation** for new features
- **Update existing documentation** if needed
- **Keep commits small and focused**

### 4. Write Tests

```python
# tests/test_your_feature.py
import pytest
from grindoreiro.your_module import YourClass

class TestYourFeature:
    def test_basic_functionality(self):
        # Test basic functionality
        pass

    def test_edge_cases(self):
        # Test edge cases
        pass

    def test_error_handling(self):
        # Test error conditions
        pass
```

### 5. Run Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_your_feature.py

# Run with coverage
pytest --cov=grindoreiro --cov-report=html

# Run pre-commit checks
pre-commit run --all-files
```

### 6. Update Documentation

- Update docstrings for new functions/classes
- Add examples to documentation
- Update README if needed
- Add migration notes for breaking changes

### 7. Commit Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add new analysis feature

- Add support for XYZ analysis
- Include comprehensive tests
- Update documentation

Closes #123"
```

**Commit Message Format**:
```
type(scope): description

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

### 8. Create Pull Request

1. **Push your branch**:
```bash
git push origin feature/your-feature-name
```

2. **Create PR on GitHub**:
   - Use descriptive title
   - Reference related issues
   - Provide detailed description
   - Add screenshots/demo if applicable

3. **PR Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes

## Related Issues
Closes #123
```

## 📝 Coding Standards

### Python Style

We use [Black](https://black.readthedocs.io/) for code formatting:

```python
# Good
def process_file(file_path: Path, config: Config) -> Dict[str, Any]:
    """Process a file with given configuration."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    result = {"file_path": str(file_path), "success": True}
    return result

# Avoid
def process_file(file_path,config):
    if not file_path.exists():
        raise FileNotFoundError('File not found: '+str(file_path))
    result={'file_path':str(file_path),'success':True}
    return result
```

### Import Organization

Use [isort](https://pycqa.github.io/isort/) for import sorting:

```python
# Standard library imports
import os
from pathlib import Path
from typing import Dict, Any, List

# Third-party imports
import click
import yaml

# Local imports
from grindoreiro.core import Config
from grindoreiro.pipeline import Pipeline
```

### Type Hints

Use type hints for better code documentation:

```python
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

def process_files(
    file_paths: List[Path],
    config: Config,
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Process multiple files."""
    pass

class FileProcessor:
    def __init__(self, config: Config) -> None:
        self.config = config

    def process(self, file_path: Path) -> Union[Dict[str, Any], None]:
        """Process a single file."""
        pass
```

### Docstrings

Use Google-style docstrings:

```python
def analyze_file(
    file_path: Path,
    config: Config,
    *,
    extract_strings: bool = True,
    calculate_hashes: bool = True
) -> Dict[str, Any]:
    """Analyze a malware sample file.

    Performs comprehensive analysis of a file including string extraction,
    hash calculation, and behavioral analysis.

    Args:
        file_path: Path to the file to analyze.
        config: Analysis configuration.
        extract_strings: Whether to extract strings from the file.
        calculate_hashes: Whether to calculate file hashes.

    Returns:
        Dictionary containing analysis results with the following keys:
        - success: Boolean indicating if analysis succeeded
        - file_info: Basic file information
        - strings: Extracted strings (if extract_strings=True)
        - hashes: File hashes (if calculate_hashes=True)
        - analysis_time: Time taken for analysis

    Raises:
        FileNotFoundError: If the file doesn't exist.
        PermissionError: If unable to read the file.

    Example:
        >>> config = Config()
        >>> result = analyze_file(Path('sample.exe'), config)
        >>> print(result['success'])
        True
    """
    pass
```

## 🧪 Testing Guidelines

### Test Coverage

- Aim for 80%+ code coverage
- Cover happy path and error cases
- Test edge cases and boundary conditions
- Use realistic test data

### Test Structure

```python
# tests/test_file_processor.py
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from grindoreiro.file_processor import FileProcessor

class TestFileProcessor:
    """Test cases for FileProcessor class."""

    @pytest.fixture
    def processor(self, config):
        """Create FileProcessor instance."""
        return FileProcessor(config)

    @pytest.fixture
    def sample_file(self, tmp_path):
        """Create sample file for testing."""
        file_path = tmp_path / "sample.exe"
        file_path.write_bytes(b"MZ\x90\x00")  # Minimal PE header
        return file_path

    def test_process_valid_file(self, processor, sample_file):
        """Test processing a valid file."""
        result = processor.process(sample_file)

        assert result['success'] is True
        assert 'file_info' in result
        assert result['file_info']['size'] > 0

    def test_process_nonexistent_file(self, processor):
        """Test processing a non-existent file."""
        with pytest.raises(FileNotFoundError):
            processor.process(Path("/non/existent/file.exe"))

    def test_process_empty_file(self, processor, tmp_path):
        """Test processing an empty file."""
        empty_file = tmp_path / "empty.exe"
        empty_file.write_bytes(b"")

        result = processor.process(empty_file)

        assert result['success'] is False
        assert 'error' in result

    @patch('grindoreiro.file_processor.hashlib.md5')
    def test_hash_calculation_failure(self, mock_md5, processor, sample_file):
        """Test handling of hash calculation failure."""
        mock_md5.side_effect = Exception("Hash calculation failed")

        result = processor.process(sample_file)

        assert result['success'] is False
        assert 'hash_error' in result
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
from pathlib import Path
from grindoreiro.processor import Processor
from grindoreiro.core import Config

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_analysis_pipeline(self, tmp_path):
        """Test complete analysis pipeline."""
        # Create test file
        test_file = tmp_path / "test.zip"
        # Create test ZIP with malware sample

        config = Config(
            input_dir=str(tmp_path),
            output_dir=str(tmp_path / "output")
        )

        processor = Processor(config)
        result = processor.process_file(test_file)

        # Verify complete pipeline execution
        assert result['success'] is True
        assert 'processing_time' in result
        assert 'extracted_files' in result
        assert 'analysis_results' in result

    def test_batch_processing(self, tmp_path):
        """Test batch processing of multiple files."""
        # Create multiple test files
        test_files = []
        for i in range(5):
            file_path = tmp_path / f"sample_{i}.exe"
            # Create test executable files
            test_files.append(file_path)

        config = Config(max_workers=2)
        processor = Processor(config)

        results = processor.process_batch(test_files)

        assert len(results) == 5
        assert all(r['success'] for r in results)
        assert all('processing_time' in r for r in results)
```

## 📚 Documentation

### Documentation Standards

- Use Markdown for documentation files
- Include code examples where helpful
- Keep documentation up to date
- Use consistent formatting

### API Documentation

```python
# grindoreiro/analyzer.py
class MalwareAnalyzer:
    """Analyzes files for malware indicators.

    This class provides comprehensive malware analysis capabilities
    including signature matching, behavioral analysis, and entropy
    calculation.
    """

    def __init__(self, config: Config):
        """Initialize the analyzer.

        Args:
            config: Analysis configuration object.
        """
        pass

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a file for malware indicators.

        Performs multiple analysis techniques including:
        - File signature checking
        - String extraction and analysis
        - Entropy calculation
        - Behavioral pattern detection

        Args:
            file_path: Path to the file to analyze.

        Returns:
            Dictionary containing analysis results.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            PermissionError: If unable to read the file.
        """
        pass
```

### README Updates

When adding features, update the README:

```markdown
## New Feature: Advanced Entropy Analysis

Grindoreiro now supports advanced entropy analysis for detecting
packed and encrypted malware.

### Usage

```python
from grindoreiro.analyzer import MalwareAnalyzer

analyzer = MalwareAnalyzer()
result = analyzer.analyze_file('sample.exe')

print(f"Entropy: {result['entropy']}")
print(f"Classification: {result['entropy_classification']}")
```
```

## 🔄 Code Review Process

### Review Checklist

**For Reviewers**:
- [ ] Code follows style guidelines
- [ ] Tests are comprehensive and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Code is maintainable

**For Contributors**:
- [ ] Self-review your code
- [ ] Ensure tests pass
- [ ] Update documentation
- [ ] Consider edge cases
- [ ] Follow commit message conventions

### Review Comments

**Good review comments**:
```markdown
✅ **Good**: "Consider using a more descriptive variable name here"
✅ **Good**: "This could benefit from a test case for empty input"
✅ **Good**: "Let's add error handling for this edge case"

❌ **Bad**: "This is wrong"
❌ **Bad**: "Fix this"
❌ **Bad**: "Bad code"
```

### Addressing Feedback

```markdown
# When addressing review feedback
git add .
git commit -m "fix: address review feedback

- Improve variable naming in analyzer.py
- Add test case for empty input
- Add error handling for edge case"
```

## 🚨 Security Considerations

### Security Checklist

- [ ] No hardcoded secrets or credentials
- [ ] Input validation for all user inputs
- [ ] Secure file handling (no path traversal)
- [ ] Safe execution of external commands
- [ ] Proper error message handling (no information leakage)
- [ ] Secure temporary file creation
- [ ] Resource limits (memory, CPU, disk)

### Reporting Security Issues

For security vulnerabilities:

1. **Don't create public issues**
2. **Email maintainers directly** with details
3. **Allow time for fix** before public disclosure
4. **Follow responsible disclosure** practices

## 🎯 Best Practices

### Development

1. **Small, focused commits**
2. **Regular rebasing** on main branch
3. **Clean commit history**
4. **Feature flags** for experimental features
5. **Progressive enhancement**

### Collaboration

1. **Clear communication**
2. **Respectful code reviews**
3. **Help newcomers**
4. **Share knowledge**
5. **Celebrate successes**

### Quality

1. **Test-driven development**
2. **Continuous integration**
3. **Code coverage goals**
4. **Performance monitoring**
5. **Security first**

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check docs first
- **Community**: Join our community channels

### Asking for Help

**Good questions**:
```markdown
I'm trying to add a new analysis step but getting a TypeError.
Here's my code:

```python
# My code here
```

Error:
```
TypeError: 'NoneType' object is not callable
```

What am I doing wrong?
```

**Bad questions**:
```markdown
Help! My code doesn't work. Please fix it.

[500 lines of code]
```

## 🎉 Recognition

Contributors are recognized through:

- **GitHub contributor statistics**
- **Mention in release notes**
- **Contributor spotlight** in documentation
- **Community recognition**

Thank you for contributing to Grindoreiro! Your efforts help make malware analysis better for everyone.

---

💡 **Pro Tip**: Start small with bug fixes or documentation improvements if you're new to the project. This helps you understand the codebase and contribution process before tackling larger features.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\developer-guides\contributing.md
