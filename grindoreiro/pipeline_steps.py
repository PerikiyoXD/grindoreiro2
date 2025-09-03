"""Concrete pipeline steps for Grandoreiro analysis."""

from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import time

from .pipeline import PipelineStep, PipelineContext, PipelineStage, StageResult, StageStatus
from .extractor import FileExtractor
from .analyzer import StringExtractor, URLAnalyzer
from .iso_handler import ISODownloader
from .core import get_logger, FileHash, generate_session_id, get_session_temp_dir, calculate_file_sha256, config, ensure_directory


logger = get_logger(__name__)


class InitializeStep(PipelineStep):
    """Initialize the analysis context and create working directories."""

    def __init__(self):
        super().__init__("initialize")

    def can_execute(self, context: PipelineContext) -> bool:
        return True

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            # Sample hash is already calculated in PipelineContext
            sample_hash = context.metadata.sha256_hash

            # Create working directory structure in temp
            work_dir = context.temp_dir / "processing"
            context.work_dir = work_dir
            ensure_directory(work_dir)

            step_dirs = {
                'extract': work_dir / "extract",
                'msi_output': work_dir / "msi_output",
                'msi_script': work_dir / "msi_script",
                'dll': work_dir / "dll",
                'iso': work_dir / "iso",
                'exe': work_dir / "exe"
            }

            for step_dir in step_dirs.values():
                ensure_directory(step_dir)

            metadata = {
                "sample_hash": sample_hash,
                "work_dir": str(work_dir),
                "temp_dir": str(context.temp_dir),
                "step_dirs": {k: str(v) for k, v in step_dirs.items()},
                "session_id": context.session_id
            }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.INITIALIZE,
                success=True,
                metadata=metadata,
                duration=duration
            )

        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.INITIALIZE,
                success=False,
                error_message=str(e),
                duration=duration
            )


class ExtractZipStep(PipelineStep):
    """Extract the ZIP file containing the MSI."""

    def __init__(self, dark_path: Optional[Path] = None):
        super().__init__("extract_zip")
        self.extractor = FileExtractor(dark_path)

    def can_execute(self, context: PipelineContext) -> bool:
        init_result = context.get_stage_result(PipelineStage.INITIALIZE)
        return init_result and init_result.success

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            step_dirs = context.get_stage_result(PipelineStage.INITIALIZE).metadata["step_dirs"]
            extract_dir = Path(step_dirs["extract"])

            self.extractor.extract_zip(context.sample_path, extract_dir)

            # Collect extracted files metadata and hashes
            extracted_files = []
            for file_path in extract_dir.rglob("*"):
                if file_path.is_file():
                    file_hash = FileHash.from_file(file_path, "extracted")
                    context.metadata.file_hashes[f"extracted_{file_path.name}"] = file_hash
                    extracted_files.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "sha256": file_hash.sha256
                    })

            context.metadata.extracted_files = extracted_files

            metadata = {
                "extracted_files_count": len(extracted_files),
                "extract_dir": str(extract_dir)
            }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.EXTRACT_ZIP,
                success=True,
                metadata=metadata,
                artifacts=[extract_dir],
                duration=duration
            )

        except Exception as e:
            logger.error(f"ZIP extraction failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.EXTRACT_ZIP,
                success=False,
                error_message=str(e),
                duration=duration
            )


class ExtractMsiStep(PipelineStep):
    """Extract the MSI file using WiX dark.exe."""

    def __init__(self, dark_path: Optional[Path] = None):
        super().__init__("extract_msi")
        self.extractor = FileExtractor(dark_path)

    def can_execute(self, context: PipelineContext) -> bool:
        zip_result = context.get_stage_result(PipelineStage.EXTRACT_ZIP)
        return zip_result and zip_result.success

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            step_dirs = context.get_stage_result(PipelineStage.INITIALIZE).metadata["step_dirs"]
            extract_dir = Path(step_dirs["extract"])
            msi_output_dir = Path(step_dirs["msi_output"])
            msi_script_dir = Path(step_dirs["msi_script"])

            # Find MSI file
            msi_file = self.extractor.find_msi_file(extract_dir)
            if not msi_file:
                raise FileNotFoundError("No MSI file found in extracted ZIP")

            # Extract MSI
            self.extractor.extract_msi(msi_file, msi_output_dir, msi_script_dir)

            # Collect MSI metadata and hash
            msi_hash = FileHash.from_file(msi_file, "msi")
            context.metadata.file_hashes["msi"] = msi_hash

            msi_info = {
                "msi_path": str(msi_file),
                "msi_size": msi_file.stat().st_size,
                "msi_sha256": msi_hash.sha256,
                "output_dir": str(msi_output_dir),
                "script_dir": str(msi_script_dir)
            }
            context.metadata.msi_info = msi_info

            metadata = {
                "msi_file": str(msi_file),
                "msi_size": msi_file.stat().st_size,
                "msi_sha256": msi_hash.sha256
            }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.EXTRACT_MSI,
                success=True,
                metadata=metadata,
                artifacts=[msi_output_dir, msi_script_dir],
                duration=duration
            )

        except Exception as e:
            logger.error(f"MSI extraction failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.EXTRACT_MSI,
                success=False,
                error_message=str(e),
                duration=duration
            )


class ExtractDllStep(PipelineStep):
    """Extract and copy the DLL file."""

    def __init__(self, dark_path: Optional[Path] = None):
        super().__init__("extract_dll")
        self.extractor = FileExtractor(dark_path)

    def can_execute(self, context: PipelineContext) -> bool:
        msi_result = context.get_stage_result(PipelineStage.EXTRACT_MSI)
        return msi_result and msi_result.success

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            step_dirs = context.get_stage_result(PipelineStage.INITIALIZE).metadata["step_dirs"]
            msi_output_dir = Path(step_dirs["msi_output"])
            dll_dir = Path(step_dirs["dll"])

            # Find DLL files
            dll_files = self.extractor.find_dll_files(
                msi_output_dir,
                exclude_patterns=['aicustact']
            )

            if not dll_files:
                raise FileNotFoundError("No suitable DLL file found")

            dll_file = dll_files[0]  # Take first DLL
            dll_copy = dll_dir / dll_file.name

            self.extractor.copy_file(dll_file, dll_copy)

            # Collect DLL metadata and hash
            dll_hash = FileHash.from_file(dll_file, "dll")
            context.metadata.file_hashes["dll"] = dll_hash

            dll_info = {
                "original_path": str(dll_file),
                "copied_path": str(dll_copy),
                "size": dll_file.stat().st_size,
                "name": dll_file.name,
                "sha256": dll_hash.sha256
            }
            context.metadata.dll_info = dll_info

            metadata = {
                "dll_file": str(dll_file),
                "dll_copy": str(dll_copy),
                "dll_size": dll_file.stat().st_size,
                "dll_sha256": dll_hash.sha256
            }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.EXTRACT_DLL,
                success=True,
                metadata=metadata,
                artifacts=[dll_copy],
                duration=duration
            )

        except Exception as e:
            logger.error(f"DLL extraction failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.EXTRACT_DLL,
                success=False,
                error_message=str(e),
                duration=duration
            )


class AnalyzeStringsStep(PipelineStep):
    """Extract strings from the DLL file."""

    def __init__(self):
        super().__init__("analyze_strings")
        self.string_extractor = StringExtractor()

    def can_execute(self, context: PipelineContext) -> bool:
        dll_result = context.get_stage_result(PipelineStage.EXTRACT_DLL)
        return dll_result and dll_result.success

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            dll_result = context.get_stage_result(PipelineStage.EXTRACT_DLL)
            dll_copy = Path(dll_result.metadata["dll_copy"])

            strings = self.string_extractor.extract_strings(dll_copy)
            context.metadata.strings_count = len(strings)

            metadata = {
                "strings_count": len(strings),
                "strings_file": str(dll_copy.with_suffix(f"{dll_copy.suffix}.strings")),
                "strings": strings  # Store strings for potential use by other components
            }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.ANALYZE_STRINGS,
                success=True,
                metadata=metadata,
                duration=duration
            )

        except Exception as e:
            logger.error(f"String analysis failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.ANALYZE_STRINGS,
                success=False,
                error_message=str(e),
                duration=duration
            )


class AnalyzeUrlsStep(PipelineStep):
    """Analyze strings for URLs."""

    def __init__(self):
        super().__init__("analyze_urls")
        self.url_analyzer = URLAnalyzer()
        self.string_extractor = StringExtractor()

    def can_execute(self, context: PipelineContext) -> bool:
        strings_result = context.get_stage_result(PipelineStage.ANALYZE_STRINGS)
        return strings_result and strings_result.success

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            strings_result = context.get_stage_result(PipelineStage.ANALYZE_STRINGS)
            strings = strings_result.metadata.get("strings", [])

            if not strings:
                # Fallback to reading from file
                strings_file = Path(strings_result.metadata["strings_file"])
                with open(strings_file, "r", encoding='utf-8') as f:
                    strings = [line.strip() for line in f if line.strip()]

            urls = self.url_analyzer.find_urls(strings)

            context.metadata.urls_found = list(urls)

            # Find C&C URL
            cnc_url = self.url_analyzer.find_cnc_url(urls)
            if cnc_url:
                context.metadata.cnc_url = cnc_url

            # Find download URL
            download_url = self.url_analyzer.find_download_url(urls)
            if download_url:
                context.metadata.download_url = download_url

            metadata = {
                "urls_count": len(urls),
                "cnc_url": cnc_url,
                "download_url": download_url
            }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.ANALYZE_URLS,
                success=True,
                metadata=metadata,
                duration=duration
            )

        except Exception as e:
            logger.error(f"URL analysis failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.ANALYZE_URLS,
                success=False,
                error_message=str(e),
                duration=duration
            )


class ProcessIsoStep(PipelineStep):
    """Download and process ISO file."""

    def __init__(self, dark_path: Optional[Path] = None):
        super().__init__("process_iso")
        self.iso_downloader = ISODownloader()
        self.extractor = FileExtractor(dark_path)

    def can_execute(self, context: PipelineContext) -> bool:
        urls_result = context.get_stage_result(PipelineStage.ANALYZE_URLS)
        return urls_result and urls_result.success and context.metadata.download_url

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            step_dirs = context.get_stage_result(PipelineStage.INITIALIZE).metadata["step_dirs"]
            iso_dir = Path(step_dirs["iso"])
            exe_dir = Path(step_dirs["exe"])

            download_url = context.metadata.download_url

            # Check for cached ISO using proper cache system
            from .core import get_cache_path
            cached_iso = get_cache_path(download_url)

            if cached_iso.exists():
                logger.info("Using cached ISO file")
                iso_path = cached_iso
                # Copy to working directory
                work_iso_path = iso_dir / cached_iso.name
                self.extractor.copy_file(cached_iso, work_iso_path)
                iso_path = work_iso_path
            else:
                # Download ISO
                iso_path = self.iso_downloader.download_iso(download_url, iso_dir)
                # Cache the downloaded file
                self.extractor.copy_file(iso_path, cached_iso)

            # Capture ISO hash
            iso_hash = FileHash.from_file(iso_path, "iso")
            context.metadata.file_hashes["iso"] = iso_hash

            # Decode ISO
            zip_path = self.iso_downloader.decode_iso(iso_path, iso_dir)

            # Capture decoded ZIP hash
            zip_hash = FileHash.from_file(zip_path, "decoded_zip")
            context.metadata.file_hashes["decoded_zip"] = zip_hash

            # Extract decoded ZIP
            self.extractor.extract_zip(zip_path, exe_dir)

            # Find and copy executable
            exe_files = self.extractor.find_files_by_extension(exe_dir, "exe")
            if exe_files:
                exe_file = exe_files[0]
                output_path = config.output_dir / exe_file.name
                self.extractor.copy_file(exe_file, output_path)

                # Capture executable hash
                exe_hash = FileHash.from_file(exe_file, "executable")
                context.metadata.file_hashes["executable"] = exe_hash

                metadata = {
                    "iso_path": str(iso_path),
                    "iso_sha256": iso_hash.sha256,
                    "decoded_zip": str(zip_path),
                    "decoded_zip_sha256": zip_hash.sha256,
                    "exe_file": str(exe_file),
                    "exe_sha256": exe_hash.sha256,
                    "output_path": str(output_path)
                }
            else:
                metadata = {
                    "iso_path": str(iso_path),
                    "iso_sha256": iso_hash.sha256,
                    "decoded_zip": str(zip_path),
                    "decoded_zip_sha256": zip_hash.sha256,
                    "exe_file": None,
                    "output_path": None
                }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.PROCESS_ISO,
                success=True,
                metadata=metadata,
                duration=duration
            )

        except Exception as e:
            logger.error(f"ISO processing failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.PROCESS_ISO,
                success=False,
                error_message=str(e),
                duration=duration
            )


class FinalizeStep(PipelineStep):
    """Finalize the analysis and generate summary."""

    def __init__(self):
        super().__init__("finalize")

    def can_execute(self, context: PipelineContext) -> bool:
        return True  # Always can finalize

    def execute(self, context: PipelineContext) -> StageResult:
        start_time = time.time()

        try:
            # Update network status based on results
            if context.metadata.download_url:
                context.metadata.network_status = {
                    "iso_download_attempted": True,
                    "iso_download_success": any(
                        stage.stage == PipelineStage.PROCESS_ISO and stage.success
                        for stage in context.metadata.stages
                    )
                }
            else:
                context.metadata.network_status = {
                    "iso_download_attempted": False,
                    "iso_download_success": False
                }

            metadata = {
                "total_stages": len(context.metadata.stages),
                "successful_stages": sum(1 for stage in context.metadata.stages if stage.success),
                "network_status": context.metadata.network_status
            }

            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.FINALIZE,
                success=True,
                metadata=metadata,
                duration=duration
            )

        except Exception as e:
            logger.error(f"Finalization failed: {e}")
            duration = time.time() - start_time
            return self.create_result(
                PipelineStage.FINALIZE,
                success=False,
                error_message=str(e),
                duration=duration
            )
