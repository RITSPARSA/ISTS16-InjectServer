"""
Pulls and writes data to google docs
"""
from apiclient import discovery

class Google(object):
    def __init__(self, apikeyfile):
        with open(apikeyfile) as fil:
            apikey = fil.read().strip()
        #self.drive = discovery.build("drive", "v3", developerKey=apikey)
        self.sheets = discovery.build("sheets", "v4", developerKey=apikey)
    def create(self, title):
        data = {
            "properties": {
                "title": "ISTS_TEST"
            }
        }
        x = self.sheets.spreadsheets()
        x.create(body = data)
