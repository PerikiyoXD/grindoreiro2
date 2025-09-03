#!/usr/bin/env python3
"""Batch processor for multiple Grandoreiro samples."""

import subprocess
import sys
from pathlib import Path
from typing import List
import time

def run_analysis(sample_path: str) -> bool:
    """Run analysis on a single sample."""
    print(f"\n🔍 Processing: {sample_path}")
    print("-" * 60)

    try:
        # Run the analysis
        cmd = [sys.executable, "-m", "grindoreiro.cli", sample_path, "--verbose"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

        if result.returncode == 0:
            print(f"✅ SUCCESS: {sample_path}")
            return True
        else:
            print(f"❌ FAILED: {sample_path}")
            print(f"Exit code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[-500:]}")  # Last 500 chars of error
            return False

    except Exception as e:
        print(f"❌ ERROR: {sample_path} - {e}")
        return False

def main():
    """Main batch processing function."""
    print("🚀 BATCH MALWARE ANALYSIS STARTING")
    print("=" * 60)
    print("⚠️  SECURITY REMINDERS:")
    print("   - This analyzes actual malware samples")
    print("   - C&C servers may be contacted (if active)")
    print("   - Analysis is performed in isolated environment")
    print("   - No executables will be automatically run")
    print("=" * 60)

    # Get all samples
    samples_dir = Path("data/samples")
    all_samples = sorted([f for f in samples_dir.glob("*.zip")])

    # Skip already processed sample
    processed_sample = "0001.zip"
    samples_to_process = [s for s in all_samples if s.name != processed_sample]

    print(f"📊 Processing {len(samples_to_process)} samples (skipping {processed_sample})")
    print()

    # Process each sample
    results = []
    start_time = time.time()

    for i, sample in enumerate(samples_to_process, 1):
        print(f"[{i}/{len(samples_to_process)}] ", end="")
        success = run_analysis(str(sample))
        results.append((sample.name, success))

        # Small delay between samples
        time.sleep(1)

    # Summary
    total_time = time.time() - start_time
    successful = sum(1 for _, success in results if success)
    failed = len(results) - successful

    print("\n" + "=" * 60)
    print("📊 BATCH ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    if len(results) > 0:
        print(f"📈 Success rate: {successful/len(results)*100:.1f}%")
    else:
        print("📈 Success rate: N/A (no samples processed)")

    if failed > 0:
        print("\n❌ Failed samples:")
        for name, success in results:
            if not success:
                print(f"   - {name}")

    print("\n🎯 Analysis complete! Check the data/output/ directory for results.")

if __name__ == "__main__":
    main()
