# reddit-multireddit-deduplication
Remove duplicate subreddits from a group of multireddits
## Usage
1. Clone the repository
1. [Get a Reddit client ID and client secret](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)
1. Paste your client ID and client secret in a new file named config.py in the root of the repository (DO NOT COMMIT THIS FILE)
1. Optionally put your account credentials in the config.py file (DO NOT COMMIT THIS FILE)
1. Enter your multireddits in a new file named multireddits.json in the root of the repository
1. Set up the venv: `py -m venv venv`
1. Enter the venv: `.\venv\Scripts\Activate.ps1`
1. Install the requirements: `pip install -r requirements.txt`
1. Run the script: `py main.py`

Example config.py (DO NOT COMMIT THIS FILE)
```
CLIENT_ID = ''
CLIENT_SECRET = ''

PASSWORD = ''
USERNAME = ''
```
Example multireddits.json
```
{
    "multireddits": [
        "multireddit1",
        "multireddit2"
    ]
}
```
## Optional arguments
--write (-w)
- Write data without confirming
- You will need to use this argument in order for the script to remove duplicate subreddits from your chosen multireddits
```
py main.py -w
py main.py --write
```