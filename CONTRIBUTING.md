# Contributing to ayx-blackbird

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to ayx-blackbird and its packages, which are hosted on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[Code of Conduct](#code-of-conduct)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)
  
[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [JavaScript Styleguide](#javascript-styleguide)
  * [CoffeeScript Styleguide](#coffeescript-styleguide)
  * [Specs Styleguide](#specs-styleguide)
  * [Documentation Styleguide](#documentation-styleguide)
  
[Additional Notes](#additional-notes)
  * [Issue and Pull Request Labels](#issue-and-pull-request-labels)
  
## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [dme722@gmail.com](mailto:dme722@gmail.com).

#### Package Conventions

This is primarily a Python package and therefore follows the following Python coding standards:

- Linting:
    - [black](https://black.readthedocs.io/en/stable/): Linting rules
    - [flake8](http://flake8.pycqa.org/en/latest/): Linting rules
    - [mypy](http://mypy-lang.org/): Static type enforcement


### Design Decisions

Many design decisions made in this library are based on the [Gang of Four book](https://www.amazon.com/Design-Patterns-Object-Oriented-Addison-Wesley-Professional-ebook/dp/B000SEIBB8). 
For an overview of the designs in this book, please see this [reference](http://www.blackwasp.co.uk/gofpatterns.aspx).

The key design patterns used in this library are:
- [Proxy]()
- [Observable]()
- [Strategy]()
- [Mixins]()

Additionally, this library is based on the concept of inheritance. A user is intended to install this library, and inherit from `ayx_blackbird.core.BasePlugin`. From there, any custom behviour can be specified by overriding methods/properties of the base class.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for `ayx_blackbird`. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.


> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Submitting A Bug Report/Enhancement Suggestion

* **Make sure it's a problem.** You might be able to find the cause of the problem and fix things yourself. Most importantly, check if you can reproduce the problem in the latest version of ayx_blackbird..
* **Check the issues board** — you might discover that the bug/enhancement is already listed. Most importantly, check if you're using the latest version of ayx_blackbird.

### Your First Code Contribution

Unsure where to begin contributing to ayx_blackbird? You can start by looking through the issues:

* Have a question about how to add a feature, or want to know if it's a good idea?
    - Open an issue.
    - Email me at [dme722@gmail.com](mailto:dme722@gmail.com)


#### Local development

- Clone the repo.
- Make sure to have the `requirements-dev.txt` `pip` installed.
- Make any changes you want.
- From the root of the repo (with the conda environment of the tool you're testing activated) `pip install .` to update the version of ayx_blackbird for the desired tool.
- Run `doit` at the command line from the root of the repo to run linting checks and tests.

### Pull Requests

The process described here has several goals:

- Maintain ayx-blackbird's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible package
- Enable a sustainable system for maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in [the template](PULL_REQUEST_TEMPLATE.md)
2. Follow the [styleguides](#styleguides)
3. After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing <details><summary>What if the status checks are failing?</summary>If a status check is failing, and you believe that the failure is unrelated to your change, please leave a comment on the pull request explaining why you believe the failure is unrelated. A maintainer will re-run the status check for you. If we conclude that the failure was a false positive, then we will open an issue to track that problem with our status check suite.</details>

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* When only changing documentation, include `[ci skip]` in the commit title
* Consider starting the commit message with an applicable emoji:
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :non-potable_water: `:non-potable_water:` when plugging memory leaks
    * :memo: `:memo:` when writing docs
    * :penguin: `:penguin:` when fixing something on Linux
    * :apple: `:apple:` when fixing something on macOS
    * :checkered_flag: `:checkered_flag:` when fixing something on Windows
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :shirt: `:shirt:` when removing linter warnings
