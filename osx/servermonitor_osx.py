#!/usr/bin/python
# Copyright (c) 2008-2010, Johan Haals <johan.haals@gmail.com>
# All rights reserved.

from __future__ import with_statement
import commands, re, socket, ConfigParser, os, sys, urllib

# configfile path.
configpath = os.path.expanduser("~") + "/.servermonitor.rc"

# Default service ports.
services = {"SSH":443, "SMTP":25, "IMAP":143, "POP":993, "AFP":548, "SMB":554, "MySQL":3306, "DNS":53, "LDAP":389}

VERSION = 'osxc_1.45' # VERION OF SERVERMONITOR
"""
VERSION sends the current version when updating.
If update notifications are enabled at the serverpanel you will get notified when a new version is avalible
"""

# Temp storage for load history
filename = '/tmp/webmonitor_load_history'
# Warn when system loads get higher then 3
threshold = 3
LOAD_warning = 0

def get_system_load(): # {{{
    # Pattern to match average load values like '0.71, 1.24, 0.88'
    pattern = r'(?:(\d+(?:\.|,)\d+),?)+'

    uptime_str = commands.getoutput('uptime')

    # Find all occurances of pattern in uptime_str
    load = re.findall(pattern, uptime_str)

    # Hack for Mac
    if ',' in load[0]:
        load = [value.replace(',', '.') for value in load]

    return load
# }}}

def CheckService(port): # {{{
    "CheckService connects to a service to see if it responds."
    serviceSocket = socket.socket()
    serviceSocket.settimeout(0.25)
    try:
        serviceSocket.connect(('localhost', port))
        serviceSocket.close()
        return True
    except socket.error:
        return False
# }}}

if __name__ == '__main__':
    # Read configfile. {{{
    if os.path.exists(configpath) and os.path.isfile(configpath):
        config = ConfigParser.RawConfigParser()
        config.read(configpath)

        try:
            id = config.get("global", "id")
            password = config.get("global", "password")
        except ConfigParser.NoOptionError:
            print "Could not extract id and/or password from " + configpath + ". Make sure it is properly configured."
            sys.exit(1)
    else:
        print "Could not locate config file, make sure " + configpath + " exists and is properly configured. \nCheck README for more information."
        sys.exit(1)
    # }}}


    load = get_system_load()

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Only calculate average if we have atleast 3 previous load values
        if len(lines) >= 3:
            avg = sum([float(value) for value in lines]) / len(lines)

            if avg > threshold:
                LOAD_warning = 1

            # Delete the oldest value
            del lines[0]

        lines.append(load[2] + '\n')

        with open(filename, 'w') as file:
            file.writelines(lines)

    except IOError:
        with open(filename, 'w') as file:
            file.write('%s\n' % load[2])


# Lots of commands executed.
serial = commands.getoutput('/usr/sbin/ioreg -l | /usr/bin/grep IOPlatformSerialNumber')
serial = re.search(r'IOPlatformSerialNumber" = "([^"]+)', serial).group(1)
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
load = re.findall('(\d+[,.]\d+)', uptime)[2] # getting the 15min load for building a graph.


serverinfo = urllib.urlencode({'password': password, 'hostname': hostname, 'serial': serial, 'id': id, 'who': who, 'last': last, 'dighost': dighost, 'digreverse': digreverse, 'df': df, 'uname': uname, 'uptime': uptime, 'ifconfig': ifconfig, 'version': VERSION, 'sw_vers': sw_vers, 'load': load})
# Send data to server
f = urllib.urlopen('http://servermonitor.linuxuser.se/monitor.php', serverinfo)

for service, value in services.items():
    try:
        port = config.get("ports", str(service))
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        port = value

    services[service] = 1 if CheckService(int(port)) else 0

services.update({"id":id, "password":password, "LOAD_warning":LOAD_warning});

# Sending info over running services.
servicesHandle = urllib.urlencode(services);
f = urllib.urlopen('http://servermonitor.linuxuser.se/services.php', servicesHandle)

# vim: set expandtab shiftwidth=4 tabstop=4
