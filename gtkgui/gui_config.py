from constants import *
import domain_config

import pygtk
pygtk.require('2.0')
import gtk

class FileConfigurationDialog(gtk.Dialog):
    """
    GTK-Dialog to support remote file configuration activitites
    """
    
    def __init__(self,  parent):
        """
        Contructor - all components are assembled in here
        """
        gtk.Dialog.__init__(self, "oSHyReMan: Remote File Configuration",  parent,  gtk.DIALOG_MODAL ,  (gtk.STOCK_QUIT,gtk.RESPONSE_OK))
        self.set_size_request(500, 300)
        box = gtk.VBox(False,  5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<big><b>Remote File Configuration</b></big>')
        box.pack_start(labelTitle, False, False, 0)
        
        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)
        
        
        self.vbox.pack_start(box, True, True, 5)
        self.vbox.show_all()
