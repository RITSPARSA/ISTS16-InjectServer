"""
Pulls and writes data to google docs
"""
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import os
import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'config.txt'
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
    
    def get_inject_col(self, inject):
        try:
            h,l = str(float(inject)).split(".")
            col = chr(65+int(l)+1)
            row = int(h)+1
            return "{}{}".format(col,row)
        except:
            raise BaseException("Invalid inject {}".format(inject))

    def get_range(self, team, col, end=None):
        """Generate a API range based on the team and the column
        """
        if end != None:
            col = col+":"+end
        rang = "Team{}!{}".format(team, col)
        return rang

    def get_cell(self, team, rang):
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

    def set_cell(self, team, col, value):
        rang = self.get_range(team, col)
        render_option = "UNFORMATTED_VALUE"
        input_option = "USER_ENTERED"
        body = { "values": [[value]] }
        request = self.service.spreadsheets().values().update(
                    spreadsheetId=self.sheetId, range=rang,
                    responseValueRenderOption=render_option,
                    includeValuesInResponse=True,
                    valueInputOption=input_option,
                    body=body)
        response = request.execute()
        try:
            # Validate that the data was updated
            return response["updatedData"]["values"][0][0] == value
            pass
        except:
            return False

    def is_submitted(self, team, inject):
        col = self.get_range(team, self.get_inject_col(inject))
        val = self.get_cell(team, col)
        try:
            return val[0] == True
        except:
            return False
    
    def is_valid(self, team, inject):
        try:
            h,l = str(float(inject)).split(".")
            start = self.get_inject_col(h+".0")
            if l != str(0):
                rang = self.get_range(team, start, self.get_inject_col(inject))
            else:
                rang = self.get_range(team, start)
            result = self.get_cell(team, rang)
            return all(result) and len(result) > 0
        except:
            raise BaseException("Invalid inject {}".format(inject))
