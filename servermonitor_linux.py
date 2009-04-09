#!/usr/bin/python
#    Copyleft 2008-2009 Servermonitor
#    Servermonitor is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Servermonitor is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Servermonitor.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement
import urllib
import commands, re

# Change this to values
id = # Example: id = 244 (id given by servermonitor)
password = "" # Example: password = "GHJdf76(/&sfsdgkjh" (password given by servermonitor)


# DO NOT change here unless you know what you're doing

VERSION = 'linux_1.3' # VERION OF SERVERMONITOR
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
p = urllib.urlencode({'pw': password, 'hostname': hostname, 'id': id, 'who': who, 'last': last, 'dighost': dighost, 'digreverse': digreverse, 'df': df, 'uname': uname, 'uptime': uptime, 'ifconfig': ifconfig, 'version': VERSION})
f = urllib.urlopen('http://servermonitor.se/monitor.php', p)

