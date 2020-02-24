# ayx-blackbird: Build fast tools, fast.

[![Build Status](https://travis-ci.com/dme722/ayx-blackbird.svg?branch=master)](https://travis-ci.com/dme722/ayx-blackbird)

![alt text](blackbird.jpg "Logo Title Text 1")

## What is it?
`ayx-blackbird` is a package for building new tools for [Alteryx Designer](https://www.alteryx.com/designer-trial/free-trial?&utm_source=google&utm_medium=cpc&utm_campaign=Demgen-Mixed-Brand_New&utm_term=alteryx%20designer&gclid=CjwKCAiAjrXxBRAPEiwAiM3DQlrvZhb2QftEwjdOIkT7rhunlaipoaT4wiFn7GsEuDrqmnj7eMNL2RoCY-oQAvD_BwE) in Python.

Alteryx Designer is equipped with a [Python SDK](https://help.alteryx.com/developer/current/Python/Overview.htm). This SDK is quite powerful, however it is convoluted and difficult to use for newcomers.

`ayx-blackbird` is an abstraction layer for the Python SDK that compromises on neither ease of use nor performance.

## Main Features
- A suite of example tools to get you off the ground.
- CLI tools to set up your tool directory structure, assist with development, and package [YXIs](https://help.alteryx.com/developer/current/PackageTool.htm?tocpath=SDKs%7CBuild%20Custom%20Tools%7C_____7).
- An extremely flexible development platform that by default, allows extremely fast development of new tools, and with small modifications, extremely fast performance.

## Where to get it

The source code is currently hosted on GitHub at: https://github.com/dme722/ayx-blackbird

Binary installers for the latest released version are available at the Python package index.

```
pip install ayx_blackbird
```

## Dependencies
[Click](https://click.palletsprojects.com/en/7.x/)

[Numpy](https://numpy.org/)

[Pandas](https://pandas.pydata.org/)

[xmltodict](https://github.com/martinblech/xmltodict)

## License
[Apache 2.0](LICENSE)

## Documentation
The official documentation is hosted on Github: https://github.com/dme722/ayx-blackbird/wiki

## Contributing
Contributors are all welcome! Please see the [Contribution Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.