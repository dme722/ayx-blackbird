from setuptools import setup, find_packages
from ayx_blackbird.version import __version__

with open("requirements.txt") as f:
  requirements = f.readlines()

setup(
    name="ayx_blackbird",
    url="https://github.com/dme722/ayx-blackbird",
    license="Apache License 2.0",
    version=__version__,
    python_requires=">=3.6.0",
    description="The (Better) Alteryx Python SDK Abstraction Layer",
    author="Drew Ellison",
    author_email="dme722@gmail.com",
    install_requires=requirements,
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
