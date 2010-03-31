#!/usr/bin/python
# Copyleft 2010 Daniel Beecham <joshu@lunix.se>
# All rights reversed.

import sys
import os
import getopt
import cnf
import urllib


def runModules(): # {{{
    """ Import and run all modules. """

    if cnf.modulepath != "":
        modulepath = cnf.modulepath
    else:
        modulepath = "./modules"


    for file in os.listdir(modulepath).sort():
        if file[-3:] == ".py":
            exec("import " + file[0:-3])
            exec(file[0:-3] + ".main()")
    if not cnf.quiet:
        print 'Done!'
# }}}

if __name__ == "__main__":
    
    VERSION = '2.0.0'
    # Make configparser do it's thing.
    cnf.main()

    # We need a path to the modules.
    if cnf.modulepath != "":
        sys.path.append(cnf.modulepath)
    else:
        sys.path.append("./modules")

    # Checking for latest version.
    if not cnf.quiet:
        latest_version = urllib.urlopen(cnf.addr + "/handlers/latest.php", urllib.urlencode(''))
        print 'Now running version %s of Servermonitor.' % VERSION
        if VERSION != latest_version.read():
            print 'A later version of this software is available for download.' 

    if cnf.daemon:
        import daemon
        import time
        with daemon.DaemonContext():
            while 1:
                runModules();
                time.sleep(60*18)

    else: runModules()

# vim: expandtab tabstop=4 shiftwidth=4
