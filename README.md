# bitbucket-helpers

This is a little toolset to make life with Atlassian Bitbucket easier.
There are these helpers:
- [clone-all-repos-in-project.py](#clone-all-repos-in-project.py)
  - let's you clone all repositories in a specified Bitbucket project
- ...

## Build status
![Tests](https://github.com/stearz/bitbucket-helpers/actions/workflows/test-latest.yml/badge.svg)
## clone-all-repos-in-project.py

### Description

This python script allows you to clone all git repositories from a Bitbucket project into a given base directory.

### Requirements

Python >= 3.6 is required with the following modules installed:

- requests
- GitPython
- validators

To install the required modules simply install them with pip:

    python3 -m pip install -r requirements.txt

### Usage

    $ python3 ./clone-all-repos-in-project.py --help
    usage: clone-all-repos-in-project.py [-h] -u URL -l USERNAME -p PROJECT -b BASEDIR [--noverify]

    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     The url of your bitbucket server (e.g. https://bitbucket.example.com)
      -l USERNAME, --username USERNAME
                            The useranme to login to your bitbucket server
      -p PROJECT, --project PROJECT
                            The project to clone the repositories from
      -b BASEDIR, --basedir BASEDIR
                            The basedir where the repositories should be cloned into
      --noverify            [optional] Disable SSL verfication by setting this parameter

### Example

    $ python3 ./clone-all-repos-in-project.py -u https://bitbucket.example.com -l my-user -b ./ -p MYPROJECT
    Password for my-user:  
    [ ... ]

### Author(s)

- Stephan Schwarz <stearz@gmx.de>
