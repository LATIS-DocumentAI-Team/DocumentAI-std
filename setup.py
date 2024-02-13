# from setuptools import setup
#
#
# with open('requirements.txt') as f:
#     required = f.read().splitlines()
# setup(
#     name='DocumentAI-std',
#     version='0.1.0',
#     packages=['base', 'utils', 'datasets'],
#     package_dir={'DocumentAI-std': 'DocumentAI-std'},
#     install_requires=required,
#     url='',
#     license='',
#     author='Hamza Gbada',
#     author_email='',
#     description='The main standards for Latis Document AI project'
# )

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='DocumentAI-std',
    version='0.1.0',
    # packages=find_packages(where='DocumentAI-std'),  # Include all packages within this directory
    packages=find_packages(exclude=['DocumentAI-std.tests']),
    # package_dir={'': 'DocumentAI-std'},  # Set root package directory
    install_requires=required,
    url='',
    license='',
    author='Hamza Gbada',
    author_email='',
    description='The main standards for Latis Document AI project'
)
