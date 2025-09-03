#!/usr/bin/env python3
"""Batch analysis of all Grindoreiro samples with parallel processing."""

import sys
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Tuple
from grindoreiro.core import get_logger


def analyze_sample(sample_file: Path) -> Tuple[str, bool, str]:
    """Analyze a single sample and return results."""
    logger = get_logger(__name__)
    sample_name = sample_file.name

    logger.info(f"Analyzing: {sample_name}")
    try:
        # Run analysis with verbose output
        cmd = [sys.executable, "-m", "grindoreiro.cli", str(sample_file), "--verbose"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            logger.info(f"SUCCESS: Successfully analyzed: {sample_name}")
            return sample_name, True, ""
        else:
            logger.error(f"FAILED: Failed to analyze: {sample_name}")
            logger.error(f"Error: {result.stderr}")
            return sample_name, False, result.stderr

    except Exception as e:
        logger.error(f"EXCEPTION: Exception analyzing {sample_name}: {e}")
        return sample_name, False, str(e)


def main():
    """Run batch analysis on all samples with parallel processing."""
    logger = get_logger(__name__)

    samples_dir = Path("./data/samples")
    if not samples_dir.exists():
        logger.error(f"Samples directory not found: {samples_dir}")
        sys.exit(1)

    # Get all ZIP files
    sample_files = list(samples_dir.glob("*.zip"))
    if not sample_files:
        logger.error("No sample files found")
        sys.exit(1)

    logger.info(f"Found {len(sample_files)} samples to analyze")

    # Determine number of concurrent processes (use CPU count or limit to reasonable number)
    import multiprocessing
    max_workers = min(multiprocessing.cpu_count(), len(sample_files), 4)  # Max 4 concurrent processes
    logger.info(f"Using {max_workers} concurrent processes for analysis")

    successful = 0
    failed = 0
    failed_samples = []

    # Run parallel analysis
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all analysis tasks
        future_to_sample = {
            executor.submit(analyze_sample, sample_file): sample_file
            for sample_file in sample_files
        }

        # Process results as they complete
        for future in as_completed(future_to_sample):
            sample_file = future_to_sample[future]
            try:
                sample_name, success, error_msg = future.result()
                if success:
                    successful += 1
                else:
                    failed += 1
                    failed_samples.append((sample_name, error_msg))
            except Exception as e:
                logger.error(f"Exception processing {sample_file.name}: {e}")
                failed += 1
                failed_samples.append((sample_file.name, str(e)))

    logger.info(f"Batch analysis completed: {successful} successful, {failed} failed")

    # Report failed samples
    if failed_samples:
        logger.warning("Failed samples:")
        for sample_name, error in failed_samples:
            logger.warning(f"  - {sample_name}: {error}")

    if successful > 0:
        logger.info("Running false negative analysis...")
        # Run the false negative analyzer
        cmd = [sys.executable, "batch_false_negative_analyzer.py"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            logger.info("False negative analysis completed")
        else:
            logger.error("False negative analysis failed")
            logger.error(result.stderr)


if __name__ == "__main__":
    main()
