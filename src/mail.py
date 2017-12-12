"""
Handles all interaction with the mail servers
"""
from .log import Logger

class Mail(object):
    def __init__(self, username, password, ip):
        self.user = username
        self.password = password
        self.server = ip

    def send(self, contents, rcpt):
        Logger.update("Sending email to {}".format(rcpt))
        #Logger.plain(contents)

def parse_email(filename):
    body = ""
    subject = ""
    sender = ""
    with open(filename) as fil:
        for line in fil.readlines():
            if "From:" in line:
                sender = line.split(":",1)[1].strip()
                continue
            if "Subject:" in line:
                subject = line.split(":",1)[1].strip()
                continue
            body += line
    return (sender, subject, body)
    
