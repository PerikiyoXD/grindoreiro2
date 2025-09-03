"""Pipeline architecture for Grandoreiro analysis."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging
import json

from .core import get_logger, FileHash, generate_session_id, get_session_temp_dir, calculate_file_sha256


logger = get_logger(__name__)


class PipelineStage(Enum):
    """Pipeline processing stages."""
    INITIALIZE = "initialize"
    EXTRACT_ZIP = "extract_zip"
    EXTRACT_MSI = "extract_msi"
    EXTRACT_DLL = "extract_dll"
    ANALYZE_STRINGS = "analyze_strings"
    ANALYZE_URLS = "analyze_urls"
    PROCESS_ISO = "process_iso"
    FINALIZE = "finalize"


class StageStatus(Enum):
    """Status of a pipeline stage."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StageResult:
    """Result of a pipeline stage execution."""
    stage: PipelineStage
    status: StageStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[Path] = field(default_factory=list)


@dataclass
class SampleMetadata:
    """Comprehensive metadata for a sample."""
    sample_path: Path
    sample_name: str
    sample_size: int
    sha256_hash: str
    analysis_start: datetime
    analysis_end: Optional[datetime] = None
    total_duration: Optional[float] = None

    # Session information
    session_id: str = ""

    # File information
    extracted_files: List[Dict[str, Any]] = field(default_factory=list)
    file_hashes: Dict[str, FileHash] = field(default_factory=dict)
    msi_info: Optional[Dict[str, Any]] = None
    dll_info: Optional[Dict[str, Any]] = None

    # Analysis results
    strings_count: int = 0
    urls_found: List[str] = field(default_factory=list)
    cnc_url: Optional[str] = None
    download_url: Optional[str] = None

    # Network analysis
    network_status: Dict[str, Any] = field(default_factory=dict)

    # Processing stages
    stages: List[StageResult] = field(default_factory=list)

    # Final assessment
    threat_level: str = "unknown"
    malware_family: str = "unknown"
    analysis_summary: str = ""


class PipelineContext:
    """Context for pipeline execution."""

    def __init__(self, sample_path: Union[str, Path]):
        self.sample_path = Path(sample_path)
        self.session_id = generate_session_id()
        self.temp_dir = get_session_temp_dir(self.session_id)
        self.work_dir: Optional[Path] = None

        # Calculate sample hash
        with open(self.sample_path, "rb") as f:
            sample_data = f.read()
        sample_hash = calculate_file_sha256(self.sample_path)

        self.metadata = SampleMetadata(
            sample_path=self.sample_path,
            sample_name=self.sample_path.name,
            sample_size=self.sample_path.stat().st_size,
            sha256_hash=sample_hash,
            analysis_start=datetime.now(),
            session_id=self.session_id
        )

        # Add sample file hash
        self.metadata.file_hashes["sample"] = FileHash.from_file(
            self.sample_path, "sample_zip"
        )

        self.stage_results: List[StageResult] = []
        self.logger = logger

        # Log session information for troubleshooting
        self.logger.info(f"Session {self.session_id} initialized")
        self.logger.info(f"Temp directory: {self.temp_dir}")
        self.logger.info(f"Sample: {self.sample_path} ({self.sample_path.stat().st_size} bytes)")
        self.logger.info(f"Sample SHA256: {sample_hash}")

    def add_stage_result(self, result: StageResult) -> None:
        """Add a stage result to the context."""
        self.stage_results.append(result)
        self.metadata.stages.append(result)

    def get_stage_result(self, stage: PipelineStage) -> Optional[StageResult]:
        """Get result for a specific stage."""
        for result in self.stage_results:
            if result.stage == stage:
                return result
        return None

    def update_metadata(self, **kwargs) -> None:
        """Update metadata with new information."""
        for key, value in kwargs.items():
            if hasattr(self.metadata, key):
                setattr(self.metadata, key, value)

    def mark_completed(self) -> None:
        """Mark the analysis as completed."""
        self.metadata.analysis_end = datetime.now()
        if self.metadata.analysis_end and self.metadata.analysis_start:
            self.metadata.total_duration = (
                self.metadata.analysis_end - self.metadata.analysis_start
            ).total_seconds()


class PipelineStep(ABC):
    """Abstract base class for pipeline steps."""

    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"pipeline.{name}")

    @abstractmethod
    def execute(self, context: PipelineContext) -> StageResult:
        """Execute the pipeline step."""
        pass

    @abstractmethod
    def can_execute(self, context: PipelineContext) -> bool:
        """Check if this step can be executed."""
        pass

    def create_result(self, stage: PipelineStage, success: bool = False,
                     error_message: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None,
                     artifacts: Optional[List[Path]] = None,
                     duration: Optional[float] = None) -> StageResult:
        """Create a stage result."""
        start_time = datetime.now()
        end_time = start_time
        if duration:
            # If duration is provided, calculate end_time from start_time + duration
            from datetime import timedelta
            end_time = start_time + timedelta(seconds=duration)

        return StageResult(
            stage=stage,
            status=StageStatus.COMPLETED if success else StageStatus.FAILED,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            success=success,
            error_message=error_message,
            metadata=metadata or {},
            artifacts=artifacts or []
        )


class AnalysisPipeline:
    """Main analysis pipeline."""

    def __init__(self):
        self.steps: List[PipelineStep] = []
        self.logger = logger

    def add_step(self, step: PipelineStep) -> None:
        """Add a step to the pipeline."""
        self.steps.append(step)

    def execute(self, context: PipelineContext) -> SampleMetadata:
        """Execute the entire pipeline."""
        self.logger.info(f"Starting pipeline execution for {context.sample_path}")

        try:
            for step in self.steps:
                if step.can_execute(context):
                    self.logger.info(f"Executing step: {step.name}")
                    result = step.execute(context)
                    context.add_stage_result(result)

                    if not result.success and result.stage != PipelineStage.PROCESS_ISO:
                        # ISO processing can fail due to network issues, but other steps should succeed
                        self.logger.error(f"Step {step.name} failed: {result.error_message}")
                        break
                else:
                    self.logger.info(f"Skipping step: {step.name}")

            context.mark_completed()
            self._generate_summary(context)

        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {e}")
            context.metadata.analysis_summary = f"Pipeline failed: {e}"

        return context.metadata

    def _generate_summary(self, context: PipelineContext) -> None:
        """Generate analysis summary."""
        metadata = context.metadata

        # Count successful stages
        successful_stages = sum(1 for stage in metadata.stages if stage.success)

        # Determine threat assessment
        if metadata.dll_info and metadata.urls_found:
            metadata.threat_level = "high"
            metadata.malware_family = "Grandoreiro"
        elif metadata.urls_found:
            metadata.threat_level = "medium"
            metadata.malware_family = "Suspicious"
        else:
            metadata.threat_level = "low"
            metadata.malware_family = "Unknown"

        # Generate summary
        summary_parts = [
            f"Analysis completed in {metadata.total_duration:.1f}s",
            f"{successful_stages}/{len(metadata.stages)} stages successful",
            f"Threat level: {metadata.threat_level}",
            f"Malware family: {metadata.malware_family}"
        ]

        if metadata.cnc_url:
            summary_parts.append(f"C&C server identified: {metadata.cnc_url}")

        metadata.analysis_summary = " | ".join(summary_parts)


class ResultsManager:
    """Manages analysis results and reporting."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

    def save_metadata(self, metadata: SampleMetadata, format: str = "json") -> Path:
        """Save metadata to file."""
        if format == "json":
            return self._save_json(metadata)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _save_json(self, metadata: SampleMetadata) -> Path:
        """Save metadata as JSON."""
        # Convert metadata to dictionary
        data = {
            "sample_info": {
                "name": metadata.sample_name,
                "path": str(metadata.sample_path),
                "size": metadata.sample_size,
                "sha256": metadata.sha256_hash
            },
            "session_info": {
                "session_id": metadata.session_id,
                "analysis_start": metadata.analysis_start.isoformat(),
                "analysis_end": metadata.analysis_end.isoformat() if metadata.analysis_end else None,
                "total_duration": metadata.total_duration
            },
            "file_analysis": {
                "extracted_files": metadata.extracted_files,
                "msi_info": metadata.msi_info,
                "dll_info": metadata.dll_info,
                "file_hashes": {
                    key: {
                        "path": str(fh.path),
                        "sha256": fh.sha256,
                        "size": fh.size,
                        "file_type": fh.file_type,
                        "modified_time": fh.modified_time.isoformat() if fh.modified_time else None
                    }
                    for key, fh in metadata.file_hashes.items()
                }
            },
            "content_analysis": {
                "strings_count": metadata.strings_count,
                "urls_found": metadata.urls_found,
                "cnc_url": metadata.cnc_url,
                "download_url": metadata.download_url
            },
            "network_analysis": metadata.network_status,
            "processing_stages": [
                {
                    "stage": stage.stage.value,
                    "status": stage.status.value,
                    "success": stage.success,
                    "duration": stage.duration,
                    "error_message": stage.error_message,
                    "metadata": stage.metadata,
                    "artifacts": [str(artifact) for artifact in stage.artifacts]
                }
                for stage in metadata.stages
            ],
            "assessment": {
                "threat_level": metadata.threat_level,
                "malware_family": metadata.malware_family,
                "summary": metadata.analysis_summary
            }
        }

        output_file = self.output_dir / f"{metadata.sample_name}_analysis.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return output_file

    def generate_report(self, metadata: SampleMetadata) -> str:
        """Generate a human-readable report."""
        report_lines = [
            "=" * 60,
            f"MALWARE ANALYSIS REPORT",
            "=" * 60,
            f"Sample: {metadata.sample_name}",
            f"SHA256: {metadata.sha256_hash}",
            f"Size: {metadata.sample_size:,} bytes",
            f"Session ID: {metadata.session_id}",
            f"Analysis Time: {metadata.total_duration:.1f}s" if metadata.total_duration else "Analysis Time: N/A",
            "",
            "FILE HASHES:",
            "-" * 15
        ]

        # Add file hashes
        for key, file_hash in metadata.file_hashes.items():
            report_lines.append(f"{key.upper()}: {file_hash.sha256}")

        report_lines.extend([
            "",
            "ANALYSIS RESULTS:",
            "-" * 20
        ])

        if metadata.dll_info:
            report_lines.extend([
                f"Malware DLL: {metadata.dll_info.get('name', 'Unknown')}",
                f"DLL Size: {metadata.dll_info.get('size', 0):,} bytes",
                f"DLL SHA256: {metadata.dll_info.get('sha256', 'N/A')}"
            ])

        if metadata.strings_count > 0:
            report_lines.append(f"Strings Extracted: {metadata.strings_count:,}")

        if metadata.urls_found:
            report_lines.append(f"URLs Found: {len(metadata.urls_found)}")

        if metadata.cnc_url:
            report_lines.append(f"C&C Server: {metadata.cnc_url}")

        if metadata.download_url:
            report_lines.append(f"Download URL: {metadata.download_url}")

        report_lines.extend([
            "",
            "THREAT ASSESSMENT:",
            "-" * 20,
            f"Threat Level: {metadata.threat_level.upper()}",
            f"Malware Family: {metadata.malware_family}",
            "",
            "SUMMARY:",
            "-" * 10,
            metadata.analysis_summary,
            "=" * 60
        ])

        return "\n".join(report_lines)
