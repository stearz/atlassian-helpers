# Bitbucket helpers

## clone-all-repos-in-project.py

### description

This python script allows you to clone and update all git repositories from a Bitbucket project into a given base directory.

### requirements

Python 3 is required with the following modules (see reqiurements.txt)

- requests
- GitPython
- argparse

### example usage

    $ ../clone-all-repos-in-project.py -u https://bitbucket.example.com -l my-user -b ./ -p MYPROJECT
    Password for my-user:  
    [ ... ]

### authors

- Stephan Schwarz <stearz@gmx.de>
