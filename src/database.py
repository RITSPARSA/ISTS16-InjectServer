"""
Pulls and writes data to google docs
This acts as the "db" for the software.
Some of this code is ripped from googles website.

Author: Micah Martin (mjm5097@rit.edu)
"""
from .google import Google

class Database(object):
    """This class abstracts the Google API into a generic DB.
    These functions should be maintained if another database is used
    """
    def __init__(self, config):
        """
        Build a Google db object
        """
        self.db = Google(config)

    def is_submitted(self, team, inject):
        """Check if an inject has been submitted for a team
        """
        try:
            # Get the range for the given cell
            col = self.calc_range(team, self.calc_location(inject))
            # Get the value at that cell
            val = self.db.get_cell(col)
            # If the value is True, return true
            return val[0] == True
        except:
            return False
    
    def is_path_complete(self, team, inject):
        """Check if all other injects in the path have been submitted
        """
        try:
            # Get the high and low value
            h,l = str(float(inject)).split(".")
            if l == str(0):
                # If its a base inject, The path is always complete
                return True
            
            # If we are not working with the base inject (e.g. 2.0), then
            # then the start is the base and the end is the end
            start = self.calc_location(h+".0")
            # Check the inject before ourselves, not ourself
            end = self.calc_location(float(inject)-0.1)
            # Get the range between the cells
            rang = self.calc_range(team, start, end)
            # Get all the values for the range
            result = self.db.get_cell(rang)
            # If all the values are True, and there is values, return true
            return all(result) and len(result) == int(l)
        except:
            # Error on anything else
            raise BaseException("Invalid inject {}".format(inject))
    
    def calc_location(self, inject):
        """Find return the cell that contains information about this inject
        """
        try:
            # Get the major inject number and minor inject number
            h,l = str(float(inject)).split(".")
            # The coloumns are A-Z, Move forward 1 as the first Col is a label
            col = chr(65+int(l)+1)
            # The row is the normal row but offset 1 for the labels
            row = int(h)+1
            return "{}{}".format(col,row)
        except:
            raise BaseException("Invalid inject {}".format(inject))

    def calc_range(self, team, col, end=None):
        """Generate a cell based on the team and the column
        """
        if end != None:
            col = col+":"+end
        rang = "Team{}!{}".format(team, col)
        return rang

    def set_late(self, team, inject):
        """Mark an inject as late, Only Primary/Base injects can be late
        """
        # The col is H and then row is the inject number + 1
        cell = "H{}".format(int(inject) + 1)
        # Get the range to set
        rang = self.calc_range(team, cell)
        return self.db.set_cell(rang, True)
    
    def set_submitted(self, team, inject):
        """Mark an inject as submitted for a team
        """
        try:
            rang = self.calc_range(team, self.calc_location(inject))
            return self.db.set_cell(rang, True)
        except:
            return False
