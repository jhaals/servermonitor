#!/usr/bin/python
# Copyleft 2010 Daniel Beecham <joshu@lunix.se>
# All rights reversed.

import sys
import os
import getopt
import cnf
import urllib

# Modules needs to be in python path.
sys.path.append("./modules")

if __name__ == "__main__":
    
    VERSION = '2.0.0'
    # Make configparser do it's thing.
    cnf.main()

    # Checking for latest version.
    if not cnf.quiet:
        latest_version = urllib.urlopen(cnf.addr + "/handlers/latest.php", urllib.urlencode(''))
        print 'Now running version %s of Servermonitor.' % VERSION
        if VERSION != latest_version.read():
            print 'A later version of this software is available for download.' 

    # And now, finally, include and run all modules.
    for file in os.listdir("./modules"):
        if file[-3:] == ".py":
            exec("import " + file[0:-3])
            exec(file[0:-3] + ".main()")
    if not cnf.quiet:
        print 'Done!'
        print cnf.addr
# vim: expandtab tabstop=4 shiftwidth=4
