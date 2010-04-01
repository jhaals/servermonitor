#!/usr/bin/python
# Copyleft 2010, Daniel Beecham <joshu@lunix.se>
# All rights reversed.

"""This module will get and send Mac serial, system build and Mac OS X version."""

import cnf
import commands
import urllib
import sys
import re
def main():
    """servermonitor.mac main function."""

    if not cnf.quiet:
        print "Serial+Build: ",

    # Get serial number
    serial = commands.getoutput('/usr/sbin/ioreg -l | /usr/bin/grep IOPlatformSerialNumber')	 	
    serial = re.search(r'IOPlatformSerialNumber" = "([^"]+)', serial).group(1)
    
    # Get Mac OS X version and system build
    sw_vers = commands.getoutput('sw_vers')
    osx_version = sw_vers.split(':')[2].split('\n')[0].replace('\t','')
    build_version = sw_vers.split(':')[3].replace('\t','')

    # Make it a dict along with id and password.
    data = {'serial':serial, 'build_version':build_version, 'osx_version':osx_version,'id':cnf.id, 'password':cnf.password}

    # And send it.
    handle = urllib.urlopen(cnf.addr + "/handlers/mac.php", urllib.urlencode(data))

    if not cnf.quiet:
        print handle.read()

# vim: expandtab tabstop=4 shiftwidth=4
