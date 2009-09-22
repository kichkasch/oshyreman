import os.path

#
# GENERAL
#
PATH_LOCAL_DATA = "/home/michael/.offline_shrmanager"
HOST_REMOTE = "192.168.0.202"
USER_REMOTE = "root"    # make sure, this user can login without password

PROGRAM_NAME = "Offline SHR Manager"
PROGRAM_VERSION = "0.0.1"
FILEPATH_COPYING = "./COPYING"
PROGRAM_AUTHORS = ['Michael Pilgermann']
PROGRAM_COMMENTS = "Automate recurring activities for the Freerunner from your Desktop."
PROGRAM_HOMEPAGE = "http://projects.openmoko.org/projects/oshyreman/"

#
# GPS Domain
#
PATH_LOCAL_MAPS = os.path.join(PATH_LOCAL_DATA, "Maps")
PATH_REMOTE_MAPS = "/home/root/Maps"


#
# Backup Domain
#
PATH_LOCAL_BACKUPS = os.path.join(PATH_LOCAL_DATA, "Backup")
BACKUP_FILES = [
    '/home/root/.pisi/conf', 
    '/etc/freesmartphone/opim/sqlite-contacts.db', 
    '/etc/freesmartphone/opim/sqlite-calls.db', 
    '/etc/freesmartphone/opim/sqlite-messages.db', 
    '/home/root/.evolution/calendar/local/system/calendar.ics']


#
# Config domain
#
PATH_LOCAL_CONFIG = os.path.join(PATH_LOCAL_DATA, "Config")
TMPFILE_LOCAL_CONFIG = os.path.join(PATH_LOCAL_CONFIG, "conf.tmp")
CONFIG_FILES = {'PISI Config File': '/home/root/.pisi/conf', 
        'Frameworkd': '/etc/frameworkd.conf', 
        'Test': '/tmp/test.txt'}
#PROGRAM_EDIT = '/usr/bin/kate'
PROGRAM_EDIT = '/usr/bin/gedit'

#
# System information domain
#
INFO_GROUPS = {'Hardware':['Processor', 'Hardware', 'Revision'], 'Operating System':['Kernel', 'Disk usage (root)'], 'Applications':[]}
INFO_PARAMETERS = {
        'Kernel':'uname', 
        'Disk usage (root)':'df | grep /dev/root | cut -c53-56', 
        'Processor':'cat /proc/cpuinfo | grep Processor | cut -f2 | cut -c3-', 
        'Hardware':'cat /proc/cpuinfo | grep Hardware | cut -f2 | cut -c3-', 
        'Revision':'cat /proc/cpuinfo | grep Revision | cut -f2 | cut -c3-'
        }
