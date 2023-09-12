import os
from setuptools import setup, find_packages

PYPI_REQUIREMENTS = []
if os.path.exists('requirements.txt'):
    for line in open('requirements.txt'):
        PYPI_REQUIREMENTS.append(line.strip())

setup(
    name="ZotTools", 
    packages=find_packages(),
    version='0.0.1',
    install_requires=PYPI_REQUIREMENTS,
    )