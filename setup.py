"""
Manual setup file for oshyreman

oshyreman is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

oshyreman is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with oshyreman.  If not, see <http://www.gnu.org/licenses/>.

Run with 
    python setup.py build /         - or
    python setup.py install /
"""

import sys
import os
import os.path
import shutil

filesToMove = [
               ['build/oshyreman.desktop', 'usr/share/applications', 'oshyreman.desktop'], 
               ]
filesToLink = [
               ['../../opt/oshyreman/oshyreman_gui.py', 'usr/bin','oshyreman'], 
               ]


def doBuild(path):
    pass

def doInstall(path):
    print "installing oshyreman"
    basedir = os.path.join(path, 'opt/oshyreman')
    if not os.path.exists(os.path.join(path, 'opt/')):
        os.mkdir(os.path.join(path, 'opt/'))
    shutil.copytree(os.getcwdu(), basedir, ignore = shutil.ignore_patterns('debian'))
    for entry in filesToMove:
        dir = os.path.join(path, entry[1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.move(os.path.join(basedir, entry[0]), os.path.join(path, entry[1], entry[2]))
    for entry in filesToLink:
        destDir = os.path.join(path, entry[1])
        if not os.path.exists(destDir):
            os.makedirs(destDir)
        os.symlink(entry[0], os.path.join(destDir, entry[2]))            

if __name__ == "__main__":
    if sys.argv[1] == 'build':
        doBuild(sys.argv[2])
    elif sys.argv[1] == 'install':
        if sys.argv[2].startswith('--root='):
            dest = sys.argv[2][7:]
        else:
            dest = sys.argv[2]
        doInstall(dest)
    elif sys.argv[1] == 'clean':
        pass
    else:
        print "Unknown command"
        sys.exit(1)

