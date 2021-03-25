"""
setup.py for building and distribution
"""
from setuptools import setup
from setuptools import find_packages

# Load the README file.
with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()
setup(
    name='niv',
    author='HS Worms Top',
    version='1.5',
    description='console application to visualize network infrastructure using YAML files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.rlp.net/top/21s/niv/niv',
    install_requires=[
        "graphviz==0.16",
        "diagrams==0.19.1",
        "PyYAML==5.4.1"
    ],
    keywords='niv, network infrastructure visualizer',
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'niv = src.main:main'
        ],
    },
    include_package_data=True,
    python_requires='>=',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])
