
# TODO: FIX the issue of downloading spacy models within installation


import glob
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
data_files_path = glob.glob(os.path.join("DocumentAI_std", "data_files", "*.json"))

# List of tuples (target_dir, files)
data_files = [("data_files", data_files_path)]

# Set up the package
setup(
    name="DocumentAI_std",
    version="0.3.8-dev4",
    packages=find_packages(exclude=["DocumentAI_std.tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    data_files=data_files,  # Include the data_files in the package
    url="https://github.com/LATIS-DocumentAI-Group/DocumentAI-std",
    license="MIT",
    author="Hamza Gbada",
    author_email="hamza.gbada@gmail.com",
    python_requires=">=3.11, <3.13",
    description="The main standards for Latis Document AI project",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
