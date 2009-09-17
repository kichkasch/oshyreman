

import sys, re
import xml.etree.cElementTree as ET

def doConvert(src, dest):
    tree = ET.parse(src)
    root = tree.getroot()
    ns = re.match('{(.*)}', root.tag).group(1)

    out = open(dest, "w")
    for trkpt in root.findall('.//{%s}trkpt' % ns) + root.findall('.//{%s}rtept' % ns):
        a = trkpt.attrib
        for key, default in (('ele', 555.55), ('speed', 1.0), ('hdop', 1.0), ('course', 0.0), ('time', '2009-05-16T09:35:58Z')):
            a[key] = trkpt.findtext('{%s}%s' % (ns, key)) or default
        
        out.write('%(lat)s,%(lon)s,%(ele)s,%(speed)s,%(hdop)s,%(time)s\n' % a)
    out.close()

if __name__ == "__main__":
    doConvert(sys.argv[1], None)
