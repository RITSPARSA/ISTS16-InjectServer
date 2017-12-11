"""
Functions that do random things
"""

from jinja2 import Template

def render(filename, **kwargs):
    contents = ""
    with open(filename) as fil:
        contents = fil.read()
    temp = Template(contents)
    return temp.render(**kwargs)

def get_injects(directory):
    """Find all the injects in a directory and return them as an
    inject object
    """
    retval = {}

    return retval
