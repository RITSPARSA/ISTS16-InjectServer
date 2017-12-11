"""
Parses incoming emails and sends autoreply
"""
from . import files
from .log import Logger
from .config import Config
from .mail import Mail
from .injects import Injects
from .templates import Templates

class Handler(object):
    """This class figures out what to do with received emails
    """
    def __init__(self):
        self.injects = Injects(Config.inject_directory)
        self.mail = Mail("u", "p", "pass")
        self.temps = Templates(Config.template_directory)

    def handle(self, sender, subject, body, attachments=[]):
        """Handle an email coming from the blue teams
        """
        def is_complete(data):
            """Makes sure that all minor paths before this inject are complete
            """
            complete = []
            hi, lo = str(data["inject_number"]).split(".")
            if lo == "1":
                return True # If its a base inject, say path is complete
            tn = data["team_number"]
            for i in range(1, int(lo)):
                inject = ".".join((hi, str(i)))
                if not files.is_tagged(tn, inject, "complete"):
                    Logger.warn("Team {} did not complete inject {}".format(tn,
                                    inject))
                    return False
            return True

        template = None # the template to render during the return
        data = {} # All the data that goes into a jinja template
        data["inject_subject"] = subject
        data["sender"] = sender
        # See if the inject is a valid format
        try:
            data.update(self.parse_subject(subject)) # get team and inject num
        except:
            data["log"] = "{}: INVALID SUBJECT: {}".format(sender, subject)
            self.send_template(self.temps.invalid, data)
            return False
        
        if not self.injects.isinject(data["inject_number"]):
            data["log"] = "{}: INVALID INJECT: {}".format(sender, subject)
            self.send_template(self.temps.invalid, data)
            return False
        
        # See if the inject is late
        inject = self.injects.get(data["inject_number"]) # The inject we got
        data["inject_name"] = inject.name
        if inject.islate():
            data["warn"] = "{}: TEAM {}: LATE SUBMISSION for Inject {}."\
                .format(sender, data["team_number"], data["inject_number"])
            self.send_template(self.temps.late, data)
            files.mark_tag(data["team_number"], data["inject_number"],
                                "late")
            return False
            
        # At this point we assume the inject is a valid submission
        if not is_complete(data):
            data["warn"] = "{}: TEAM {}: EARLY SUBMISSION for Inject {}."\
                .format(sender, data["team_number"], data["inject_number"])
            self.send_template(self.temps.invalid, data)
            files.mark_tag(data["team_number"], data["inject_number"],
                                "late")
            return False

        
        # Send the inject confirmation
        data["log"] = "{}: TEAM {}: ON-TIME SUBMISSION for Inject {}."\
            .format(sender, data["team_number"], data["inject_number"])
        self.send_template(self.temps.valid, data)
        files.mark_tag(data["team_number"], data["inject_number"],
                                "complete")
        # Now we check if there is a follow up inject
        nxt = self.injects.next_path(inject)
        if nxt is not None:
            # Send the next inject in the path if they have completed it
            # TODO
            pass
        else:
            # Send a message that the inject path is complete
            # TODO
            Logger.green("inject complete for {}".format(int(float(inject.number))))
            pass
        return False

    def parse_subject(self, subject):
        """Parse a subject line to see if the information is valid
        """
        try:
            team, inject = subject.lower().split(":", 1) # Split the line to 
            team_number = None
            for w in team.split():
                # Find the team number
                try:
                    team_number = int(w)
                except:
                    continue
            if team_number is None:
                # Not a valid subject line
                raise BaseException 

            inject_number = None
            for w in inject.split():
                # Find the inject number
                try:
                    inject_number = float(w)
                except:
                    continue
            if inject_number is None:
                # Not a valid subject line
                raise BaseException 
            return {"team_number":team_number, "inject_number":inject_number}
        except:
            # Not a valid subject line
            raise ValueError("Invalid subject line {}".format(subject))


    def send_template(self, template, data):
            x = data.pop("log",False)
            if x is not False:
                Logger.log(x)
            x = data.pop("warn",False)
            if x is not False:
                Logger.warn(x)
            
            sender = data.pop("sender")
            template = template.render(**data)
            self.mail.send(template, sender)
        
