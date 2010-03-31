#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send uname info."""

import cnf;
import commands;
import urllib;

def main():
    """servermonitor.uname main function.
    Get uname info and send it to servermonitor servers."""

    if not cnf.quiet:
        print "uname: ",

    # Extract information
    kernelName = commands.getoutput("uname -s")
    kernelRelease = commands.getoutput("uname -r")
    machineHardware = commands.getoutput("uname -m")

    output = "|".join([kernelName, kernelRelease, machineHardware])

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/uname.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
