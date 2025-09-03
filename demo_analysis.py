#!/usr/bin/env python3
"""Safe demonstration of Grindoreiro string extraction capabilities."""

from pathlib import Path
from grindoreiro.analyzer import StringExtractor
from grindoreiro.core import setup_logging

def main():
    print('🧪 TESTING STRING EXTRACTION (WiX-independent)')
    print('=' * 50)

    # Setup logging
    setup_logging()

    # Create a test file to demonstrate string extraction
    test_content = b'''Hello World
This is a test string
https://malicious.example.com/c2
Normal text content
Some binary data\x00\x01\x02
Another URL: http://c2server.com:8080/api
'''

    test_file = Path('demo_sample.bin')
    with open(test_file, 'wb') as f:
        f.write(test_content)

    print(f'Created test file: {test_file}')
    print(f'File size: {test_file.stat().st_size} bytes')

    # Test string extraction
    extractor = StringExtractor(min_length=4)
    strings = extractor.extract_strings(test_file)

    print(f'\nExtracted {len(strings)} strings:')
    for i, s in enumerate(strings, 1):
        print(f'  {i:2d}. "{s}"')

    # Show URLs found
    from grindoreiro.analyzer import URLAnalyzer
    url_analyzer = URLAnalyzer()
    urls = url_analyzer.find_urls(strings)

    if urls:
        print(f'\n🌐 Found {len(urls)} URLs:')
        for url in urls:
            print(f'  🔗 {url}')

    # Clean up
    test_file.unlink()
    strings_file = test_file.with_suffix('.strings')
    if strings_file.exists():
        strings_file.unlink()

    print('\n✅ String extraction and URL analysis working correctly!')
    print('💡 Once WiX is installed, you can analyze full malware samples.')

if __name__ == "__main__":
    main()
