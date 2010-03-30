#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send uptime info."""

import cnf;
import commands;
import urllib;

def main():
    """servermonitor.uptime main function.
    Get uptime and send it to servermonitor servers."""

    if not cnf.quiet:
        print "uptime: ",

    # Get `uptime`
    output = commands.getoutput("uptime")

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/uptime.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
