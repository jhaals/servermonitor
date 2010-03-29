#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send hostname."""

import cnf;
import commands;
import urllib;

def main():
    """servermonitor.hostname main function.
    Get hostname and send it to servermonitor servers."""

    # Get `hostname`
    output = commands.getoutput("hostname")

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/hostname.php", urllib.urlencode(data))
    print "hostname: " + handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
