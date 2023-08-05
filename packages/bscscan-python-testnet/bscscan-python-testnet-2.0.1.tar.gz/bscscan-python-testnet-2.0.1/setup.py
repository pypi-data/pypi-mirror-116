from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="bscscan-python-testnet",
    version="2.0.1",
    description="A python API for bscscan.com with support for BSC Testnet",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/gabr1e11/bscscan-python",
    author="Panagiotis-Christos Kotsias, Roberto Cano",
    author_email="kotsias.pan@gmail.com, thesolidchain@gmail.com",
    license="MIT",
    packages=[
        "bscscan",
        "bscscan.configs",
        "bscscan.core",
        "bscscan.enums",
        "bscscan.modules",
        "bscscan.utils",
    ],
    python_requires='>=3.8',
    install_requires=["aiohttp", "requests"],
    include_package_data=True,
    zip_safe=False,
)
