from os.path import exists
import argparse
import getpass
import json
import sys

import praw
import prawcore

import config

FOUND_ACCOUNT_CREDENTIALS_MESSAGE = 'Found Reddit account credentials from config.py'
GET_ACCOUNT_CREDENTIALS_MESSAGE = '\nEnter Reddit account credentials:'
PASSWORD_VARIABLE_NAME = 'PASSWORD'
USER_AGENT = 'reddit-multireddit-deduplication'
USERNAME_VARIABLE_NAME = 'USERNAME'


def exit_script(message=None):
    """Print a message and exit.
    
    Keyword arguments:
    message -- the message to print before exiting (default None)
    """
    if message:
        print(message)
    else:
        print('Exiting')
    sys.exit()


def get_account_credentials(message):
    """Prompt the user to enter their Reddit account credentials and return them.
    
    Keyword arguments:
    message -- the message to prompt the user with
    """
    print(message)
    username = input('Username\n> ')
    confirm_password, password = get_password()
    while confirm_password != password:
        print("Passwords don't match. Try again? (y/n)")
        user_input = input('> ')
        if user_input == 'n':
            exit_script()
        confirm_password, password = get_password()
    return (password, username)


def get_from_file(filename, key):
    """Get the resource from the filename and return it.
    
    Keyword arguments:
    filename -- the filename
    key -- the key of the resource
    """
    if not exists(filename):
        exit_script(f"Error: {filename} doesn't exist. Exiting.")
    with open(filename) as f:
        dictionary = json.load(f)
        resource = dictionary[key]
        return resource


def get_password():
    """Prompt the user to enter their Reddit account password and return it."""
    print('Password\n> ', end='')
    password = getpass.getpass(prompt='')
    print('Confirm password\n> ', end='')
    confirm_password = getpass.getpass(prompt='')
    return (confirm_password, password)


def get_reddit(account_credentials, client_id, client_secret, message):
    """Get the PRAW Reddit instance, allowing the user to enter their Reddit account credentials again if authentication fails.
    
    Keyword arguments:
    account_credentials -- the Reddit account credentials
    client_id -- the client ID for the Reddit app
    client_secret -- the client secret for the Reddit app
    message -- the message to prompt the user with if authentication fails
    """
    while True:
        try:
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                password=account_credentials[0],
                user_agent=USER_AGENT,
                username=account_credentials[1],
            )
            reddit.user.me()
            return reddit
        except prawcore.OAuthException:
            print('\nError: Authentication failed. Would you like to try entering your Reddit account credentials again? (y/n)')
            user_input = input('> ')
            if user_input == 'n':
                exit_script()
            account_credentials = get_account_credentials(message)


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--write', action='store_true', help='Write data without confirming')
args = parser.parse_args()

targeted_multireddits = get_from_file('multireddits.json', 'multireddits')

if not args.write:
    print("Dry run, write argument wasn't found")

account_credentials = None
if hasattr(config, PASSWORD_VARIABLE_NAME) and config.PASSWORD and hasattr(config, USERNAME_VARIABLE_NAME) and config.USERNAME:
    print(FOUND_ACCOUNT_CREDENTIALS_MESSAGE)
    account_credentials = (config.PASSWORD, config.USERNAME)
else:
    account_credentials = get_account_credentials(GET_ACCOUNT_CREDENTIALS_MESSAGE)
reddit = get_reddit(account_credentials, config.CLIENT_ID, config.CLIENT_SECRET, GET_ACCOUNT_CREDENTIALS_MESSAGE)
multireddits = reddit.user.multireddits()
subreddits = set()
for multireddit in multireddits:
    if multireddit.name in targeted_multireddits:
        print('Checking multireddit', multireddit.name)
        for subreddit in multireddit.subreddits:
            if subreddit.display_name in subreddits:
                if args.write:
                    print('Removing duplicate subreddit:', subreddit.display_name)
                    multireddit.remove(subreddit)
                else:
                    print('Found duplicate subreddit:', subreddit.display_name)
            else:
                subreddits.add(subreddit.display_name)