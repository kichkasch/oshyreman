"""
Offline SHR Manager

Domain: Backup / Restore

For Backup: Download specified files and put into folder made out of timestamp.
"""

import os,  os.path, sys
from constants import *
import shutil
from datetime import datetime

OUTPUTFILE = "/tmp/oshyreman-output.dat"
ERRORFILE = "/tmp/oshyreman-error.dat"
REDIRECT_OUTPUT = " > " + OUTPUTFILE # + " 2>" + ERRORFILE

def do_backup(files = BACKUP_FILES):
    dir = os.path.join(PATH_LOCAL_BACKUPS, datetime.now().strftime("%Y%m%d-%H%M%S"))
    if not os.path.exists(dir):
            os.makedirs(dir)
    
    for file in files:
        localDir = os.path.join(dir, os.path.dirname(file)[1:])
        if not os.path.exists(localDir):
                os.makedirs(localDir)
        
        os.system("scp %s %s" %(USER_REMOTE + "@" + HOST_REMOTE + ":" + file, localDir))
    
    os.system("(cd %s && tar czf %s %s)" %(
                                                    dir, 
                                                    os.path.join("..", "backup-" +datetime.now().strftime("%Y%m%d-%H%M%S")+ ".tar.gz"), 
                                                    "*"))
    os.system("rm -rf %s" %(dir))
        
def getBackupList():
    ret = []
    entries = os.listdir(PATH_LOCAL_BACKUPS)
    for entry in entries:
        if os.path.isfile(os.path.join(PATH_LOCAL_BACKUPS, entry)) and entry.endswith('.tar.gz'):
            ret.append(entry[7:22])
    return ret    
    
def getFilesForBackup(backupTimestamp):
    ret = []
    os.system("tar --list --verbose --file=%s %s" %(os.path.join(PATH_LOCAL_BACKUPS,"backup-" + backupTimestamp + ".tar.gz"), REDIRECT_OUTPUT ))
    f = open(OUTPUTFILE, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        if line.startswith('-'):    # not a directory
            ret.append("/" + line.strip().split()[5])
    return ret
        
def dispatch(argv):
    if argv[1] == 'bck-backup':
        do_backup()
    elif argv[1] == 'bck-list':
        for x in getBackupList():
            print x
    elif argv[1] == 'bck-files':
        for file in getFilesForBackup(argv[2]):
            print file
    elif argv[1] == 'bck-test':
        print _determinePathLength(os.path.join(PATH_LOCAL_BACKUPS, datetime.now().strftime("%Y%m%d-%H%M%S")))

    else:
        print "Unknown command"
        sys.exit(1)
