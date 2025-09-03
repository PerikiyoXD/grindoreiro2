#!/usr/bin/env python3
"""Batch analysis and false negative detection for Grindoreiro samples."""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from grindoreiro.core import get_logger


@dataclass
class AnalysisResult:
    """Analysis result for a sample."""
    sample_name: str
    json_path: Path  # Added to store the full path to the JSON file
    detected: bool
    threat_level: str
    malware_family: str
    analysis_time: float
    stages_successful: int
    total_stages: int
    dll_found: bool
    urls_found: int
    strings_extracted: int
    iso_download_attempted: bool
    errors: List[str]


def analyze_sample_result(json_file: Path) -> AnalysisResult:
    """Analyze a single sample's JSON result."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        sample_name = data.get('sample_name', json_file.stem.replace('_analysis', ''))

        # Check if malware was detected
        detected = False
        threat_level = "UNKNOWN"
        malware_family = "Unknown"

        # Check both possible locations for results
        if 'assessment' in data:
            assessment = data['assessment']
            threat_level = assessment.get('threat_level', 'UNKNOWN').upper()
            malware_family = assessment.get('malware_family', 'Unknown')

            # Consider it detected if:
            # 1. Threat level is HIGH/MEDIUM/LOW, OR
            # 2. A DLL was found and strings were extracted (indicating successful analysis)
            dll_found = 'dll' in data.get('file_analysis', {}).get('file_hashes', {})
            strings_count = data.get('content_analysis', {}).get('strings_count', 0)

            detected = (threat_level in ['HIGH', 'MEDIUM', 'LOW'] and malware_family != 'Unknown') or \
                      (dll_found and strings_count > 0)
        elif 'analysis_results' in data:
            results = data['analysis_results']
            if isinstance(results, dict):
                threat_level = results.get('threat_level', 'UNKNOWN')
                malware_family = results.get('malware_family', 'Unknown')
                detected = threat_level in ['HIGH', 'MEDIUM', 'LOW'] and malware_family != 'Unknown'

        # Extract other metrics
        analysis_time = data.get('analysis_time', 0)
        stages_info = data.get('stages_completed', '0/0')
        if '/' in str(stages_info):
            stages_successful, total_stages = map(int, str(stages_info).split('/'))
        else:
            stages_successful = total_stages = 0

        dll_found = 'dll_sha256' in data.get('file_hashes', {})
        urls_found = data.get('analysis_results', {}).get('urls_found', 0) if isinstance(data.get('analysis_results'), dict) else 0
        strings_extracted = data.get('analysis_results', {}).get('strings_extracted', 0) if isinstance(data.get('analysis_results'), dict) else 0

        # Check for ISO download attempts
        iso_download_attempted = False
        if 'pipeline_steps' in data:
            for step in data['pipeline_steps']:
                if step.get('step') == 'process_iso' and step.get('status') == 'completed':
                    iso_download_attempted = True
                    break

        # Collect errors
        errors = []
        if 'pipeline_steps' in data:
            for step in data['pipeline_steps']:
                if step.get('status') == 'failed':
                    errors.append(f"{step.get('step')}: {step.get('error', 'Unknown error')}")

        return AnalysisResult(
            sample_name=sample_name,
            json_path=json_file,  # Store the full path
            detected=detected,
            threat_level=threat_level,
            malware_family=malware_family,
            analysis_time=analysis_time,
            stages_successful=stages_successful,
            total_stages=total_stages,
            dll_found=dll_found,
            urls_found=urls_found,
            strings_extracted=strings_extracted,
            iso_download_attempted=iso_download_attempted,
            errors=errors
        )

    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error analyzing {json_file}: {e}")
        return AnalysisResult(
            sample_name=json_file.stem.replace('_analysis', ''),
            json_path=json_file,  # Store the full path even on error
            detected=False,
            threat_level="ERROR",
            malware_family="Error",
            analysis_time=0,
            stages_successful=0,
            total_stages=0,
            dll_found=False,
            urls_found=0,
            strings_extracted=0,
            iso_download_attempted=False,
            errors=[str(e)]
        )


def batch_analyze_results(output_dir: Path) -> Dict[str, Any]:
    """Analyze all JSON results and identify false negatives."""
    logger = get_logger(__name__)

    # Find all JSON analysis files
    json_files = list(output_dir.glob("*_analysis.json"))

    if not json_files:
        logger.warning(f"No analysis files found in {output_dir}")
        return {}

    logger.info(f"Found {len(json_files)} analysis files")

    results = {}
    false_negatives = []
    successful_detections = []
    analysis_errors = []

    for json_file in sorted(json_files):
        result = analyze_sample_result(json_file)
        results[result.sample_name] = result

        if result.threat_level == "ERROR":
            analysis_errors.append(result)
        elif result.detected:
            successful_detections.append(result)
        else:
            false_negatives.append(result)

    # Generate summary
    summary = {
        'total_samples': len(results),
        'successful_detections': len(successful_detections),
        'false_negatives': len(false_negatives),
        'analysis_errors': len(analysis_errors),
        'detection_rate': len(successful_detections) / len(results) * 100 if results else 0,
        'false_negative_rate': len(false_negatives) / len(results) * 100 if results else 0,
        'results': results,
        'false_negatives_list': false_negatives,
        'successful_detections_list': successful_detections,
        'analysis_errors_list': analysis_errors
    }

    return summary


def print_analysis_summary(summary: Dict[str, Any]) -> None:
    """Print a comprehensive analysis summary."""
    print("=" * 80)
    print("GRINDOREIRO BATCH ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Total Samples Analyzed: {summary['total_samples']}")
    print(f"Successful Detections: {summary['successful_detections']}")
    print(f"False Negatives: {summary['false_negatives']}")
    print(f"Analysis Errors: {summary['analysis_errors']}")
    print(".1f")
    print(".1f")
    print()

    if summary['false_negatives_list']:
        print("FALSE NEGATIVES DETECTED:")
        print("-" * 40)
        for fn in summary['false_negatives_list']:
            print(f"[FALSE NEGATIVE] {fn.sample_name}")
            print(f"   Full Path: {fn.json_path}")  # Print full path to temp session
            print(f"   Threat Level: {fn.threat_level}")
            print(f"   Malware Family: {fn.malware_family}")
            print(f"   DLL Found: {'YES' if fn.dll_found else 'NO'}")
            print(f"   URLs Found: {fn.urls_found}")
            print(f"   Strings Extracted: {fn.strings_extracted}")
            print(f"   Stages: {fn.stages_successful}/{fn.total_stages}")
            if fn.errors:
                print(f"   Errors: {len(fn.errors)}")
                for error in fn.errors[:2]:  # Show first 2 errors
                    print(f"     - {error}")
            print()

    # Skip printing successful detections

    if summary['analysis_errors_list']:
        print("ANALYSIS ERRORS:")
        print("-" * 40)
        for ae in summary['analysis_errors_list']:
            print(f"[ERROR] {ae.sample_name}")
            print(f"   Full Path: {ae.json_path}")  # Print full path for errors too
            if ae.errors:
                for error in ae.errors[:2]:
                    print(f"   Error: {error}")
            print()


def generate_false_negative_report(summary: Dict[str, Any], output_file: Path) -> None:
    """Generate a detailed HTML report for false negatives."""
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grindoreiro False Negative Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #007bff;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .metric-label {{
            color: #666;
            margin-top: 5px;
        }}
        .false-negatives {{
            margin-top: 30px;
        }}
        .sample-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            background: #fff;
        }}
        .sample-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .sample-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #dc3545;
        }}
        .status-badge {{
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        .false-negative {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .detection {{
            background-color: #d4edda;
            color: #155724;
        }}
        .error {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-bottom: 15px;
        }}
        .metric {{
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
        .metric small {{
            display: block;
            color: #666;
            margin-top: 5px;
        }}
        .errors {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }}
        .error-item {{
            color: #721c24;
            margin-bottom: 5px;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Grindoreiro False Negative Analysis Report</h1>
            <p>Comprehensive analysis of malware detection accuracy</p>
        </div>

        <div class="summary-grid">
            <div class="metric-card">
                <div class="metric-value">{summary['total_samples']}</div>
                <div class="metric-label">Total Samples</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['successful_detections']}</div>
                <div class="metric-label">Detections</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #dc3545;">{summary['false_negatives']}</div>
                <div class="metric-label">False Negatives</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #ffc107;">{summary['analysis_errors']}</div>
                <div class="metric-label">Analysis Errors</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['detection_rate']:.1f}%</div>
                <div class="metric-label">Detection Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #dc3545;">{summary['false_negative_rate']:.1f}%</div>
                <div class="metric-label">False Negative Rate</div>
            </div>
        </div>

        <div class="false-negatives">
            <h2>False Negatives ({len(summary['false_negatives_list'])})</h2>
"""

    for fn in summary['false_negatives_list']:
        html_content += f"""
            <div class="sample-card">
                <div class="sample-header">
                    <span class="sample-name">{fn.sample_name}</span>
                    <span class="status-badge false-negative">FALSE NEGATIVE</span>
                </div>
                <div class="metrics">
                    <div class="metric">
                        {fn.json_path}
                        <small>Full Path</small>
                    </div>
                    <div class="metric">
                        {fn.threat_level}
                        <small>Threat Level</small>
                    </div>
                    <div class="metric">
                        {fn.malware_family}
                        <small>Malware Family</small>
                    </div>
                    <div class="metric">
                        {'YES' if fn.dll_found else 'NO'}
                        <small>DLL Found</small>
                    </div>
                    <div class="metric">
                        {fn.urls_found}
                        <small>URLs Found</small>
                    </div>
                    <div class="metric">
                        {fn.strings_extracted:,}
                        <small>Strings</small>
                    </div>
                    <div class="metric">
                        {fn.stages_successful}/{fn.total_stages}
                        <small>Stages</small>
                    </div>
                </div>
"""
        if fn.errors:
            html_content += """
                <div class="errors">
                    <strong>Errors:</strong>
"""
            for error in fn.errors:
                html_content += f"""
                    <div class="error-item">• {error}</div>
"""
            html_content += """
                </div>
"""
        html_content += """
            </div>
"""

    # Skip successful detections section

    html_content += f"""
        <div class="timestamp">
            Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"False negative report generated: {output_file}")


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Batch analysis and false negative detection")
    parser.add_argument("--output-dir", type=Path, default=Path("./data/output"),
                       help="Directory containing analysis results")
    parser.add_argument("--report-file", type=Path,
                       default=Path("./data/output/false_negative_analysis.html"),
                       help="Output file for HTML report")

    args = parser.parse_args()

    logger = get_logger(__name__)
    logger.info("Starting batch analysis and false negative detection")

    # Analyze all results
    summary = batch_analyze_results(args.output_dir)

    if not summary:
        logger.error("No analysis results found")
        sys.exit(1)

    # Print summary to console
    print_analysis_summary(summary)

    # Generate HTML report
    generate_false_negative_report(summary, args.report_file)

    logger.info("Batch analysis completed")


if __name__ == "__main__":
    main()
