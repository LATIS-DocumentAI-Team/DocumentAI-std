from pathlib import Path
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="DocumentAI_std",
    version="0.3.3-dev3",
    packages=find_packages(exclude=["DocumentAI_std.tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
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
