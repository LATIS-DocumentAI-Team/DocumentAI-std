# TODO: FIX the issue of downloading spacy models within installation


import os
from pathlib import Path
from setuptools import setup, find_packages

# Read the requirements from the requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

# Get the long description from the README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Collect all .json files in the data_files directory
data_files_path = [str(p) for p in Path("DocumentAI_std/data_file").rglob("*.json")]

# Set up the package
setup(
    name="DocumentAI_std",
    version="0.4.0-dev5",
    packages=find_packages(exclude=["DocumentAI_std.tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    package_data={
        "DocumentAI_std": data_files_path,  # Include JSON files in the DocumentAI_std package
    },
    include_package_data=True,  # Ensure non-Python files are included
    url="https://github.com/LATIS-DocumentAI-Group/DocumentAI-std",
    license="MIT",
    author="Hamza Gbada",
    author_email="hamza.gbada@gmail.com",
    python_requires=">=3.11, <3.14",
    description="The main standards for Latis Document AI project",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
