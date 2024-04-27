from pathlib import Path

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="DocumentAI_std",
    version="0.2.6.dev1",
    # packages=find_packages(where='DocumentAI_std'),  # Include all packages within this directory
    packages=find_packages(exclude=["DocumentAI_std.tests"]),
    # package_dir={'': 'DocumentAI_std'},  # Set root package directory
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    url="",
    license="",
    author="Hamza Gbada",
    author_email="",
    description="The main standards for Latis Document AI project",
)
