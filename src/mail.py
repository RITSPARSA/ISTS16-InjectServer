"""
Handles all interaction with the mail servers
"""
import imaplib
import email
import json
from .log import Logger
from .config import Config

class Mail(object):
    """Manages all email functions including sending emails, get new emails, and parsing raw emails
    Connects to multiple account
    """
    def __init__(self, username, password, ip):
        self.user = username
        self.password = password
        self.server = ip
        with open(Config.get("gmail_creds")) as fil:
            cdata = json.load(fil)
        self.gmail = ImapClient(cdata["server"], cdata["port"], cdata["username"], cdata["password"])

    def send(self, contents, rcpt):
        """Send an email with the following contents
        """
        Logger.update("Sending email to {}".format(rcpt))
        Logger.plain(contents)


def parse_email(filename):
    """Parse an email file and return the subject, body, and sender address
    """
    body = ""
    subject = ""
    sender = ""
    with open(filename) as fil:
        for line in fil.readlines():
            if "From:" in line:
                sender = line.split(":", 1)[1].strip()
                continue
            if "Subject:" in line:
                subject = line.split(":", 1)[1].strip()
                continue
            body += line
    return (sender, subject, body)

class ImapClient(object):
    """An imap client capable of basic tasks
    """
    def __init__(self, server, port, username, password):
        try:
            self.server = server
            self.port = port
            self.user = username
            self.passwd = password
            self.con = imaplib.IMAP4_SSL(self.server, self.port)
            self.con.login(username, password)
            self.valid = True
            self.con.create("Team0")
        except BaseException:
            self.valid = False

    def check_mail(self, mailbox="INBOX"):
        """Check for emails in the given directory
        """
        self.con.select(mailbox)
        status, ids = self.con.search(None, "ALL")
        ids = [int(i) for i in ids[0].split()] # the ids is a list of int in a string
        retval = []
        for i in ids:
            status, emails = self.con.fetch(i, "(RFC822)")
            for item in emails:
                if isinstance(item, tuple) and len(item) > 1:
                    em = email.message_from_string(item[1])
                    em_filename = "{}.mbox".format(abs(hash(em)))
                    em_path = "{}recv/{}".format(Config.get("cache_directory"), em_filename)
                    with open(em_path,'w') as fil:
                        fil.write(em)
                        Logger.update("Saved incoming email " + em_filename)
                    retval += [(em["subject"], em["from"], em_path)]
        return retval
