#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send info about running services."""

import cnf
import commands
import urllib
import sys

def main():
    """servermonitor.services main function.
    Get running services and send it to servermonitor servers."""

    if not cnf.quiet:
        print "services: ",

    # Get output from netstat to work with.
    if sys.platform == "darwin":
        output = commands.getoutput("netstat -f inet -an | grep LISTEN")
    else:
        output = commands.getoutput("netstat -ltun")

    result = ""
    # Get the good stuff.
    for line in output.split("\n"):
        splittedLine = line.split()
        if splittedLine[0] == "udp" or splittedLine[0] == "tcp":
            result += "|".join([splittedLine[0], splittedLine[3]]) + "||"


    # Make it a dict along with id and password.
    data = {"data":result, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/services.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
