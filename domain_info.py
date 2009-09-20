"""
Offline SHR Manager

Domain: Sys-Info
"""
from constants import *

def getSysinfo():
    for desc in INFO_PARAMETERS.keys():
        cmd = INFO_PARAMETERS[desc]
        os.system("ssh %s %s" %(USER_REMOTE + "@" + HOST_REMOTE, cmd))

def dispatch(argv):
    if argv[1] == 'info':
        info = getSysinfo()
        
    else:
        print "Unknown command"
        sys.exit(1)
