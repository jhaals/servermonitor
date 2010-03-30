#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""Config module for servermonitor."""

import ConfigParser
import sys
import os
import getopt

# Global variables that modules will use.
addr = "http://servermonitor.linuxuser.se"
quiet = 0;

def parseOpts(): # {{{
    """ Parse command line arguments and make some global variables. """
    optlist, args = getopt.gnu_getopt(sys.argv, 'q')

    for opt in optlist:
        
        # quiet
        if opt[0] == '-q':
            global quiet
            quiet = 1
# }}}

def getConfig(): # {{{
    """ Find and parse configfile. """

    # Get configfile pathname. Doing this to be cross-platform.
    configpath = os.path.join(os.path.expanduser("~"), ".servermonitor.rc")

    if os.path.isfile(configpath):
        config = ConfigParser.RawConfigParser()
        config.read(configpath)

        try:
            # Import from the global scope.
            global id
            global password

            id = config.get("global", "id")
            password = config.get("global", "password")
        except ConfigParser.NoOptionError:
            # It seems there is no 'id' or 'password' in the configfile. We can't continue without it.
            print "Could not extract id and/or password from %s. Make sure it is properly configured." % configpath
            sys.exit(1)
# }}}

def main():
    """ Main function for the configuration module for servermonitor. """
    parseOpts()
    getConfig()


# vim: expandtab tabstop=4 shiftwidth=4
