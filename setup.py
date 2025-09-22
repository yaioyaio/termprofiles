from pathlib import Path
from setuptools import find_packages, setup

README_PATH = Path(__file__).parent / "README.md"
long_description = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""

setup(
    name="termprofiles",
    version="0.1.0",
    description="Per-project terminal profiles for iTerm2 (macOS) and Windows Terminal (Windows), safely via per-file JSON.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="yaioyaio",
    author_email="yaioyaio@gmail.com",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
    ],
    project_urls={
        "Homepage": "https://github.com/yaioyaio/termprofiles",
    },
    entry_points={
        "console_scripts": [
            "termprofiles = termprofiles.cli:main",
        ]
    },
)
