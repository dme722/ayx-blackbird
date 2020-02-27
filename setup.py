import os
from setuptools import setup, find_packages

from ayx_blackbird.version import __version__


CLASSIFIERS = [
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering",
    "Operating System :: Microsoft :: Windows"
]

SUMMARY = (__doc__ or "").split("\n")

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(THIS_DIRECTORY, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


REQUIREMENTS = [
    "Click>=7.0",
    "numpy>=1.16.3",
    "pandas>=0.23.4",
    "xmltodict>=0.11.0"
]

setup(
    name="ayx_blackbird",
    url="https://github.com/dme722/ayx-blackbird",
    license="Apache License 2.0",
    version=__version__,
    python_requires=">=3.6.0",
    description="Alteryx Designer Python SDK Abstraction Layer",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    author="Drew Ellison",
    author_email="dme722@gmail.com",
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        ayx_blackbird=ayx_blackbird.__main__:main
    """,
    package_data={
        "ayx_blackbird": [
            "assets/*",
            "assets/base_tool_config/*",
            "assets/examples/*",
            "assets/examples/BlackbirdPassthrough/*",
            "assets/examples/BlackbirdInput/*",
            "assets/examples/BlackbirdMultianchor/*",
            "assets/examples/BlackbirdMultipleInputs/*",
            "assets/examples/BlackbirdMultipleOutputs/*",
            "assets/examples/BlackbirdOptional/*",
            "assets/examples/BlackbirdOutput/*",
        ]
    }
)
