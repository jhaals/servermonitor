#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send DNS lookup information."""

import cnf;
import commands;
import urllib;


# TODO:
# This module needs to check reverse DNS info aswell
# we just need to code something stable (probably with regexp, or a DNS library)

def main():
    """servermonitor.dig main function.
    Get DSN lookup information and send it to servermonitor servers."""

    # Get `hostname`
    hostname = commands.getoutput("hostname")
    
    # And now dig hostname
    output = commands.getoutput("dig " + hostname)

    # Make it a dict along with id and password.
    data = {"data":output, "id":cnf.id, "password":cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/dig.php", urllib.urlencode(data))
    print "dig: " + handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
