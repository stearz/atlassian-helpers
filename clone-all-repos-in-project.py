#!/usr/bin/python3

# imports
import getpass
import json
import os
import requests
from git import Repo
import argparse
import validators

# variables
restApiEndpoint = '/rest/api/1.0/projects/'

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
url = args.url.rstrip("/")
username = args.username
project = args.project
basedir = args.basedir.rstrip("/")
verifyssl = False if args.noverify else True

# checking validity of variables set by arguments
if (not validators.url(url)):
    print('ERROR: %s is no valid url', url)
    exit(1)

if (not os.path.isdir(basedir)):
    print('ERROR: %s is no directory', basedir)
    exit(1)

# DIALOG - asking user for credentials
password = getpass.getpass("Password for " + username + ": ")

# getting list of repositories from bitbucket server
r = requests.get(url + restApiEndpoint + project + '/repos/?limit=1000000',
                 auth=(username, password), verify=verifyssl)
if (r.status_code != 200):
    print('Error contacting Bitbucket: Got status code:', r.status_code)
    exit(2)
else:
    myObject = json.loads(r.text)

# iterating through all repositories
for value in myObject['values']:
    gitRepoName = value['name']

    if (value['links']['clone'][1]['name'] == 'ssh'):
        gitCloneUrl = value['links']['clone'][1]['href']
    elif (value['links']['clone'][0]['name'] == 'ssh'):
        gitCloneUrl = value['links']['clone'][0]['href']
    else:
        gitCloneUrl = ''

    if (gitCloneUrl != ''):
        try:
            # cloning from origin
            os.makedirs(basedir + '/' + gitRepoName)
            print('[cloning] ' + basedir + '/' + gitRepoName)
            repo = Repo.clone_from(gitCloneUrl, basedir + '/' + gitRepoName)

        except OSError:
            if not os.path.isdir(basedir + '/' + gitRepoName):
                raise
            else:
                print('[ok]      ' + basedir + '/' + gitRepoName)
