#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send load average."""

import cnf;
import commands;
import urllib;
from os import getloadavg

def main():
    """servermonitor.load main function.
    Get load average and send it to servermonitor servers."""

    if not cnf.quiet:
        print "load: ",

    # Get load average
    output = getloadavg()[2]

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/load.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
