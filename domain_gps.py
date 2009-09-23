"""
Offline SHR Manager

Domain: GPS
"""
import os,  os.path, sys
from constants import *

def doLocalClear():
    os.system("rm -f %s" %(os.path.join(PATH_LOCAL_MAPS, "*.log")))
    
def doRemoteClear():
    os.system("ssh %s rm -f %s" %(USER_REMOTE + "@" + HOST_REMOTE, os.path.join(PATH_REMOTE_MAPS, "*.log")))
    
def doPull():
    os.system("scp %s %s" %(USER_REMOTE + "@" + HOST_REMOTE + ":" + os.path.join(PATH_REMOTE_MAPS, "*.log"), PATH_LOCAL_MAPS))

def doPush():
    os.system("scp %s %s" %(os.path.join(PATH_LOCAL_MAPS, "*.log"), USER_REMOTE + "@" + HOST_REMOTE + ":" + PATH_REMOTE_MAPS))

def doImportGxp(src):
        if src.endswith('.gpx'):
            dest = os.path.join(PATH_LOCAL_MAPS, os.path.basename(src)[:len(os.path.basename(src))-4] + ".log")
            import gxp2TangoGps
            gxp2TangoGps.doConvert(src, dest)
        else:
            print "Unkown import format. Only <gpx> is available for import."

def doRename(old,  new):
    os.system("mv %s %s" %(os.path.join(PATH_LOCAL_MAPS, old), os.path.join(PATH_LOCAL_MAPS, new)))

def getLocalTrackList():
    ret = []
    entries = os.listdir(PATH_LOCAL_MAPS)
    for entry in entries:
        if os.path.isfile(os.path.join(PATH_LOCAL_MAPS, entry)) and entry.endswith('.log'):
            ret.append(entry)
    return ret

def dispatch(argv):
    if argv[1] == 'gps-clear-local':
        doLocalClear()
    elif argv[1] == 'gps-clear-remote':
        doRemoteClear()
    elif argv[1] == 'gps-pull':
        doPull()
    elif argv[1] == 'gps-push':
        doPush()
    elif argv[1] == 'gps-import':
        doImportGxp(sys.argv[2])
    elif argv[1] == 'gps-rename':
        doRename(argv[2], argv[3])
    elif argv[1] == 'gps-list':
        for x in getLocalTrackList():
            print x

    else:
        print "Unknown command"
        sys.exit(1)
