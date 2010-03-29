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

    # Get `df -h`
    output = commands.getoutput("df -h")

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    urllib.urlopen(cnf.addr + "/handlers/df.php", urllib.urlencode(data))
