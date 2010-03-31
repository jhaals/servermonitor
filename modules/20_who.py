#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and info of currentl logged in users."""

import cnf;
import commands;
import urllib;

def main():
    """servermonitor.who main function.
    Get `who` and send it to servermonitor servers."""

    if not cnf.quiet:
        print "who: ",

    # Get `who`
    output = commands.getoutput("who")

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/who.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
