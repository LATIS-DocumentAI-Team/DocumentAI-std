import glob
import os
from pathlib import Path

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()
# TODO: FIX the issue of downloading spacy models within installation

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

data_files_path = glob.glob(os.path.join("DocumentAI_std", "data_files", "*.json"))

data_files = [("data_files", data_files_path)]
setup(
    name="DocumentAI_std",
    version="0.3.8-dev3",
    packages=find_packages(exclude=["DocumentAI_std.tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    data_files=data_files,
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
