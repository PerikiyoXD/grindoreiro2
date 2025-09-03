#!/usr/bin/env python3
"""Consolidated HTML Report Generator for Grindoreiro Analysis Results."""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64
import hashlib
from collections import defaultdict


class ConsolidatedHTMLReportGenerator:
    """Consolidated HTML report generator with deduplication and enhanced features."""

    def __init__(self):
        self.css_styles = self._get_css_styles()
        self.js_scripts = self._get_js_scripts()

    def _get_css_styles(self) -> str:
        """Get comprehensive CSS styles for the report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }

        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }

        .header .subtitle {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 20px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .info-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }

        .info-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }

        .info-card p {
            color: #666;
            font-size: 0.9em;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-success { background: #d4edda; color: #155724; }
        .status-warning { background: #fff3cd; color: #856404; }
        .status-danger { background: #f8d7da; color: #721c24; }
        .status-info { background: #d1ecf1; color: #0c5460; }

        .section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }

        .hash-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .hash-item {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #28a745;
        }

        .hash-item .hash-type {
            font-weight: bold;
            color: #28a745;
            text-transform: uppercase;
            font-size: 0.9em;
            margin-bottom: 5px;
        }

        .hash-item .hash-value {
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #666;
            word-break: break-all;
            cursor: pointer;
        }

        .file-list {
            margin-top: 20px;
        }

        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
        }

        .file-item:hover {
            background: #f8f9fa;
        }

        .file-info {
            flex: 1;
        }

        .file-name {
            font-weight: bold;
            color: #333;
        }

        .file-details {
            color: #666;
            font-size: 0.9em;
            margin-top: 2px;
        }

        .file-hash {
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            color: #28a745;
            margin-top: 2px;
        }

        .file-size {
            color: #007bff;
            font-weight: bold;
        }

        .timeline {
            position: relative;
            padding-left: 30px;
        }

        .timeline-item {
            position: relative;
            padding: 15px 0;
            border-left: 2px solid #667eea;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: -6px;
            top: 20px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #667eea;
        }

        .timeline-item:last-child {
            border-left: none;
        }

        .timeline-item h4 {
            color: #667eea;
            margin-bottom: 5px;
        }

        .timeline-item .time {
            color: #666;
            font-size: 0.9em;
        }

        .timeline-item .status {
            margin-top: 5px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .stat-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
        }

        .url-list {
            margin-top: 20px;
        }

        .url-item {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }

        .url-item .url {
            font-family: 'Courier New', monospace;
            color: #856404;
            word-break: break-all;
        }

        .assessment {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
        }

        .assessment h2 {
            color: white;
            margin-bottom: 20px;
        }

        .threat-level {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .threat-description {
            font-size: 1.2em;
            margin-bottom: 20px;
        }

        .summary {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            font-style: italic;
        }

        .footer {
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 0.9em;
        }

        .tab-container {
            margin-top: 20px;
        }

        .tab-buttons {
            display: flex;
            background: #f8f9fa;
            border-radius: 10px 10px 0 0;
            overflow: hidden;
        }

        .tab-button {
            flex: 1;
            padding: 15px;
            border: none;
            background: transparent;
            cursor: pointer;
            font-weight: bold;
            color: #666;
            transition: all 0.3s;
        }

        .tab-button.active {
            background: #667eea;
            color: white;
        }

        .tab-button:hover {
            background: #5a67d8;
            color: white;
        }

        .tab-content {
            background: white;
            border-radius: 0 0 10px 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }

        .tab-pane {
            display: none;
        }

        .tab-pane.active {
            display: block;
        }

        .search-container {
            margin-bottom: 20px;
        }

        .search-input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }

        .duplicate-notice {
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 15px;
            color: #004085;
        }

        .duplicate-group {
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
            overflow: hidden;
        }

        .duplicate-header {
            background: #f8f9fa;
            padding: 10px;
            font-weight: bold;
            cursor: pointer;
            border-bottom: 1px solid #ddd;
        }

        .duplicate-content {
            padding: 10px;
            display: none;
        }

        .duplicate-content.show {
            display: block;
        }

        .export-buttons {
            margin-bottom: 20px;
            text-align: right;
        }

        .export-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px;
        }

        .export-btn:hover {
            background: #218838;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            .header {
                padding: 20px;
            }

            .header h1 {
                font-size: 2em;
            }

            .section {
                padding: 20px;
            }

            .info-grid {
                grid-template-columns: 1fr;
            }

            .hash-grid {
                grid-template-columns: 1fr;
            }

            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        """

    def _get_js_scripts(self) -> str:
        """Get JavaScript for interactive features."""
        return """
        function switchTab(tabName) {
            // Hide all tab panes
            const tabPanes = document.querySelectorAll('.tab-pane');
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Remove active class from all tab buttons
            const tabButtons = document.querySelectorAll('.tab-button');
            tabButtons.forEach(button => button.classList.remove('active'));

            // Show selected tab pane
            document.getElementById(tabName).classList.add('active');

            // Add active class to clicked button
            event.target.classList.add('active');
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                showNotification('Copied to clipboard!', 'success');
            });
        }

        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? '#28a745' : '#dc3545'};
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                z-index: 1000;
                font-weight: bold;
            `;
            document.body.appendChild(notification);
            setTimeout(() => document.body.removeChild(notification), 2000);
        }

        function filterItems(searchTerm, containerId) {
            const container = document.getElementById(containerId);
            const items = container.querySelectorAll('.file-item, .url-item, .hash-item');
            const term = searchTerm.toLowerCase();

            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(term)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function toggleDuplicateGroup(header) {
            const content = header.nextElementSibling;
            content.classList.toggle('show');
            header.textContent = header.textContent.replace(
                content.classList.contains('show') ? '▶' : '▼',
                content.classList.contains('show') ? '▼' : '▶'
            );
        }

        function exportToJSON() {
            const data = {
                timestamp: new Date().toISOString(),
                reportData: window.reportData || {}
            };
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'analysis_report.json';
            a.click();
            URL.revokeObjectURL(url);
        }

        function exportToCSV() {
            // Simple CSV export of key findings
            let csv = 'Type,Value,Details\\n';
            const urls = document.querySelectorAll('.url-item .url');
            urls.forEach(url => {
                csv += `URL,${url.textContent},Found in analysis\\n`;
            });
            const hashes = document.querySelectorAll('.hash-value');
            hashes.forEach(hash => {
                csv += `Hash,${hash.textContent},File hash\\n`;
            });

            const blob = new Blob([csv], {type: 'text/csv'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'analysis_findings.csv';
            a.click();
            URL.revokeObjectURL(url);
        }

        // Initialize first tab as active
        document.addEventListener('DOMContentLoaded', function() {
            const firstTab = document.querySelector('.tab-button');
            const firstPane = document.querySelector('.tab-pane');
            if (firstTab && firstPane) {
                firstTab.classList.add('active');
                firstPane.classList.add('active');
            }
        });
        """

    def _deduplicate_urls(self, urls: List[str]) -> Dict[str, List[str]]:
        """Deduplicate URLs and group similar ones."""
        if not urls:
            return {}

        # Group URLs by domain
        domain_groups = defaultdict(list)
        for url in urls:
            try:
                # Extract domain (simplified)
                if '://' in url:
                    domain = url.split('://')[1].split('/')[0]
                else:
                    domain = url.split('/')[0]
                domain_groups[domain].append(url)
            except:
                domain_groups['other'].append(url)

        # Remove duplicates within groups
        deduplicated = {}
        for domain, url_list in domain_groups.items():
            unique_urls = list(set(url_list))
            if len(unique_urls) > 1:
                deduplicated[f"{domain} ({len(unique_urls)} variants)"] = unique_urls
            else:
                deduplicated[domain] = unique_urls

        return deduplicated

    def _deduplicate_files(self, files: List[Dict]) -> Dict[str, List[Dict]]:
        """Deduplicate files by hash and group similar ones."""
        if not files:
            return {}

        # Group by hash
        hash_groups = defaultdict(list)
        for file_info in files:
            hash_val = file_info.get('sha256', 'unknown')
            hash_groups[hash_val].append(file_info)

        # Group duplicates
        deduplicated = {}
        for hash_val, file_list in hash_groups.items():
            if len(file_list) > 1:
                deduplicated[f"Duplicate files ({len(file_list)} instances)"] = file_list
            else:
                deduplicated[file_list[0]['name']] = file_list

        return deduplicated

    def generate_report(self, json_data: Dict[str, Any]) -> str:
        """Generate HTML report from JSON data."""
        self.sample_info = json_data.get('sample_info', {})
        self.session_info = json_data.get('session_info', {})
        self.file_analysis = json_data.get('file_analysis', {})
        self.content_analysis = json_data.get('content_analysis', {})
        self.network_analysis = json_data.get('network_analysis', {})
        self.processing_stages = json_data.get('processing_stages', [])
        self.assessment = json_data.get('assessment', {})

        # Deduplicate data
        deduplicated_urls = self._deduplicate_urls(self.content_analysis.get('urls_found', []))
        deduplicated_files = self._deduplicate_files(self.file_analysis.get('extracted_files', []))

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Malware Analysis Report - {self.sample_info.get('name', 'Unknown')}</title>
    <style>{self.css_styles}</style>
</head>
<body>
    <div class="container">
        {self._generate_header(self.sample_info, self.session_info)}
        {self._generate_overview(self.file_analysis, self.content_analysis)}
        {self._generate_tabs(deduplicated_files, deduplicated_urls, self.processing_stages, self.content_analysis)}
        {self._generate_statistics(self.content_analysis, self.processing_stages)}
        {self._generate_assessment(self.assessment)}
        {self._generate_footer()}
    </div>

    <script>
        window.reportData = {json.dumps(json_data, indent=2)};
        {self.js_scripts}
    </script>
</body>
</html>
        """
        return html

    def _generate_header(self, sample_info: Dict, session_info: Dict) -> str:
        """Generate header section."""
        sample_name = sample_info.get('name', 'Unknown')
        sample_size = sample_info.get('size', 0)
        sha256 = sample_info.get('sha256', 'N/A')
        session_id = session_info.get('session_id', 'N/A')
        duration = session_info.get('total_duration', 0)

        return f"""
        <div class="header">
            <h1>🔍 Malware Analysis Report</h1>
            <div class="subtitle">Comprehensive analysis of {sample_name}</div>

            <div class="export-buttons">
                <button class="export-btn" onclick="exportToJSON()">Export JSON</button>
                <button class="export-btn" onclick="exportToCSV()">Export CSV</button>
            </div>

            <div class="info-grid">
                <div class="info-card">
                    <h3>📁 Sample Information</h3>
                    <p><strong>Name:</strong> {sample_name}</p>
                    <p><strong>Size:</strong> {sample_size:,} bytes</p>
                    <p><strong>SHA256:</strong> <span onclick="copyToClipboard('{sha256}')" style="cursor: pointer; text-decoration: underline;">{sha256[:16]}...</span></p>
                </div>

                <div class="info-card">
                    <h3>⏱️ Analysis Details</h3>
                    <p><strong>Session ID:</strong> {session_id}</p>
                    <p><strong>Duration:</strong> {duration:.2f} seconds</p>
                    <p><strong>Analysis Time:</strong> {session_info.get('analysis_start', 'N/A')}</p>
                </div>

                <div class="info-card">
                    <h3>🎯 Quick Status</h3>
                    <p><strong>Files Processed:</strong> {len(self.file_analysis.get('extracted_files', []))}</p>
                    <p><strong>URLs Found:</strong> {len(self.content_analysis.get('urls_found', []))}</p>
                    <p><strong>Strings:</strong> {self.content_analysis.get('strings_count', 0):,}</p>
                </div>
            </div>
        </div>
        """

    def _generate_overview(self, file_analysis: Dict, content_analysis: Dict) -> str:
        """Generate overview section."""
        msi_info = file_analysis.get('msi_info')
        dll_info = file_analysis.get('dll_info')

        overview_items = []

        if msi_info:
            overview_items.append(f"""
            <div class="info-card">
                <h3>📦 MSI Analysis</h3>
                <p><strong>MSI File:</strong> {Path(msi_info.get('msi_path', '')).name}</p>
                <p><strong>Size:</strong> {msi_info.get('msi_size', 0):,} bytes</p>
                <p><strong>SHA256:</strong> {msi_info.get('msi_sha256', 'N/A')[:16]}...</p>
            </div>
            """)

        if dll_info:
            overview_items.append(f"""
            <div class="info-card">
                <h3>🔧 DLL Analysis</h3>
                <p><strong>DLL File:</strong> {dll_info.get('name', 'N/A')}</p>
                <p><strong>Size:</strong> {dll_info.get('size', 0):,} bytes</p>
                <p><strong>SHA256:</strong> {dll_info.get('sha256', 'N/A')[:16]}...</p>
            </div>
            """)

        if content_analysis.get('cnc_url'):
            overview_items.append(f"""
            <div class="info-card">
                <h3>🌐 C&C Server</h3>
                <p><strong>URL:</strong> {content_analysis.get('cnc_url')}</p>
                <p><strong>Status:</strong> <span class="status-badge status-danger">MALICIOUS</span></p>
            </div>
            """)

        return f"""
        <div class="section">
            <h2>📊 Analysis Overview</h2>
            <div class="info-grid">
                {''.join(overview_items)}
            </div>
        </div>
        """

    def _generate_tabs(self, deduplicated_files: Dict, deduplicated_urls: Dict, processing_stages: List[Dict], content_analysis: Dict) -> str:
        """Generate tabbed content section."""
        return f"""
        <div class="section">
            <h2>📋 Detailed Analysis</h2>
            <div class="tab-container">
                <div class="tab-buttons">
                    <button class="tab-button" onclick="switchTab('files')">Files</button>
                    <button class="tab-button" onclick="switchTab('urls')">URLs</button>
                    <button class="tab-button" onclick="switchTab('timeline')">Timeline</button>
                    <button class="tab-button" onclick="switchTab('strings')">Strings</button>
                </div>

                <div class="tab-content">
                    <div id="files" class="tab-pane">
                        {self._generate_files_tab(deduplicated_files)}
                    </div>
                    <div id="urls" class="tab-pane">
                        {self._generate_urls_tab(deduplicated_urls)}
                    </div>
                    <div id="timeline" class="tab-pane">
                        {self._generate_timeline_tab(processing_stages)}
                    </div>
                    <div id="strings" class="tab-pane">
                        {self._generate_strings_tab(content_analysis)}
                    </div>
                </div>
            </div>
        </div>
        """

    def _generate_files_tab(self, deduplicated_files: Dict) -> str:
        """Generate files tab content."""
        if not deduplicated_files:
            return "<p>No files found in analysis.</p>"

        content = '<div class="search-container"><input type="text" class="search-input" placeholder="Search files..." onkeyup="filterItems(this.value, \'files-container\')"></div>'
        content += '<div id="files-container">'

        for group_name, files in deduplicated_files.items():
            if len(files) > 1:
                content += f'<div class="duplicate-notice">⚠️ Found {len(files)} duplicate files with same hash</div>'
                content += f'<div class="duplicate-group">'
                content += f'<div class="duplicate-header" onclick="toggleDuplicateGroup(this)">▶ {group_name}</div>'
                content += '<div class="duplicate-content">'

                for file_info in files:
                    content += f"""
                    <div class="file-item">
                        <div class="file-info">
                            <div class="file-name">{file_info.get('name', 'Unknown')}</div>
                            <div class="file-details">Path: {file_info.get('path', 'N/A')}</div>
                            <div class="file-hash">SHA256: {file_info.get('sha256', 'N/A')[:32]}...</div>
                        </div>
                        <div class="file-size">{file_info.get('size', 0):,} bytes</div>
                    </div>
                    """
                content += '</div></div>'
            else:
                file_info = files[0]
                content += f"""
                <div class="file-item">
                    <div class="file-info">
                        <div class="file-name">{file_info.get('name', 'Unknown')}</div>
                        <div class="file-details">Path: {file_info.get('path', 'N/A')}</div>
                        <div class="file-hash">SHA256: {file_info.get('sha256', 'N/A')[:32]}...</div>
                    </div>
                    <div class="file-size">{file_info.get('size', 0):,} bytes</div>
                </div>
                """

        content += '</div>'
        return content

    def _generate_urls_tab(self, deduplicated_urls: Dict) -> str:
        """Generate URLs tab content."""
        if not deduplicated_urls:
            return "<p>No URLs found in analysis.</p>"

        content = '<div class="search-container"><input type="text" class="search-input" placeholder="Search URLs..." onkeyup="filterItems(this.value, \'urls-container\')"></div>'
        content += '<div id="urls-container">'

        for domain, urls in deduplicated_urls.items():
            if len(urls) > 1:
                content += f'<div class="duplicate-notice">📋 {domain}</div>'
                for url in urls:
                    content += f"""
                    <div class="url-item">
                        <div class="url">{url}</div>
                    </div>
                    """
            else:
                url = urls[0]
                content += f"""
                <div class="url-item">
                    <div class="url">{url}</div>
                </div>
                """

        content += '</div>'
        return content

    def _generate_timeline_tab(self, processing_stages: List[Dict]) -> str:
        """Generate timeline tab content."""
        if not processing_stages:
            return "<p>No processing stages recorded.</p>"

        content = '<div class="timeline">'
        for stage in processing_stages:
            status_class = "status-info"
            if stage.get('success'):
                status_class = "status-success"
            elif stage.get('error_message'):
                status_class = "status-danger"

            content += f"""
            <div class="timeline-item">
                <h4>{stage.get('stage', 'unknown').replace('_', ' ').title()}</h4>
                <div class="time">Duration: {stage.get('duration', 0):.3f}s</div>
                <div class="status">
                    <span class="status-badge {status_class}">
                        {'SUCCESS' if stage.get('success') else 'FAILED'}
                    </span>
                </div>
                {f'<div style="color: #721c24; margin-top: 5px;">{stage.get("error_message")}</div>' if stage.get('error_message') else ''}
            </div>
            """
        content += '</div>'
        return content

    def _generate_strings_tab(self, content_analysis: Dict) -> str:
        """Generate strings tab content."""
        strings = content_analysis.get('strings_found', [])
        if not strings:
            return "<p>No strings extracted.</p>"

        content = f'<div class="search-container"><input type="text" class="search-input" placeholder="Search strings..." onkeyup="filterItems(this.value, \'strings-container\')"></div>'
        content += '<div id="strings-container">'

        for string_item in strings[:1000]:  # Limit to first 1000 strings for performance
            content += f"""
            <div class="url-item" style="background: #f8f9fa; border: 1px solid #dee2e6;">
                <div class="url" style="color: #333; font-family: 'Courier New', monospace;">{string_item}</div>
            </div>
            """

        if len(strings) > 1000:
            content += f'<div class="duplicate-notice">⚠️ Showing first 1000 strings out of {len(strings)} total</div>'

        content += '</div>'
        return content

    def _generate_statistics(self, content_analysis: Dict, processing_stages: List[Dict]) -> str:
        """Generate statistics section."""
        strings_count = content_analysis.get('strings_count', 0)
        urls_count = len(content_analysis.get('urls_found', []))
        stages_count = len(processing_stages)
        successful_stages = sum(1 for stage in processing_stages if stage.get('success'))

        return f"""
        <div class="section">
            <h2>📈 Analysis Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{strings_count:,}</div>
                    <div class="stat-label">Strings Extracted</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{urls_count}</div>
                    <div class="stat-label">URLs Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{successful_stages}/{stages_count}</div>
                    <div class="stat-label">Stages Completed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{successful_stages * 100 // stages_count if stages_count > 0 else 0}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </div>
        """

    def _generate_assessment(self, assessment: Dict) -> str:
        """Generate assessment section."""
        threat_level = assessment.get('threat_level', 'unknown').upper()
        malware_family = assessment.get('malware_family', 'Unknown')
        summary = assessment.get('summary', 'No assessment available')

        threat_colors = {
            'HIGH': '#dc3545',
            'MEDIUM': '#ffc107',
            'LOW': '#28a745',
            'UNKNOWN': '#6c757d'
        }

        threat_color = threat_colors.get(threat_level, '#6c757d')

        return f"""
        <div class="assessment">
            <h2>🛡️ Threat Assessment</h2>
            <div class="threat-level" style="color: {threat_color};">{threat_level}</div>
            <div class="threat-description">Malware Family: {malware_family}</div>
            <div class="summary">{summary}</div>
        </div>
        """

    def _generate_footer(self) -> str:
        """Generate footer section."""
        return f"""
        <div class="footer">
            <p>Report generated by Grindoreiro v2.0 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>🔬 Advanced Malware Analysis Toolkit</p>
        </div>
        """


def main():
    """Main function to generate HTML reports."""
    parser = argparse.ArgumentParser(description='Generate consolidated HTML reports from analysis JSON files')
    parser.add_argument('json_file', help='Path to analysis JSON file')
    parser.add_argument('-o', '--output', help='Output HTML file path (default: auto-generated)')
    parser.add_argument('--batch', action='store_true', help='Process all JSON files in output directory')

    args = parser.parse_args()

    generator = ConsolidatedHTMLReportGenerator()

    if args.batch:
        # Process all JSON files in output directory
        output_dir = Path('./data/output')
        if not output_dir.exists():
            print("Output directory not found!")
            return

        json_files = list(output_dir.glob('*_analysis.json'))
        if not json_files:
            print("No analysis JSON files found!")
            return

        for json_file in json_files:
            print(f"Processing {json_file.name}...")

            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            html_content = generator.generate_report(data)

            html_file = json_file.with_suffix('.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"Generated {html_file}")

    else:
        # Process single JSON file
        json_file = Path(args.json_file)
        if not json_file.exists():
            print(f"JSON file not found: {json_file}")
            return

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        html_content = generator.generate_report(data)

        if args.output:
            output_file = Path(args.output)
        else:
            output_file = json_file.with_suffix('.html')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML report generated: {output_file}")


if __name__ == '__main__':
    main()

    def _get_css_styles(self) -> str:
        """Get comprehensive CSS styles for the report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }

        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }

        .header .subtitle {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 20px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .info-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }

        .info-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }

        .info-card p {
            color: #666;
            font-size: 0.9em;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-success { background: #d4edda; color: #155724; }
        .status-warning { background: #fff3cd; color: #856404; }
        .status-danger { background: #f8d7da; color: #721c24; }
        .status-info { background: #d1ecf1; color: #0c5460; }

        .section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }

        .hash-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .hash-item {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #28a745;
        }

        .hash-item .hash-type {
            font-weight: bold;
            color: #28a745;
            text-transform: uppercase;
            font-size: 0.9em;
            margin-bottom: 5px;
        }

        .hash-item .hash-value {
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #666;
            word-break: break-all;
        }

        .file-list {
            margin-top: 20px;
        }

        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
        }

        .file-item:hover {
            background: #f8f9fa;
        }

        .file-info {
            flex: 1;
        }

        .file-name {
            font-weight: bold;
            color: #333;
        }

        .file-details {
            color: #666;
            font-size: 0.9em;
            margin-top: 2px;
        }

        .file-hash {
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            color: #28a745;
            margin-top: 2px;
        }

        .file-size {
            color: #007bff;
            font-weight: bold;
        }

        .timeline {
            position: relative;
            padding-left: 30px;
        }

        .timeline-item {
            position: relative;
            padding: 15px 0;
            border-left: 2px solid #667eea;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: -6px;
            top: 20px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #667eea;
        }

        .timeline-item:last-child {
            border-left: none;
        }

        .timeline-item h4 {
            color: #667eea;
            margin-bottom: 5px;
        }

        .timeline-item .time {
            color: #666;
            font-size: 0.9em;
        }

        .timeline-item .status {
            margin-top: 5px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .stat-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
        }

        .url-list {
            margin-top: 20px;
        }

        .url-item {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }

        .url-item .url {
            font-family: 'Courier New', monospace;
            color: #856404;
            word-break: break-all;
        }

        .assessment {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
        }

        .assessment h2 {
            color: white;
            margin-bottom: 20px;
        }

        .threat-level {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .threat-description {
            font-size: 1.2em;
            margin-bottom: 20px;
        }

        .summary {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            font-style: italic;
        }

        .footer {
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 0.9em;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            .header {
                padding: 20px;
            }

            .header h1 {
                font-size: 2em;
            }

            .section {
                padding: 20px;
            }

            .info-grid {
                grid-template-columns: 1fr;
            }

            .hash-grid {
                grid-template-columns: 1fr;
            }

            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        .tab-container {
            margin-top: 20px;
        }

        .tab-buttons {
            display: flex;
            background: #f8f9fa;
            border-radius: 10px 10px 0 0;
            overflow: hidden;
        }

        .tab-button {
            flex: 1;
            padding: 15px;
            border: none;
            background: transparent;
            cursor: pointer;
            font-weight: bold;
            color: #666;
            transition: all 0.3s;
        }

        .tab-button.active {
            background: #667eea;
            color: white;
        }

        .tab-button:hover {
            background: #5a67d8;
            color: white;
        }

        .tab-content {
            background: white;
            border-radius: 0 0 10px 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }

        .tab-pane {
            display: none;
        }

        .tab-pane.active {
            display: block;
        }
        """

    def _get_js_scripts(self) -> str:
        """Get JavaScript for interactive features."""
        return """
        function switchTab(tabName) {
            // Hide all tab panes
            const tabPanes = document.querySelectorAll('.tab-pane');
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Remove active class from all tab buttons
            const tabButtons = document.querySelectorAll('.tab-button');
            tabButtons.forEach(button => button.classList.remove('active'));

            // Show selected tab pane
            document.getElementById(tabName).classList.add('active');

            // Add active class to clicked button
            event.target.classList.add('active');
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                // Show temporary feedback
                const notification = document.createElement('div');
                notification.textContent = 'Copied to clipboard!';
                notification.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #28a745;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    z-index: 1000;
                    font-weight: bold;
                `;
                document.body.appendChild(notification);
                setTimeout(() => document.body.removeChild(notification), 2000);
            });
        }

        // Initialize first tab as active
        document.addEventListener('DOMContentLoaded', function() {
            const firstTab = document.querySelector('.tab-button');
            const firstPane = document.querySelector('.tab-pane');
            if (firstTab && firstPane) {
                firstTab.classList.add('active');
                firstPane.classList.add('active');
            }
        });
        """

    def generate_report(self, json_data: Dict[str, Any]) -> str:
        """Generate HTML report from JSON data."""
        sample_info = json_data.get('sample_info', {})
        session_info = json_data.get('session_info', {})
        file_analysis = json_data.get('file_analysis', {})
        content_analysis = json_data.get('content_analysis', {})
        network_analysis = json_data.get('network_analysis', {})
        processing_stages = json_data.get('processing_stages', [])
        assessment = json_data.get('assessment', {})

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Malware Analysis Report - {sample_info.get('name', 'Unknown')}</title>
    <style>{self.css_styles}</style>
</head>
<body>
    <div class="container">
        {self._generate_header(sample_info, session_info)}
        {self._generate_overview(file_analysis, content_analysis)}
        {self._generate_file_hashes(file_analysis)}
        {self._generate_extracted_files(file_analysis)}
        {self._generate_processing_timeline(processing_stages)}
        {self._generate_statistics(content_analysis, processing_stages)}
        {self._generate_urls_found(content_analysis)}
        {self._generate_assessment(assessment)}
        {self._generate_footer()}
    </div>

    <script>{self.js_scripts}</script>
</body>
</html>
        """
        return html

    def _generate_header(self, sample_info: Dict, session_info: Dict) -> str:
        """Generate header section."""
        sample_name = sample_info.get('name', 'Unknown')
        sample_size = sample_info.get('size', 0)
        sha256 = sample_info.get('sha256', 'N/A')
        session_id = session_info.get('session_id', 'N/A')
        duration = session_info.get('total_duration', 0)

        return f"""
        <div class="header">
            <h1>🔍 Malware Analysis Report</h1>
            <div class="subtitle">Comprehensive analysis of {sample_name}</div>

            <div class="export-buttons">
                <button class="export-btn" onclick="exportToJSON()">Export JSON</button>
                <button class="export-btn" onclick="exportToCSV()">Export CSV</button>
            </div>

            <div class="info-grid">
                <div class="info-card">
                    <h3>📁 Sample Information</h3>
                    <p><strong>Name:</strong> {sample_name}</p>
                    <p><strong>Size:</strong> {sample_size:,} bytes</p>
                    <p><strong>SHA256:</strong> <span onclick="copyToClipboard('{sha256}')" style="cursor: pointer; text-decoration: underline;">{sha256[:16]}...</span></p>
                </div>

                <div class="info-card">
                    <h3>⏱️ Analysis Details</h3>
                    <p><strong>Session ID:</strong> {session_id}</p>
                    <p><strong>Duration:</strong> {duration:.2f} seconds</p>
                    <p><strong>Analysis Time:</strong> {session_info.get('analysis_start', 'N/A')}</p>
                </div>

                <div class="info-card">
                    <h3>🎯 Quick Status</h3>
                    <p><strong>Files Processed:</strong> {len(self.file_analysis.get('extracted_files', []))}</p>
                    <p><strong>URLs Found:</strong> {len(self.content_analysis.get('urls_found', []))}</p>
                    <p><strong>Strings:</strong> {self.content_analysis.get('strings_count', 0):,}</p>
                </div>
            </div>
        </div>
        """

    def _generate_overview(self, file_analysis: Dict, content_analysis: Dict) -> str:
        """Generate overview section."""
        msi_info = file_analysis.get('msi_info')
        dll_info = file_analysis.get('dll_info')

        overview_items = []

        if msi_info:
            overview_items.append(f"""
            <div class="info-card">
                <h3>📦 MSI Analysis</h3>
                <p><strong>MSI File:</strong> {Path(msi_info.get('msi_path', '')).name}</p>
                <p><strong>Size:</strong> {msi_info.get('msi_size', 0):,} bytes</p>
                <p><strong>SHA256:</strong> {msi_info.get('msi_sha256', 'N/A')[:16]}...</p>
            </div>
            """)

        if dll_info:
            overview_items.append(f"""
            <div class="info-card">
                <h3>🔧 DLL Analysis</h3>
                <p><strong>DLL File:</strong> {dll_info.get('name', 'N/A')}</p>
                <p><strong>Size:</strong> {dll_info.get('size', 0):,} bytes</p>
                <p><strong>SHA256:</strong> {dll_info.get('sha256', 'N/A')[:16]}...</p>
            </div>
            """)

        if content_analysis.get('cnc_url'):
            overview_items.append(f"""
            <div class="info-card">
                <h3>🌐 C&C Server</h3>
                <p><strong>URL:</strong> {content_analysis.get('cnc_url')}</p>
                <p><strong>Status:</strong> <span class="status-badge status-danger">MALICIOUS</span></p>
            </div>
            """)

        return f"""
        <div class="section">
            <h2>📊 Analysis Overview</h2>
            <div class="info-grid">
                {''.join(overview_items)}
            </div>
        </div>
        """

    def _generate_file_hashes(self, file_analysis: Dict) -> str:
        """Generate file hashes section."""
        file_hashes = file_analysis.get('file_hashes', {})

        if not file_hashes:
            return ""

        hash_items = []
        for hash_type, hash_info in file_hashes.items():
            hash_items.append(f"""
            <div class="hash-item">
                <div class="hash-type">{hash_type.upper()}</div>
                <div class="hash-value" onclick="copyToClipboard('{hash_info.get('sha256', 'N/A')}')" style="cursor: pointer;">
                    {hash_info.get('sha256', 'N/A')}
                </div>
                <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                    Size: {hash_info.get('size', 0):,} bytes | Type: {hash_info.get('file_type', 'unknown')}
                </div>
            </div>
            """)

        return f"""
        <div class="section">
            <h2>🔐 File Hashes</h2>
            <div class="hash-grid">
                {''.join(hash_items)}
            </div>
        </div>
        """

    def _generate_extracted_files(self, file_analysis: Dict) -> str:
        """Generate extracted files section."""
        extracted_files = file_analysis.get('extracted_files', [])

        if not extracted_files:
            return ""

        file_items = []
        for file_info in extracted_files:
            file_items.append(f"""
            <div class="file-item">
                <div class="file-info">
                    <div class="file-name">{file_info.get('name', 'Unknown')}</div>
                    <div class="file-details">Path: {file_info.get('path', 'N/A')}</div>
                    <div class="file-hash">SHA256: {file_info.get('sha256', 'N/A')[:32]}...</div>
                </div>
                <div class="file-size">{file_info.get('size', 0):,} bytes</div>
            </div>
            """)

        return f"""
        <div class="section">
            <h2>📂 Extracted Files</h2>
            <div class="file-list">
                {''.join(file_items)}
            </div>
        </div>
        """

    def _generate_processing_timeline(self, processing_stages: List[Dict]) -> str:
        """Generate processing timeline section."""
        if not processing_stages:
            return ""

        timeline_items = []
        for stage in processing_stages:
            status_class = "status-info"
            if stage.get('success'):
                status_class = "status-success"
            elif stage.get('error_message'):
                status_class = "status-danger"

            timeline_items.append(f"""
            <div class="timeline-item">
                <h4>{stage.get('stage', 'unknown').replace('_', ' ').title()}</h4>
                <div class="time">Duration: {stage.get('duration', 0):.3f}s</div>
                <div class="status">
                    <span class="status-badge {status_class}">
                        {'SUCCESS' if stage.get('success') else 'FAILED'}
                    </span>
                </div>
                {f'<div style="color: #721c24; margin-top: 5px;">{stage.get("error_message")}</div>' if stage.get('error_message') else ''}
            </div>
            """)

        return f"""
        <div class="section">
            <h2>⏳ Processing Timeline</h2>
            <div class="timeline">
                {''.join(timeline_items)}
            </div>
        </div>
        """

    def _generate_statistics(self, content_analysis: Dict, processing_stages: List[Dict]) -> str:
        """Generate statistics section."""
        strings_count = content_analysis.get('strings_count', 0)
        urls_count = len(content_analysis.get('urls_found', []))
        stages_count = len(processing_stages)
        successful_stages = sum(1 for stage in processing_stages if stage.get('success'))

        return f"""
        <div class="section">
            <h2>📈 Analysis Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{strings_count:,}</div>
                    <div class="stat-label">Strings Extracted</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{urls_count}</div>
                    <div class="stat-label">URLs Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{successful_stages}/{stages_count}</div>
                    <div class="stat-label">Stages Completed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{successful_stages * 100 // stages_count if stages_count > 0 else 0}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </div>
        """

    def _generate_urls_found(self, content_analysis: Dict) -> str:
        """Generate URLs found section."""
        urls = content_analysis.get('urls_found', [])
        cnc_url = content_analysis.get('cnc_url')
        download_url = content_analysis.get('download_url')

        if not urls:
            return ""

        url_items = []
        for url in urls:
            is_cnc = url == cnc_url
            is_download = url == download_url

            badge = ""
            if is_cnc:
                badge = '<span class="status-badge status-danger" style="margin-left: 10px;">C&C SERVER</span>'
            elif is_download:
                badge = '<span class="status-badge status-warning" style="margin-left: 10px;">DOWNLOAD</span>'

            url_items.append(f"""
            <div class="url-item">
                <div class="url">{url}</div>
                {badge}
            </div>
            """)

        return f"""
        <div class="section">
            <h2>🌐 URLs Found</h2>
            <div class="url-list">
                {''.join(url_items)}
            </div>
        </div>
        """

    def _generate_assessment(self, assessment: Dict) -> str:
        """Generate assessment section."""
        threat_level = assessment.get('threat_level', 'unknown').upper()
        malware_family = assessment.get('malware_family', 'Unknown')
        summary = assessment.get('summary', 'No assessment available')

        threat_colors = {
            'HIGH': '#dc3545',
            'MEDIUM': '#ffc107',
            'LOW': '#28a745',
            'UNKNOWN': '#6c757d'
        }

        threat_color = threat_colors.get(threat_level, '#6c757d')

        return f"""
        <div class="assessment">
            <h2>🛡️ Threat Assessment</h2>
            <div class="threat-level" style="color: {threat_color};">{threat_level}</div>
            <div class="threat-description">Malware Family: {malware_family}</div>
            <div class="summary">{summary}</div>
        </div>
        """

    def _generate_footer(self) -> str:
        """Generate footer section."""
        return f"""
        <div class="footer">
            <p>Report generated by Grindoreiro v2.0 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>🔬 Advanced Malware Analysis Toolkit</p>
        </div>
        """


def main():
    """Main function to generate HTML reports."""
    parser = argparse.ArgumentParser(description='Generate HTML reports from analysis JSON files')
    parser.add_argument('json_file', nargs='?', help='Path to analysis JSON file')
    parser.add_argument('-o', '--output', help='Output HTML file path (default: auto-generated)')
    parser.add_argument('--batch', action='store_true', help='Process all JSON files in output directory')

    args = parser.parse_args()

    generator = ConsolidatedHTMLReportGenerator()

    if args.batch:
        # Process all JSON files in output directory
        output_dir = Path('./data/output')
        if not output_dir.exists():
            print("Output directory not found!")
            return

        json_files = list(output_dir.glob('*_analysis.json'))
        if not json_files:
            print("No analysis JSON files found!")
            return

        for json_file in json_files:
            print(f"Processing {json_file.name}...")

            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            html_content = generator.generate_report(data)

            html_file = json_file.with_suffix('.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"Generated {html_file}")

    else:
        # Process single JSON file
        json_file = Path(args.json_file)
        if not json_file.exists():
            print(f"JSON file not found: {json_file}")
            return

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        html_content = generator.generate_report(data)

        if args.output:
            output_file = Path(args.output)
        else:
            output_file = json_file.with_suffix('.html')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML report generated: {output_file}")


if __name__ == '__main__':
    main()
