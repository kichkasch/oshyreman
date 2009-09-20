import os.path

#
# GENERAL
#
PATH_LOCAL_DATA = "/home/michael/.offline_shrmanager"
HOST_REMOTE = "192.168.0.202"
USER_REMOTE = "root"    # make sure, this user can login without password


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
