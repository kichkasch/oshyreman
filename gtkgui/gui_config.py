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
        self.set_size_request(600, 400)
        box = gtk.VBox(False,  5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<big><b>Remote File Configuration</b></big>')
        box.pack_start(labelTitle, False, False, 0)
        
        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)

        hbox = gtk.HBox(False, 5)
        
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        hbox.pack_start(scrolled_window, True, True, 0)

        store = gtk.ListStore(str, str)
        for desc in domain_config.getList().keys():
            store.append([desc, domain_config.getList()[desc]])

        self._configTable = gtk.TreeView(model=store)
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Description", cell, text=0)
        col.pack_start(cell, False)
        self._configTable.append_column(col)
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Path", cell, text=1)
        col.pack_start(cell, False)
        self._configTable.append_column(col)
                
        self._configTable.get_selection().set_mode(gtk.SELECTION_SINGLE)
        scrolled_window.add_with_viewport(self._configTable)
        
        separator = gtk.VSeparator()
        hbox.pack_start(separator, False, True, 5)
        
        bButtons = gtk.VBox(False, 5)
        bButtons.set_size_request(180, -1)
        b = gtk.Button("Edit selected File")
        b.connect('clicked', self._doEdit)        
        bButtons.pack_start(b, False, False,  5)
        
        hbox.pack_end(bButtons, False, True,  5)
        box.pack_end(hbox, True, True, 0)
        
        self.vbox.pack_start(box, True, True, 5)
        self.vbox.show_all()

    def _doEdit(self, target):
        treeselection = self._configTable.get_selection()
        (model, iter) = treeselection.get_selected()
        value = model.get_value(iter, 0)
        
        domain_config.doConfigPartDownload(value)
        domain_config.doConfigPartEdit()
        
#        domain_config.doConfigPartUpload(value)
