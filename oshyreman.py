#!/usr/bin/python
"""
oSHyReman

Offline SHR Manager
"""
from constants import *
import os,  os.path, sys

import domain_gps,  domain_backup

if __name__ == "__main__":
    if sys.argv[1].startswith('gps'):
        domain_gps.dispatch(sys.argv)
    elif sys.argv[1].startswith('bck'):
        domain_backup.dispatch(sys.argv)
    
    else:
        print "Unknown command"
        sys.exit(1)

