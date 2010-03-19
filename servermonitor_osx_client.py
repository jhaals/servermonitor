#!/usr/bin/python
# Copyright (c) 2008-2010, Johan Haals <johan.haals@gmail.com>
# All rights reserved.

from __future__ import with_statement
import urllib
import commands, re, socket

# Change this to values
id =  # Example: id = 244 (id given by servermonitor)
password = '' # Example: password = 'GHJdf76(/&sfsdgkjh' (password given by servermonitor)


# DO NOT change here unless you know what you're doing

VERSION = 'osxc_1.3' # VERION OF SERVERMONITOR
"""
VERSION sends the current version when updating.
If update notifications are enabled at the serverpanel you will get notified when a new version is avalible
"""

# Temp storage for load history
filename = '/tmp/webmonitor_load_history'
# Warn when system loads get higher then 3
threshold = 3
LOADWARNING = 0
def get_system_load():
    # Pattern to match average load values like '0.71, 1.24, 0.88'
    pattern = r'(?:(\d+(?:\.|,)\d+),?)+'

    uptime_str = commands.getoutput('uptime')

    # Find all occurances of pattern in uptime_str
    load = re.findall(pattern, uptime_str)

    # Hack for Mac
    if ',' in load[0]:
        load = [value.replace(',', '.') for value in load]

    return load

if __name__ == '__main__':
    load = get_system_load()

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Only calculate average if we have atleast 3 previous load values
        if len(lines) >= 3:
            avg = sum([float(value) for value in lines]) / len(lines)

            if avg > threshold:
                LOADWARNING = 1

            # Delete the oldest value
            del lines[0]

        lines.append(load[2] + '\n')

        with open(filename, 'w') as file:
            file.writelines(lines)

    except IOError:
        with open(filename, 'w') as file:
            file.write('%s\n' % load[2])

# Lots of commands executed.
serial = commands.getoutput('system_profiler |head -20 |grep Serial').split()[3]
df = commands.getoutput('df -h')
uname = commands.getoutput('uname -a')
uptime = commands.getoutput('uptime')
hostname = commands.getoutput('hostname')
ifconfig = commands.getoutput('/sbin/ifconfig -a')
last = commands.getoutput('last | head -20')
who = commands.getoutput('who')
dighost = commands.getoutput('dig '+hostname)
digr = commands.getoutput('dig '+hostname+' +short')
digreverse = commands.getoutput('dig -x '+digr)
sw_vers = commands.getoutput('sw_vers')

p = urllib.urlencode({'pw': password, 'hostname': hostname, 'serial': serial, 'loadwarning': LOADWARNING, 'id': id, 'who': who, 'last': last, 'dighost': dighost, 'digreverse': digreverse, 'df': df, 'uname': uname, 'uptime': uptime, 'ifconfig': ifconfig, 'version': VERSION, 'sw_vers': sw_vers})
# Send data to server
f = urllib.urlopen('http://servermonitor.se/monitor.php', p)
