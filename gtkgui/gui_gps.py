from constants import *
import domain_gps
import gtkgui.mainwindow

import pygtk
pygtk.require('2.0')
import gtk

class GPSDialog(gtk.Dialog):
    """
    GTK-Dialog to support GPS track management
    """
    
    def __init__(self,  parent):
        """
        Contructor - all components are assembled in here
        """
        gtk.Dialog.__init__(self, "oSHyReMan: GPS Track Management",  parent,  gtk.DIALOG_MODAL ,  (gtk.STOCK_QUIT,gtk.RESPONSE_OK))
        self.set_size_request(500, -1)
        box = gtk.VBox(False,  5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<big><b>GPS Track Management</b></big>')
        box.pack_start(labelTitle, False, False, 0)
        
        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)

        hbox = gtk.HBox(False, 5)
        
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        hbox.pack_start(scrolled_window, True, True, 0)
        
        store = gtk.ListStore(str)
        for trackname in domain_gps.getLocalTrackList():
            store.append([trackname])

        self._gpsTable = gtk.TreeView(model=store)
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Tracknames (local)", cell, text=0)
        col.pack_start(cell, False)
        self._gpsTable.append_column(col)
                
        self._gpsTable.get_selection().set_mode(gtk.SELECTION_SINGLE)
        scrolled_window.add_with_viewport(self._gpsTable)
        
        
        separator = gtk.VSeparator()
        hbox.pack_start(separator, False, True, 5)
        
        bButtons = gtk.VBox(False, 5)
        b = gtk.Button("Rename selected Track")
        b.connect('clicked', self._doRename)
        bButtons.pack_start(b, False, False,  5)
        b = gtk.Button("Import Track")
        b.connect('clicked', self._doImport)
        bButtons.pack_start(b, False, False,  5)
        separator = gtk.HSeparator()
        bButtons.pack_start(separator, False, True, 5)
        b = gtk.Button("Pull Tracks from Freerunner")
        bButtons.pack_start(b, False, False,  5)
        b = gtk.Button("Push Tracks to Freerunner")
        bButtons.pack_start(b, False, False,  5)
        separator = gtk.HSeparator()
        bButtons.pack_start(separator, False, True, 5)
        b = gtk.Button("Clear Tracks on Freerunner")
        bButtons.pack_start(b, False, False,  5)
        b = gtk.Button("Clear Tracks locally")
        bButtons.pack_end(b, False, False,  5)
        
        hbox.pack_end(bButtons, False, True,  5)
        
        box.pack_end(hbox, True, True, 0)

        self.vbox.pack_start(box, True, True, 5)
        self.vbox.show_all()

    def _doRename(self, target):
        treeselection = self._gpsTable.get_selection()
        (model, iter) = treeselection.get_selected()
        value = model.get_value(iter, 0)

        dia = gtkgui.mainwindow.SimpleInputDialog(self, "New name for this track", default=value)
        if dia.run() == gtk.RESPONSE_OK:
            domain_gps.doRename(value, dia.getValue())
        dia.destroy()
        self._updateTracklist()

    def _doImport(self, target):
        chooser = gtk.FileChooserDialog(title="Please choose file to import",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        filter = gtk.FileFilter()
        filter.set_name("GPX Files")
        filter.add_pattern("*.gpx")

        chooser.add_filter(filter)
        if chooser.run() == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
            domain_gps.doImportGxp(filename)
        chooser.destroy()
        self._updateTracklist()

    def _updateTracklist(self):
        model = self._gpsTable.get_model()
        model.clear()
        for trackname in domain_gps.getLocalTrackList():
            model.append([trackname])
