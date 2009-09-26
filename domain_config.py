"""
Offline SHR Manager

Domain: Config

Download and edit file - upload afterwards.
A list of pre-defined files is provided in config.
"""
from constants import *
import os

def doConfig(desc):
    doConfigPartDownload(desc)
    doConfigPartEdit()
    doConfigPartUpload(desc)

def doConfigPartDownload(desc):
    if not os.path.exists(PATH_LOCAL_CONFIG):
            os.makedirs(PATH_LOCAL_CONFIG)
    file = CONFIG_FILES[desc]
    os.system("scp %s %s" %(USER_REMOTE + "@" + HOST_REMOTE + ":" + file, TMPFILE_LOCAL_CONFIG))
    
def doConfigPartUpload(desc):
    file = CONFIG_FILES[desc]
    os.system("scp %s %s %% rm -f %s" %(TMPFILE_LOCAL_CONFIG, USER_REMOTE + "@" + HOST_REMOTE + ":" + file, TMPFILE_LOCAL_CONFIG))
    
def doConfigPartEdit():
    os.system("%s %s" %(PROGRAM_EDIT, TMPFILE_LOCAL_CONFIG))
    
def getList():
    return CONFIG_FILES
    
def dispatch(argv):
    if argv[1] == 'conf-list':
        list = getList()
        for title in list.keys():
            print "\t%s \t -> %s" %(title, list[title])
    elif argv[1] == 'conf-edit':
        doConfig(argv[2])

    else:
        print "Unknown command"
        sys.exit(1)
