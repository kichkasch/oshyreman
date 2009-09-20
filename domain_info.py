"""
Offline SHR Manager

Domain: Sys-Info
"""

def getSysinfo():
    pass

def dispatch(argv):
    if argv[1] == 'info':
        info = getSysinfo()
        
    else:
        print "Unknown command"
        sys.exit(1)
