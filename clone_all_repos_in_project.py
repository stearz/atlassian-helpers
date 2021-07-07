#!/usr/bin/python3

# imports
import getpass
import json
import sys
import os
import argparse

import requests
from git import Repo
import validators

# constants
REST_API_ENDPOINT = '/rest/api/1.0/projects/'

# parse arguments
parser = argparse.ArgumentParser()

parser.add_argument('-u', '--url', required=True,
                    help="The url of your bitbucket server \
                          (e.g. https://bitbucket.example.com)")
parser.add_argument('-l', '--username', required=True,
                    help="The useranme to login to your bitbucket server")
parser.add_argument('-p', '--project', required=True,
                    help="The project to clone the repositories from")
parser.add_argument('-b', '--basedir', required=True,
                    help="The basedir where the repositories should be \
                          cloned into")
parser.add_argument('--noverify', action='store_true', required=False,
                    help="[optional] Disable SSL verfication by setting \
                          this parameter")

args = parser.parse_args()

# sanitizing arguments
URL = args.url.rstrip("/")
USERNAME = args.username
PROJECT = args.project
BASEDIR = args.basedir.rstrip("/")
VERIFY_SSL = not args.noverify

# checking validity of variables set by arguments
if not validators.url(URL):
    print('ERROR: %s is no valid url', URL)
    sys.exit(1)

if not os.path.isdir(BASEDIR):
    print('ERROR: %s is no directory', BASEDIR)
    sys.exit(1)

# DIALOG - asking user for credentials
password = getpass.getpass("Password for " + USERNAME + ": ")

# getting list of repositories from bitbucket server
r = requests.get(URL + REST_API_ENDPOINT + PROJECT + '/repos/?limit=1000000',
                 auth=(USERNAME, password), verify=VERIFY_SSL)
if r.status_code != 200:
    print('Error contacting Bitbucket: Got status code:', r.status_code)
    sys.exit(2)
else:
    myObject = json.loads(r.text)

# iterating through all repositories
for value in myObject['values']:
    git_repo_name = value['name']

    if value['links']['clone'][1]['name'] == 'ssh':
        GIT_CLONE_URL = value['links']['clone'][1]['href']
    elif value['links']['clone'][0]['name'] == 'ssh':
        GIT_CLONE_URL = value['links']['clone'][0]['href']
    else:
        GIT_CLONE_URL = ''

    if GIT_CLONE_URL != '':
        try:
            # cloning from origin
            os.makedirs(BASEDIR + '/' + git_repo_name)
            print('[cloning] ' + BASEDIR + '/' + git_repo_name)
            repo = Repo.clone_from(GIT_CLONE_URL, BASEDIR + '/' +
                                   git_repo_name)

        except OSError:
            if not os.path.isdir(BASEDIR + '/' + git_repo_name):
                raise
            print('[ok]      ' + BASEDIR + '/' + git_repo_name)
