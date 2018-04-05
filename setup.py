from setuptools import setup

setup(
    name='wordexporter',
    version='2.7.12',
    description='Word Exporter',
    url='https://github.com/kyleesantos/Capio',
    author='Kylee Santos',
    packages=['wordexporter'],
    install_requires=['python-docx'],
    entry_points={
        'console_scripts': ['wordexporter=wordexporter.wordExporter:main'],
    }
)
