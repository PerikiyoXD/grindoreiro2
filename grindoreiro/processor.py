"""Main processor for Grandoreiro sample analysis."""

from pathlib import Path
from typing import Optional
import logging

from .core import get_logger, config
from .pipeline import AnalysisPipeline, PipelineContext, ResultsManager
from .pipeline_steps import (
    InitializeStep,
    ExtractZipStep,
    ExtractMsiStep,
    ExtractDllStep,
    AnalyzeStringsStep,
    AnalyzeUrlsStep,
    ProcessIsoStep,
    FinalizeStep
)


logger = get_logger(__name__)


class GrandoreiroProcessor:
    """Main processor for Grandoreiro malware analysis."""

    def __init__(self, dark_path: Optional[Path] = None):
        """Initialize processor with dependencies."""
        self.config = config
        self.logger = logger
        self.dark_path = dark_path or self.config.dark_path

        # Initialize pipeline
        self.pipeline = AnalysisPipeline()
        self._setup_pipeline()

        # Initialize results manager
        self.results_manager = ResultsManager(self.config.output_dir)

        # Initialize results manager
        self.results_manager = ResultsManager(self.config.output_dir)

    def _setup_pipeline(self) -> None:
        """Setup the analysis pipeline with all steps."""
        self.pipeline.add_step(InitializeStep())
        self.pipeline.add_step(ExtractZipStep(self.dark_path))
        self.pipeline.add_step(ExtractMsiStep(self.dark_path))
        self.pipeline.add_step(ExtractDllStep(self.dark_path))
        self.pipeline.add_step(AnalyzeStringsStep())
        self.pipeline.add_step(AnalyzeUrlsStep())
        self.pipeline.add_step(ProcessIsoStep(self.dark_path))
        self.pipeline.add_step(FinalizeStep())

    def process_sample(self, sample_path: str, keep_temp: bool = False) -> None:
        """Process a Grandoreiro sample file using the pipeline."""
        sample_file = Path(sample_path)

        if not sample_file.exists():
            raise FileNotFoundError(f"Sample file not found: {sample_file}")

        self.logger.info(f"Processing sample: {sample_file.name}")

        # Create pipeline context
        context = PipelineContext(sample_file)

        try:
            # Execute pipeline
            metadata = self.pipeline.execute(context)

            # Save results
            results_file = self.results_manager.save_metadata(metadata)
            self.logger.info(f"Analysis results saved to: {results_file}")

            # Generate and display report
            report = self.results_manager.generate_report(metadata)
            print("\n" + report)

            # Handle cleanup based on success/failure and keep_temp flag
            if keep_temp:
                # Create debug marker to prevent cleanup
                from .core import create_session_debug_marker
                debug_file = create_session_debug_marker(context.session_id, "keep_temp=True specified")
                self.logger.info(f"Keeping temp files for manual analysis. Debug marker: {debug_file}")
                self.logger.info(f"Session temp directory: {context.temp_dir}")
            else:
                # Check if analysis was successful before cleanup
                successful_stages = sum(1 for stage in metadata.stages if stage.success)
                total_stages = len(metadata.stages)

                if successful_stages == total_stages:
                    # Successful analysis - cleanup temp files
                    from .core import cleanup_session_temp_dir
                    cleanup_session_temp_dir(context.session_id)
                    self.logger.info(f"Cleaned up temporary files for session: {context.session_id}")
                else:
                    # Failed analysis - keep temp files for troubleshooting
                    from .core import create_session_debug_marker
                    debug_file = create_session_debug_marker(
                        context.session_id,
                        f"Analysis failed: {successful_stages}/{total_stages} stages successful"
                    )
                    self.logger.warning(f"Keeping temp files for troubleshooting failed analysis. Debug marker: {debug_file}")
                    self.logger.warning(f"Session temp directory: {context.temp_dir}")

            self.logger.info("Processing complete!")

        except Exception as e:
            # On exception, always keep temp files for debugging
            from .core import create_session_debug_marker
            try:
                debug_file = create_session_debug_marker(context.session_id, f"Exception during processing: {e}")
                self.logger.error(f"Processing failed, keeping temp files for debugging. Debug marker: {debug_file}")
                self.logger.error(f"Session temp directory: {context.temp_dir}")
            except:
                pass
            raise
