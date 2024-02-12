from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='your_package_name',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'your_script_name = your_package_name.module_name:main_function',
        ],
    },
    # Add other metadata like author, description, etc.
    author='Your Name',
    description='Description of your package',
)
