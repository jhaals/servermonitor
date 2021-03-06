#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send ifconfig info."""

import cnf;
import commands;
import urllib;

def main():
    """servermonitor.ifconfig main function.
    Get interface info and send it to servermonitor servers."""

    if not cnf.quiet:
        print "ifconfig: ",

    # Get `ifconfig`
    output = commands.getoutput("ifconfig -a")

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/ifconfig.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
