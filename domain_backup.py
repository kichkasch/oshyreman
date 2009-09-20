"""
Offline SHR Manager

Domain: Backup / Restore

For Backup: Download specified files and put into folder made out of timestamp.
"""

import os,  os.path, sys
from constants import *
import shutil
from datetime import datetime

def do_backup(files = BACKUP_FILES):
    dir = os.path.join(PATH_LOCAL_BACKUPS, datetime.now().strftime("%Y%m%d-%H:%M:%S"))
    if not os.path.exists(dir):
            os.makedirs(dir)
    
    for file in files:
        localDir = os.path.join(dir, os.path.dirname(file)[1:])
        if not os.path.exists(localDir):
                os.makedirs(localDir)
        
        os.system("scp %s %s" %(USER_REMOTE + "@" + HOST_REMOTE + ":" + file, localDir))
        
        
def dispatch(argv):
    if argv[1] == 'bck-backup':
        do_backup()

    else:
        print "Unknown command"
        sys.exit(1)
