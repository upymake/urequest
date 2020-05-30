![Screenshot](icon.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/upymake/urequest.svg?branch=master)](https://travis-ci.org/upymake/urequest)
[![Coverage Status](https://coveralls.io/repos/github/upymake/urequest/badge.svg?branch=master)](https://coveralls.io/github/upymake/urequest?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with pylint](https://img.shields.io/badge/pylint-checked-blue)](https://www.pylint.org)
[![Checked with flake8](https://img.shields.io/badge/flake8-checked-blue)](http://flake8.pycqa.org/)
[![Checked with pydocstyle](https://img.shields.io/badge/pydocstyle-checked-yellowgreen)](http://www.pydocstyle.org/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)
[![PyPI version shields.io](https://img.shields.io/pypi/v/urequest.svg)](https://pypi.python.org/pypi/urequest/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/urequest.svg)](https://pypi.python.org/pypi/urequest/)
[![Downloads](https://pepy.tech/badge/urequest)](https://pepy.tech/project/urequest)
[![CodeFactor](https://www.codefactor.io/repository/github/upymake/urequest/badge)](https://www.codefactor.io/repository/github/upymake/urequest)

# uRequest

> Provides user-friendly micro HTTP client with nothing but clean objects.
>
> Basically, it is a wrapper over **requests** python library. For asynchronous version please check [aiorequest](https://github.com/aiopymake/aiorequest) package.

## Tools

- python 3.6, 3.7, 3.8
- [requests](https://requests.readthedocs.io/en/master) library
- [travis](https://travis-ci.org/) CI
- code analysis
  - [pytest](https://pypi.org/project/pytest/)
  - [black](https://black.readthedocs.io/en/stable/)
  - [mypy](http://mypy.readthedocs.io/en/latest)
  - [pylint](https://www.pylint.org/)
  - [flake8](http://flake8.pycqa.org/en/latest/)

## Usage

### Installation

Please run following script to obtain latest package from PYPI:
```bash
pip install urequest
✨ 🍰 ✨
```
### Quick start

```python
>>> from urequest.session import Session, HttpSession
>>> from urequest.response import Response
>>> from urequest.url import HttpUrl
>>>
>>> session: Session
>>> with HttpSession() as session:
...     response: Response = session.get(HttpUrl(host="xkcd.com", path="info.0.json"))
...     response.is_ok()
...     response.as_json()
...
True
{
    "month": "3",
    "num": 2284,
    "link": "",
    "year": "2020",
    "news": "",
    "safe_title": "Sabotage",
    "transcript": "",
    "alt": "So excited to see everyone after my cruise home from the World Handshake Championships!",
    "img": "https://imgs.xkcd.com/comics/sabotage.png",
    "title": "Sabotage",
    "day": "23",
}
```
### Source code

```bash
git clone git@github.com:vyahello/urequest.git
python setup.py install
```

Or using specific release:
```bash
pip install git+https://github.com/vyahello/urequest@0.0.1
```

### Local debug

```bash
git clone git@github.com:aiopymake/aiorequest.git
```

```python
>>> import urequest
>>> urequest.__doc__
'Provides user-friendly HTTP client with clean objects.'
```

**[⬆ back to top](#urequest)**

## Development notes

### CI

Project has Travis CI integration using [.travis.yml](.travis.yml) file thus code analysis (`black`, `pylint`, `flake8`, `mypy`, `pydocstyle`) and unittests (`pytest`) will be run automatically after every made change to the repository.

To be able to run code analysis, please execute command below:
```bash
./analyse-source-code.sh
```
### Release notes

Please check [changelog](CHANGELOG.md) file to get more details about actual versions and it's release notes.

### Meta

Author – _Volodymyr Yahello_. Please check [AUTHORS](AUTHORS.md) file for all contributors.

Distributed under the `MIT` license. See [LICENSE](LICENSE.md) for more information.

You can reach out me at:
* [vyahello@gmail.com](vyahello@gmail.com)
* [https://github.com/vyahello](https://github.com/vyahello)
* [https://www.linkedin.com/in/volodymyr-yahello-821746127](https://www.linkedin.com/in/volodymyr-yahello-821746127)

### Contributing
1. clone the repository
2. configure Git for the first time after cloning with your `name` and `email`
3. `pip install -r requirements.txt` to install all project dependencies
4. `pip install -r requirements-dev.txt` to install all development project dependencies

**[⬆ back to top](#urequest)**
