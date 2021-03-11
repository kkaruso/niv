from setuptools import setup
from setuptools import find_packages

# Load the README file.
with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()
setup(
    name='niv-top-test',
    author='HS Worms Top',
    author_email='inf3199@hs-worms.de',
    version='0.2',
    description='console application to visualize network infrastructure using YAML files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.rlp.net/top/21s/niv/niv',
    install_requires=[
        "graphviz==0.16",
        "diagrams==0.19.1",
        "ruamel.yaml==0.16.13",
        "PyYAML==5.4.1"
    ],
    keywords='niv, network infrastructure visualisation',
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'niv = main:main'
        ],
    },
    include_package_data=True,
    python_requires='>=',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])
