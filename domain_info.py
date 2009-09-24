"""
Offline SHR Manager

Domain: Sys-Info
"""
from constants import *
from cStringIO import StringIO
import sys

infoObject = None

OUTPUTFILE = "/tmp/oshyreman-output.dat"
ERRORFILE = "/tmp/oshyreman-error.dat"
REDIRECT_OUTPUT = " > " + OUTPUTFILE # + " 2>" + ERRORFILE

def getSysinfo():
    global infoObject
    if not infoObject:
        doInit()
    return infoObject

def doInit():
    global infoObject
    infoObject = {}
    for desc in INFO_PARAMETERS.keys():
        infoObject [desc] = "n.a."

def doUpdate():
    print "updating sys info"
    global infoObject
    infoObject = {}
    for desc in INFO_PARAMETERS.keys():
        cmd = INFO_PARAMETERS[desc]
        os.system("ssh %s %s" %(USER_REMOTE + "@" + HOST_REMOTE, cmd + REDIRECT_OUTPUT))
        file = open(OUTPUTFILE,  "r")
        infoObject [desc] = file.read()
        file.close()
#        print ">" + mystdout.getvalue() + "<"
#        infoObject [desc]  = mystdout.getvalue()

def dispatch(argv):
    if argv[1] == 'info':
        info = getSysinfo()
        
    else:
        print "Unknown command"
        sys.exit(1)
