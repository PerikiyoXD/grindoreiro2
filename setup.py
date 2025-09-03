"""Setup configuration for Grindoreiro package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="grindoreiro",
    version="1.0.0",
    author="PerikiyoXD",
    description="Malware analysis toolkit for Grandoreiro samples",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.24.0",
        "certifi>=2020.6.20",
        "chardet>=3.0.4",
        "idna>=2.10",
        "urllib3>=1.25.10",
    ],
    entry_points={
        "console_scripts": [
            "grindoreiro=grindoreiro.cli:main",
            "stringripper=grindoreiro.scripts.stringripper:main",
            "isoabduct=grindoreiro.scripts.isoabduct:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
