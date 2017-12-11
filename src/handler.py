"""
Parses incoming emails and sends autoreply
"""

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
        template = None # the template to render during the return
        data = {} # All the data that goes into a jinja template
        data["inject_subject"] = subject
        try:
            data.update(self.parse_subject(subject)) # get team and inject num
        except:
            template = self.temps.invalid # Send the invalid template warning
            template = template.render(**data)
            Logger.log("{}: INVALID EMAIL: Sending reply..."
                        .format(sender))
            self.mail.send(template, sender)
            return False
 
        inject = self.injects.get(data["inject_number"]) # The inject we got
        data["inject_name"] = inject.name
        if inject.islate():
            template = self.temps.late # Send the late submission warning
            template = template.render(**data)
            Logger.log(
                "{}: TEAM {}: LATE SUBMISSION for Inject {}."
                .format(sender, data["team_number"], data["inject_number"]))
            self.mail.send(template, sender)
            return False
        # At this point we assume the inject is a valid submission
        # Send the inject confirmation
        template = self.temps.valid # Send the confirmation
        template = template.render(**data)
        Logger.log(
            "{}: TEAM {}: ON-TIME SUBMISSION for Inject {}."
            .format(sender, data["team_number"], data["inject_number"]))
        self.mail.send(template, sender)
        # Now we check if there is a follow up inject
        nxt = inject.next_path()
        if nxt is None:
            # Send a message that the inject path is complete
            # TODO
            pass
        else:
            # Send the next inject in the path if they have completed it
            # TODO
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


