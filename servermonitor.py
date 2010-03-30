#!/usr/bin/python
# Copyright (c) 2008-2010, Johan Haals <johan.haals@gmail.com>
# All rights reserved.

from __future__ import with_statement

import commands
import ConfigParser
import os
import re
import socket
import sys
import urllib

# configfile path.
configpath = os.path.expanduser('~') + '/.servermonitor.rc'

# Default service ports.
services = {
    'AFP': 548,
    'DNS': 53,
    'IMAP': 143,
    'LDAP': 389,
    'MySQL': 3306,
    'POP': 993,
    'SMB': 554,
    'SMTP': 25,
    'SSH': 443
}

VERSION = '2.0.0' # VERION OF SERVERMONITOR
"""
VERSION sends the current version when updating.
If update notifications are enabled at the serverpanel you will get notified when a new version is avalible
"""

# Temp storage for load history
load_history_path = '/tmp/webmonitor_load_history'
LOAD_warning = 0

def check_service(port):
    'check_service connects to a service to see if it responds.'
    serviceSocket = socket.socket()
    serviceSocket.settimeout(0.25)
    try:
        serviceSocket.connect(('localhost', port))
        serviceSocket.close()
        return 1
    except socket.error:
        return 0

if __name__ == '__main__':
    # Read configfile. {{{
    if os.path.exists(configpath) and os.path.isfile(configpath):
        config = ConfigParser.RawConfigParser()
        config.read(configpath)

        try:
            id = config.get('global', 'id')
            password = config.get('global', 'password')
        except ConfigParser.NoOptionError:
            print 'Could not extract id and/or password from %s. Make sure it is properly configured.' % configpath
            sys.exit(1)
        try:
            threshold = config.get('global', 'threshold')
        except:
            print 'Unable to extract threshold from %s. Make sure it is properly configured.' % configpath
            sys.exit(1)
        try:
            load_history_path = config.get('global', 'load_history_path')
        except:
            print 'Unable to extract load_history_path from %s. Make sure it is properly configured.' % configpath
            sys.exit(1)
    else:
        print 'Could not locate config file, make sure %s exists and is properly configured. \nCheck README for more information.' % configpath
        sys.exit(1)
    # }}}


    try:
        load = os.getloadavg()

        try:
            with open(load_history_path, 'r') as file:
                lines = file.readlines()

            # Only calculate average if we have atleast 3 previous load values
            if len(lines) >= 3:
                avg = sum([float(value) for value in lines]) / len(lines)

                if avg > threshold:
                    LOAD_warning = 1

                # Delete the oldest value
                del lines[0]

            lines.append(str(load[2]) + '\n')

            with open(load_history_path, 'w') as file:
                file.writelines(lines)

        except IOError:
            with open(load_history_path, 'w') as file:
                file.write('%.2f\n' % load[2])

    except OSError:
        # Couldn't get the system load average.
        # TODO: Log this error when a proper logging system is in place.
        pass

    # Lots of commands executed.
    df = commands.getoutput('df -h')
    uname = commands.getoutput('uname -a')
    uptime = commands.getoutput('uptime')
    hostname = commands.getoutput('hostname')
    ifconfig = commands.getoutput('/sbin/ifconfig -a')
    last = commands.getoutput('last -n 20')
    who = commands.getoutput('who')
    dighost = commands.getoutput('dig '+hostname)
    digr = commands.getoutput('dig '+hostname+' +short')
    digreverse = commands.getoutput('dig -x '+digr)

    serverinfo = {
        'password': password,
        'hostname': hostname,
        'id': id,
        'who': who,
        'last': last,
        'dighost': dighost,
        'digreverse': digreverse,
        'df': df,
        'uname': uname,
        'uptime': uptime,
        'ifconfig': ifconfig,
        'version': VERSION,
        'load': load[2]
    }

    # Extra commands for Mac, getting serial and system build
    if(sys.platform == 'darwin'):
        serial = commands.getoutput('/usr/sbin/ioreg -l | /usr/bin/grep IOPlatformSerialNumber')
        serial = re.search(r'IOPlatformSerialNumber" = "([^"]+)', serial).group(1)
        sw_vers = commands.getoutput('sw_vers')

        serverinfo.update({
            'serial': serial,
            'sw_vers': sw_vers
        })

    urllib.urlopen('http://servermonitor.linuxuser.se/monitor.php', urllib.urlencode(serverinfo))

    # Check if services are accepting connections
    for service, port in services.items():
        try:
            port = int(config.get('ports', service))

        except ValueError:
            # Couldn't convert the given port to an integer. Continue with
            # the standard port.
            # TODO: Log this error when a proper logging system is in place.
            pass

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            # No custom port configuration specified. Continue with the
            # standard port.
            pass

        services[service] = check_service(port)

    services.update({
        'id': id,
        'password': password,
        'LOAD_warning': LOAD_warning
    })

    # Sending info over running services.
    servicesHandle = urllib.urlencode(services)
    urllib.urlopen('http://servermonitor.linuxuser.se/services.php', servicesHandle)

# vim: set expandtab shiftwidth=4 tabstop=4
