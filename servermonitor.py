#!/usr/bin/python
# Copyleft 2010 Daniel Beecham <joshu@lunix.se>
# All rights reversed.

import sys
import os
import getopt
import cnf

# Modules needs to be in python path.
sys.path.append("./modules")

if __name__ == "__main__":

    VERSION = '2.0.0'
    # Make configparser do it's thing.
    cnf.main()
    if not cnf.quiet:
        print 'Now running version %s of Servermonitor' % VERSION

    # And now, finally, include and run all modules.
    for file in os.listdir("./modules"):
        if file[-3:] == ".py":
            exec("import " + file[0:-3])
            exec(file[0:-3] + ".main()")
    if not cnf.quiet:
        print 'Done!'
# vim: expandtab tabstop=4 shiftwidth=4
