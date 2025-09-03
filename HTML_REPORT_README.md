# HTML Report Generator

This consolidated HTML report generator creates beautiful, interactive HTML reports from Grindoreiro malware analysis results.

## Features

- **Consolidated Design**: Single generator that replaces the old duplicate generators
- **Interactive Reports**: Tabbed interface with search functionality
- **Deduplication**: Automatically groups and highlights duplicate files and URLs
- **Batch Processing**: Generate reports for multiple analysis files at once
- **Export Options**: Export findings to JSON or CSV
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional appearance with intuitive navigation

## Usage

### Generate a single HTML report

```bash
python html_report_generator.py path/to/analysis_result.json
```

### Generate HTML reports for all JSON files in the output directory

```bash
python html_report_generator.py --batch
```

### Use the batch report generator (recommended for multiple files)

```bash
python batch_html_report.py
```

This will:
1. Generate individual HTML reports for each JSON file
2. Create a batch summary report (`batch_report.html`) with an overview of all samples

## Report Features

### Individual Reports
- **Header**: Sample information, analysis details, and quick status
- **Overview**: Key findings including MSI/DLL analysis and C&C servers
- **Tabbed Content**:
  - **Files**: Extracted files with deduplication and search
  - **URLs**: Found URLs grouped by domain with deduplication
  - **Timeline**: Processing stages with success/failure status
  - **Strings**: Extracted strings with search functionality
- **Statistics**: Analysis metrics and success rates
- **Threat Assessment**: Risk level and malware family identification

### Batch Report
- **Summary Statistics**: Total samples, files, URLs, and strings
- **Threat Distribution**: Overview of threat levels across all samples
- **Sample Grid**: Quick access to individual reports
- **Export Options**: Download all findings as JSON or CSV

## File Structure

```
data/output/
├── *_analysis.json          # Analysis result files
├── *_analysis.html          # Individual HTML reports
└── batch_report.html        # Batch summary report
```

## Key Improvements

1. **Deduplication**: Files with identical hashes are grouped together
2. **Interactive Search**: Filter files, URLs, and strings in real-time
3. **Export Functionality**: Download data in multiple formats
4. **Responsive Design**: Works on all screen sizes
5. **Performance**: Optimized for large analysis results
6. **Modern UI**: Clean, professional appearance

## Technical Details

- **CSS**: Embedded responsive styles with modern design
- **JavaScript**: Interactive features without external dependencies
- **Data Handling**: Efficient processing of large JSON files
- **Error Handling**: Graceful handling of malformed data
- **Cross-platform**: Works on Windows, Linux, and macOS

## Examples

### View a single report
Open `data/output/DOC__34867_FRT.zip_analysis.html` in your web browser

### View batch summary
Open `data/output/batch_report.html` in your web browser

### Export findings
Use the "Export JSON" or "Export CSV" buttons in any report

## Integration

The HTML reports can be:
- Served by a web server for team access
- Archived for compliance purposes
- Integrated into SIEM systems
- Used in incident response workflows
- Shared with stakeholders via email or secure links
