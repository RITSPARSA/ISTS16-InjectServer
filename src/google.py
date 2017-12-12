"""
Pulls and writes data to google docs
This acts as the "db" for the software.
Some of this code is ripped from googles website.

Author: Micah Martin (mjm5097@rit.edu)
"""

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import os
import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# Required variables for the google API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
APPLICATION_NAME = 'ISTS Engine'

class Google(object):
    def __init__(self, keyfile):
        self.get_credentials(keyfile)
        http = self.key.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                            'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                    discoveryServiceUrl=discoveryUrl)
        self.sheetId = "12yVwEkMVWOQ4udcDwJ9mp7HgMyIymc5Rsk8dO05mFGo"
    
    def get_credentials(self, cred_file):
        """Gets valid user credentials from storage.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, "ists_engine.json")
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(cred_file, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
        self.key = credentials
    
    def get_cell(self, rang):
        """Return all the values at the given range
        """
        # Build the API object
        render_option = "UNFORMATTED_VALUE"
        request = self.service.spreadsheets().values().get(
                    spreadsheetId=self.sheetId, range=rang,
                    valueRenderOption=render_option)
        response = request.execute()
        try:
            vs = response["values"]
            return vs[0]
            pass
        except:
            return []

    def set_cell(self, rang, value):
        """Set the value of a given cell. Only supports one at a time
        """
        render_option = "UNFORMATTED_VALUE"
        input_option = "RAW"
        # Add the new value to the API body
        body = { "values": [[value]] }
        request = self.service.spreadsheets().values().update(
                    spreadsheetId=self.sheetId, range=rang,
                    responseValueRenderOption=render_option,
                    includeValuesInResponse=True,
                    valueInputOption=input_option,
                    body=body)
        response = request.execute()
        try:
            # Validate that the data by checking against the sent data
            return response["updatedData"]["values"][0][0] == value
        except:
            # If there is any error, assume it didnt work
            return False

