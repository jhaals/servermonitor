#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send hdd usage."""

import cnf;
import commands;
import urllib;

def main():
    """servermonitor.df main function.
    Get HDD usage and send it to servermonitor servers."""

    if not cnf.quiet:
        print "df: ",

    # Get `df -h`
    output = commands.getoutput("df -h")

    # Make it parseable
    output = "||".join(["|".join(i.split()) for i in output.split("\n")[1:]])

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/df.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
