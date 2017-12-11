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
        Logger.green("Sending email to {}".format(rcpt))
        Logger.log(contents)
