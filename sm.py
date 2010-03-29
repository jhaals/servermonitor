#!/usr/bin/python
# Copyleft 2010 Daniel Beecham <joshu@lunix.se>
# All rights reversed.

import sys
import os
import cnf

# Modules needs to be in python path.
sys.path.append("./modules")

if __name__ == "__main__":

    # Make configparser do it's thing.
    cnf.getConfig()

    # And now, finally, include and run all modules.
    for file in os.listdir("./modules"):
        if file[-3:len(file)] == ".py":
            exec("import " + file[0:-3])
            exec(file[0:-3] + ".main()")
