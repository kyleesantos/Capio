from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wordExporter',
    version='2.7.12',
    description='Word Exporter',
    url='https://github.com/kyleesantos/Capio',
    author='Kylee Santos',
    packages=find_packages(),
    install_requires=['numpy','python-docx'],
)
