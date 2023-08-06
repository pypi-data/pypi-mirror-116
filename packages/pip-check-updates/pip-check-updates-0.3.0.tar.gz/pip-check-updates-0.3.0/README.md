<div align="center">
    <img src="https://cdn2.iconfinder.com/data/icons/flat-jewels-icon-set/512/0000_Refresh.png" alt="logo" height="196">
</div>

# pip-check-updates

[![pytest](https://github.com/zehengl/pip-check-updates/actions/workflows/pytest.yml/badge.svg)](https://github.com/zehengl/pip-check-updates/actions/workflows/pytest.yml)
![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)
![PyPI - License](https://img.shields.io/pypi/l/pip-check-updates)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pip-check-updates)
![PyPI - License](https://img.shields.io/pypi/l/pip-check-updates)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pip-check-updates)

A tool to upgrade dependencies to the latest versions, inspired by [npm-check-updates](https://www.npmjs.com/package/npm-check-updates)

## Install

From [PyPi](https://pypi.org/project/pip-check-updates/)

    pip install pip-check-updates

From [GitHub](https://github.com/zehengl/pip-check-updates)

    pip install git+https://github.com/zehengl/pip-check-updates.git

## Usage

Show any new dependencies for the project in the current directory:

- Red = major upgrade
- Cyan = minor upgrade
- Green = patch upgrade

```terminal
pcu
```

    Checking dependencies
    100%|████████████████████| 6/6 [00:01<00:00,  5.75it/s]

    In requirements.txt

    tqdm    4.62.0  →  4.62.1
    pandas  0.25.3  →  1.3.2
    Django  3.1.13  →  3.2.6

    Run pcu -u to upgrade requirements.txt

Upgrade a project's requirements file:

```terminal
pcu -u
```

    Upgrading dependencies
    100%|████████████████████| 6/6 [00:01<00:00,  5.84it/s]

    In requirements.txt

    tqdm    4.62.0  →  4.62.1
    pandas  0.25.3  →  1.3.2
    Django  3.1.13  →  3.2.6

    Run pip install -r ... to install new versions

Specify requirements file if needed, `-r` option will be recognized as well:

```terminal
pcu requirements-dev.txt
```

    Checking dependencies
    100%|████████████████████| 10/10 [00:01<00:00,  6.05it/s]

    In requirements.txt

    tqdm    4.62.0  →  4.62.1
    pandas  0.25.3  →  1.3.2
    Django  3.1.13  →  3.2.6

    In requirements-dev.txt

    black   21.6b0  →  21.7b0
    pylint  2.9.3   →  2.9.6
    pytest  5.4.3   →  6.2.4

    Run pcu -u to upgrade requirements.txt and requirements-dev.txt

Target version:

```terminal
pcu requirements-dev.txt -t patch
```

    Checking dependencies
    100%|████████████████████| 10/10 [00:02<00:00,  4.73it/s]

    In requirements.txt

    tqdm  4.62.0  →  4.62.1

    In requirements-dev.txt

    pylint  2.9.3  →  2.9.6

    Run pcu -u to upgrade requirements.txt and requirements-dev.txt

Show the helper text:

```terminal
pcu -h
```

    usage: pcu [-h] [-u] [-t {latest,newest,greatest,minor,patch}] [path]

    pip-check-updates.

    positional arguments:
    path                  specify path to a requirements file

    optional arguments:
    -h, --help            show this help message and exit
    -u, --upgrade         overwrite package file with upgraded versions instead of just outputting to console.
    -f FILTER [FILTER ...], --filter FILTER [FILTER ...]
                            include only package names matching the given string.
    -t {latest,newest,greatest,minor,patch}, --target {latest,newest,greatest,minor,patch}
                            target version to upgrade to: latest, newest, greatest, minor, patch.
    --no_ssl_verify       disable SSL verification.

## Test

    python setup.py test

## Credits

- [Icon](https://www.iconfinder.com/icons/171269/refresh_icon) by PixelKit
