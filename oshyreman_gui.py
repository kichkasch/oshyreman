#!/usr/bin/python
"""
oSHyReman GUI

Offline SHR Manager
"""
from constants import *

import domain_gps,  domain_backup, domain_config, domain_info

import pygtk
pygtk.require('2.0')
import gtk

DOMAINS = {'GPS Tracks':domain_gps, 'Backup and Restore':domain_backup, 'Configuration of Files':domain_config}

class Base():
    """
    The one and only Main frame
    
    Made up mainly by a notebook; one side for each type of PIM data, and by a progress bar and some buttons.
    """
    def __init__(self):
        """
        Constructor - the whole assembling of the window is performed in here
        """
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        box = gtk.VBox(False, 5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<big><b>Offline SHR Manager</b></big>')
        box.pack_start(labelTitle, False, False, 0)
        labelTitle.show()

        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)
        separator.show()

        boxDomains = gtk.VBox(False, 5)
        for domain in DOMAINS.keys():
            b = gtk.Button(domain)
#            b.connect_object("clicked", gtk.Widget.destroy, self.window)
            boxDomains.pack_start(b,  True,  False,  0)
            b.show()
            
        
        
        boxDomains.show()
        box.pack_start(boxDomains,  False,  False, 0)

        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)
        separator.show()

        self._sysinfoPanel = self._getSysinfoPanel()
        box.pack_start(self._sysinfoPanel, False, True, 5)
        self._sysinfoPanel.show()

        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)
        separator.show()

        boxButtons = gtk.HBox(False, 5)
        bAbout = gtk.Button('About')
        bAbout.connect('clicked', self.showAbout)
        boxButtons.pack_start(bAbout,  True,  False,  0)
        bAbout.show()

        bQuit = gtk.Button('Quit')
        bQuit.connect_object("clicked", gtk.Widget.destroy, self.window)
        boxButtons.pack_start(bQuit,  True,  False,  0)
        bQuit.show()

        boxButtons.show()
        box.pack_start(boxButtons,  False,  False, 0)

        box.show()
        self.window.add(box)
        self.window.show()

    def _getSysinfoPanel(self):
        box = gtk.VBox(False, 1)
        
        self.infoLabels = {}
        for group in INFO_GROUPS.keys():
            if len(INFO_GROUPS[group]) > 0:
                infoHeading = gtk.Label() #"System information - %s" %(group))
                infoHeading.set_markup("System information - <big><i>%s</i></big>" %(group));
                box.pack_start(infoHeading, False, False, 0)
                infoHeading.show()
                for desc in INFO_GROUPS[group]:
    #        for desc in domain_info.getSysinfo().keys():
                    self.infoLabels[desc] = gtk.Label("%s: %s" %(desc, domain_info.getSysinfo()[desc]))
                    self.infoLabels[desc].set_alignment(0, 0)
                    box.pack_start(self.infoLabels[desc], False, False, 0)
                    self.infoLabels[desc].show()

        boxButtons = gtk.HBox(False, 5)
        bAbout = gtk.Button('Update')
        bAbout.connect('clicked', self._updateSysinfo)
        boxButtons.pack_end(bAbout,  True,  False,  0)
        bAbout.show()
        boxButtons.show()
        box.pack_start(boxButtons,  False,  False, 0)

        box.show()
        return box

    def _updateSysinfo(self,  target):
        domain_info.doUpdate()
        for desc in domain_info.getSysinfo().keys():
            self.infoLabels[desc].set_text("%s: %s" %(desc, domain_info.getSysinfo()[desc]))

    def main(self):
        """
        Starts up the application ('Main-Loop')
        """
        gtk.main()

    def destroy(self, widget, data=None):
        """
        Shuts down the application
        """
        gtk.main_quit()

    def delete_event(self, widget, event, data=None):
        """
        Event handler
        """
        return False

    def showAbout(self,  target):
        """
        Pops up an 'About'-dialog, which displays all the application meta information from module constants.
        """
        d = gtk.AboutDialog()
        d.set_name(PROGRAM_NAME)
        d.set_version(PROGRAM_VERSION)
        f = open(FILEPATH_COPYING,  "r")
        content = f.read()
        f.close()
        d.set_license(content)
        d.set_authors(PROGRAM_AUTHORS)
        d.set_comments(PROGRAM_COMMENTS)
        d.set_website(PROGRAM_HOMEPAGE)
        ret = d.run()
        d.destroy()

"""
This starts the GUI version of oSHyReMan
"""
if __name__ == "__main__":
    base = Base()
    base.main()
