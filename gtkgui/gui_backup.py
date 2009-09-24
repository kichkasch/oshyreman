from constants import *
import domain_backup

import pygtk
pygtk.require('2.0')
import gtk

class BackupDialog(gtk.Dialog):
    """
    GTK-Dialog to support all backup / restore activitites
    """
    
    def __init__(self,  parent):
        """
        Contructor - all components are assembled in here
        """
        gtk.Dialog.__init__(self, "oSHyReMan: Backup and Restore",  parent,  gtk.DIALOG_MODAL ,  (gtk.STOCK_QUIT,gtk.RESPONSE_OK))
        self.set_size_request(500, 300)

        box = gtk.VBox(False,  5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<big><b>Backup and Restore</b></big>')
        box.pack_start(labelTitle, False, False, 0)
        
        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)
        
        
        self.vbox.pack_start(box, True, True, 5)
        self.vbox.show_all()
