#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------
# Written by https://github.com/ryanyonzon
# -----------------------------------------

import argparse
import getpass
import requests
import json

def main(args):

    owner = args.owner
    repo = args.repo
    username = args.username
    output = args.write

    password = None
    while password is None or password == '':
        password = getpass.getpass("Password for 'https://" + username + "@github.com': ")

    repo_commit_url = 'https://api.github.com/repos/' + owner + '/' + repo + '/commits'
    r = requests.get(repo_commit_url, auth=(username, password))

    if r.status_code == 200:
        json_object = json.loads(r.text)

        is_write_on_file = False
        if output is not None:
            output_file = open(output, 'wb')
            is_write_on_file = True

        for commit in json_object:
            commit_html_url = commit['html_url']
            committer = commit['author']['login']
            message = commit['commit']['message']

            commit_author = commit['commit']['author']
            commit_date = commit_author['date']

            if is_write_on_file:
                output_string = commit_date + ' - [' + committer + '] - ' + message + ' - ' + commit_html_url + "\n"
                output_file.write(bytes(output_string, 'UTF-8'))
            else:
                print(commit_date + ' - [' + committer + '] - ' + message + ' - ' + commit_html_url)
    else:
        print('Error: Unable to get repository\'s commits.')
        print('Make sure owner, repo, username and password are correct.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--owner", help="Repository owner", required=True)
    parser.add_argument("-r", "--repo", help="Repository name", required=True)
    parser.add_argument("-u", "--username", help="GitHub username", required=True)
    parser.add_argument("-w", "--write", help="Output file name (Optional)", required=False)

    args = parser.parse_args()

    main(args)
