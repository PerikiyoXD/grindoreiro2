"""Grindoreiro - Malware Analysis Toolkit for Grandoreiro Samples.

This package provides tools to analyze and unpack Grandoreiro malware samples,
including ZIP extraction, MSI decompilation, string analysis, and ISO decoding.
"""

__version__ = "1.0.0"
__author__ = "PerikiyoXD"
__description__ = "Malware analysis toolkit for Grandoreiro samples"

# Import main components for easy access
from .core import config, setup_logging, get_logger
from .processor import GrandoreiroProcessor
from .extractor import FileExtractor
from .analyzer import StringExtractor, URLAnalyzer
from .iso_handler import ISODownloader
from .pipeline import AnalysisPipeline, PipelineContext, ResultsManager

__all__ = [
    "config",
    "setup_logging",
    "get_logger",
    "GrandoreiroProcessor",
    "FileExtractor",
    "StringExtractor",
    "URLAnalyzer",
    "ISODownloader",
    "AnalysisPipeline",
    "PipelineContext",
    "ResultsManager",
]
