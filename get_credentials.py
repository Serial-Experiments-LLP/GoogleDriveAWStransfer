#!/usr/bin/Python3

import os

from oauth2client import client

from oauth2client import tools

from oauth2client.file import Storage

import httplib2

"""

  In order to run this script you need python3 and pip3 installed.

  You also need some additional python modules. Please run

    sudo pip3 install httplib2

    sudo pip3 install --upgrade google-api-python-client



  To authenticate in Google follow the instructions at

  https://developers.google.com/drive/v3/web/quickstart/python

  A credentials.json file needs to placed in the same directory

  with this script. The link above contains the instruction on

  how to obtain this file. Once you complete these steps run

    python3 this_script.py --noauth_local_webserver

  and follow the instructions

"""


# If modifying these scopes, delete your previously saved credentials

# at ~/.credentials/drive-python-quickstart.json

SCOPES = 'https://www.googleapis.com/auth/drive.readonly' #allows read access to metadata and files

CLIENT_SECRET_FILE = 'credentials.json'

APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.



    If nothing has been stored, or if the stored credentials are invalid,

    the OAuth2 flow is completed to obtain the new credentials.



    Returns:

        Credentials, the obtained credential.

    """

    home_dir = os.path.expanduser('~')

    # credential_dir = os.path.join(home_dir, '.credentials2')
    credential_dir = 'credentials/'

    # if not os.path.exists(credential_dir):
    #     os.makedirs(credential_dir)

    # credential_path = os.path.join(credential_dir,

    #                                'drive-python-quickstart.json')

    credential_path = 'credentials/credentials.json'

    store = Storage(credential_path)

    credentials = store.get()

    if not credentials or credentials.invalid:

        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

        flow.user_agent = APPLICATION_NAME

        if flags:

            credentials = tools.run_flow(flow, store, flags)

        else:  # Needed only for compatibility with Python 2.6

            credentials = tools.run(flow, store)

        print('Storing credentials to ' + credential_path)

    return credentials
