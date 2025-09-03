# HTML Reports

> Generating and viewing interactive HTML analysis reports

## 🎯 Overview

Grindoreiro generates comprehensive HTML reports with interactive features for easy analysis and sharing.

## 🚀 Quick Start

```bash
# Generate HTML report from analysis
python html_report_generator.py data/output/sample_analysis.json

# Generate batch reports for all samples
python batch_html_report.py

# View report in browser
# Open data/output/sample_analysis.html
```

## 📊 Report Types

### Individual Reports

**Purpose**: Detailed analysis of a single sample

```bash
python html_report_generator.py data/output/sample_analysis.json
```

**Features**:
- 📋 **Sample Overview**: Basic information and metadata
- 📁 **File Analysis**: Extracted files with deduplication
- 🌐 **URL Analysis**: Found URLs grouped by domain
- 📈 **Timeline**: Processing stages with status
- 🔍 **String Search**: Interactive string filtering
- 📊 **Statistics**: Analysis metrics and success rates

### Batch Reports

**Purpose**: Consolidated view of multiple samples

```bash
python batch_html_report.py
```

**Features**:
- 📊 **Summary Dashboard**: Overall statistics and trends
- 🔍 **Sample Grid**: Quick access to individual reports
- 📈 **Performance Metrics**: Processing times and success rates
- 🚨 **Error Overview**: Failed samples and issues
- 📤 **Export Options**: Download data in multiple formats

## 🎨 Report Features

### Interactive Elements

#### Search & Filter

- **Real-time Search**: Filter files, URLs, and strings instantly
- **Category Filters**: Filter by file type, domain, or content
- **Case Sensitivity**: Toggle case-sensitive search
- **Regex Support**: Advanced pattern matching

#### Navigation

- **Tabbed Interface**: Organized sections for different data types
- **Collapsible Sections**: Expand/collapse content areas
- **Breadcrumb Navigation**: Easy navigation between sections
- **Bookmarkable URLs**: Share specific report sections

### Data Visualization

#### Charts & Graphs

- **Processing Timeline**: Visual representation of analysis stages
- **File Type Distribution**: Pie charts of extracted file types
- **URL Domain Analysis**: Bar charts of domain frequencies
- **Success/Failure Metrics**: Visual success rates

#### Tables & Lists

- **Sortable Columns**: Click headers to sort data
- **Pagination**: Handle large datasets efficiently
- **Export Options**: Download data as CSV or JSON
- **Copy to Clipboard**: Easy data extraction

## 📁 Report Structure

### Individual Report Layout

```
Header
├── Sample Information
├── Analysis Summary
└── Quick Statistics

Navigation Tabs
├── Overview
├── Files
├── URLs
├── Timeline
├── Strings
└── Statistics

Footer
├── Export Options
├── Generation Info
└── Links
```

### Batch Report Layout

```
Header
├── Batch Summary
├── Processing Statistics
└── Quick Actions

Sample Grid
├── Sample List
├── Status Indicators
└── Quick Links

Analysis Overview
├── Success Rates
├── Error Summary
└── Performance Metrics

Footer
├── Export All Data
├── Generation Info
└── Links
```

## 🔧 Customization

### Report Templates

Modify `report_template.html` to customize:

```html
<!-- Custom styling -->
<style>
.custom-header {
    background: linear-gradient(45deg, #your-color, #another-color);
}
</style>

<!-- Custom JavaScript -->
<script>
function customFunction() {
    // Your custom functionality
}
</script>
```

### CSS Customization

```css
/* Custom theme colors */
:root {
    --primary-color: #your-brand-color;
    --secondary-color: #your-accent-color;
    --background-color: #your-background;
}

/* Custom layout */
.report-container {
    max-width: 1400px; /* Adjust width */
    font-family: 'Your Font', sans-serif;
}
```

## 📤 Export Options

### Data Export

- **JSON Export**: Complete analysis data
- **CSV Export**: Tabular data for spreadsheets
- **Text Export**: Plain text summaries
- **PDF Export**: Print-ready reports

### Batch Export

```bash
# Export all sample data
python -c "
import json
import csv
from pathlib import Path

output_dir = Path('data/output')
for json_file in output_dir.glob('*_analysis.json'):
    # Export logic here
    pass
"
```

## 🌐 Web Serving

### Local Server

```bash
# Python built-in server
cd data/output
python -m http.server 8000

# Open in browser
# http://localhost:8000/sample_analysis.html
```

### Production Deployment

```bash
# Nginx configuration
server {
    listen 80;
    server_name reports.example.com;
    root /path/to/grindoreiro/data/output;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 📊 Advanced Features

### Deduplication

- **File Hashing**: SHA256-based duplicate detection
- **Content Grouping**: Similar files grouped together
- **Reference Counting**: Track duplicate occurrences
- **Storage Optimization**: Reduce storage for duplicate files

### Search Capabilities

#### Basic Search

```javascript
// Simple text search
function searchContent(query) {
    const elements = document.querySelectorAll('.searchable');
    elements.forEach(el => {
        const text = el.textContent.toLowerCase();
        el.style.display = text.includes(query.toLowerCase()) ? '' : 'none';
    });
}
```

#### Advanced Search

- **Regex Patterns**: `/https?:\/\/[^\s]+/g`
- **Case Insensitive**: `/pattern/i`
- **Word Boundaries**: `/\bword\b/g`
- **Multiple Terms**: `term1|term2|term3`

### Performance Optimization

#### Large Reports

- **Lazy Loading**: Load content on demand
- **Virtual Scrolling**: Handle thousands of items
- **Compression**: Gzip compression for faster loading
- **Caching**: Browser caching for static assets

## 🆘 Troubleshooting

### Report Not Generating

**Issue**: HTML report fails to generate

**Solutions**:
```bash
# Check JSON file exists
ls -la data/output/sample_analysis.json

# Verify JSON structure
python -c "import json; json.load(open('data/output/sample_analysis.json'))"

# Check permissions
chmod 644 data/output/sample_analysis.json

# Regenerate analysis
python -m grindoreiro.cli sample.zip --verbose
```

### Report Not Displaying

**Issue**: HTML report doesn't render properly

**Solutions**:
- Check browser console for JavaScript errors
- Verify CSS loading
- Test with different browsers
- Check file permissions

### Large Report Performance

**Issue**: Report is slow with large datasets

**Solutions**:
- Enable browser hardware acceleration
- Increase browser memory limits
- Use pagination for large tables
- Implement virtual scrolling

## 🔧 Integration

### SIEM Integration

```python
# Export for SIEM
import json
from pathlib import Path

def export_for_siem(json_path: Path, siem_format: str):
    with open(json_path) as f:
        data = json.load(f)

    if siem_format == 'splunk':
        # Format for Splunk
        events = []
        for item in data.get('findings', []):
            event = {
                'timestamp': data['timestamp'],
                'sample': data['sample_name'],
                'type': item['type'],
                'value': item['value'],
                'severity': item['severity']
            }
            events.append(event)
        return events
```

### API Integration

```python
# REST API endpoint
from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/reports/<sample_name>')
def get_report(sample_name):
    report_path = f'data/output/{sample_name}_analysis.html'
    if os.path.exists(report_path):
        return send_file(report_path)
    return {'error': 'Report not found'}, 404
```

## 📈 Analytics & Metrics

### Report Metrics

- **Generation Time**: How long it takes to create reports
- **File Size**: Report size and optimization opportunities
- **Load Time**: Browser loading performance
- **User Interactions**: Click tracking and usage patterns

### Usage Tracking

```javascript
// Track user interactions
document.addEventListener('click', function(e) {
    if (e.target.matches('.search-button')) {
        gtag('event', 'search', {
            'event_category': 'engagement',
            'event_label': 'search_used'
        });
    }
});
```

## 📚 Related Topics

- [Basic Usage](basic-usage.md) - Generating reports
- [Batch Processing](batch-processing.md) - Batch report generation
- [Configuration](configuration.md) - Report customization
- [HTML Generator](../tools/html-generator.md) - Technical details

## 🎨 Best Practices

### Design Principles

1. **Clarity**: Clear information hierarchy
2. **Consistency**: Uniform styling and behavior
3. **Performance**: Fast loading and interaction
4. **Accessibility**: Screen reader and keyboard support

### Content Organization

1. **Progressive Disclosure**: Show summary first, details on demand
2. **Logical Flow**: Guide users through information naturally
3. **Visual Hierarchy**: Use typography and spacing effectively
4. **Actionable Data**: Make data useful and exportable

---

💡 **Pro Tip**: Use browser developer tools to inspect and debug report rendering issues.</content>
<parameter name="filePath">c:\Users\pxd\Desktop\grindoreiro\docs\user-guides\html-reports.md
