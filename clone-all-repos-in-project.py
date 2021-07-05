#!/usr/bin/python3

# imports
import getpass
import json
import os
import requests
from git import Repo
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--url', required=True,
    help="[required] - The url of your bitbucket server (e.g. https://bitbucket.example.com)")
parser.add_argument('-l', '--username', required=True,
    help="[required] - The useranme to login to your bitbucket server")
parser.add_argument('-p', '--project', required=True,
    help="[required] - The project to clone the repositories from")
parser.add_argument('-b', '--basedir', required=False,
    help="[optional] - The basedir where the repositories should be cloned into")

args = parser.parse_args()

# variables
restApiEndpoint = '/rest/api/1.0/projects/'

# asking for credentials
password = getpass.getpass("Password for " + args.username + ": ")

# getting list of repositories from bitbucket server
r = requests.get(args.url + restApiEndpoint + args.project + '/repos/?limit=1000000', auth=(args.username, password))
if (r.status_code != 200):
    print ('Error contacting Bitbucket: Got status code:', r.status_code)
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
            os.makedirs(args.basedir + '/' + gitRepoName)
            print ('[cloning] ' + args.basedir + '/' + gitRepoName)
            repo = Repo.clone_from(gitCloneUrl, args.basedir + '/' + gitRepoName)

        except OSError:
            if not os.path.isdir(args.basedir + '/' + gitRepoName):
                raise
            else:
                print ('[ok]      ' + args.basedir + '/' + gitRepoName)
