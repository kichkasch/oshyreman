from constants import *
import domain_backup

import pygtk
pygtk.require('2.0')
import gtk, gobject

class BackupDialog(gtk.Dialog):
    """
    GTK-Dialog to support all backup / restore activitites
    """
    
    def __init__(self,  parent):
        """
        Contructor - all components are assembled in here
        """
        gtk.Dialog.__init__(self, "oSHyReMan: Backup and Restore",  parent,  gtk.DIALOG_MODAL ,  (gtk.STOCK_QUIT,gtk.RESPONSE_OK))
        self.set_size_request(600, 700)

        box = gtk.VBox(False,  5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<big><b>Backup and Restore</b></big>')
        box.pack_start(labelTitle, False, False, 0)
        
        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)


        infoHeading = gtk.Label() 
        infoHeading.set_markup("<i>Backup</i>");
        box.pack_start(infoHeading, False, False, 0)
        
        box.pack_start(self._getBackupBox(), True, True, 0)

        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)
        infoHeading = gtk.Label() 
        infoHeading.set_markup("<i>Restore</i>");
        box.pack_start(infoHeading, False, False, 0)

        box.pack_start(self._getRestoreBox(), True, True, 0)
        
        self.vbox.pack_start(box, True, True, 5)
        self.vbox.show_all()

    def _getBackupBox(self):
        hbox = gtk.HBox(False, 5)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        hbox.pack_start(scrolled_window, True, True, 0)
        
        store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        for filename in BACKUP_FILES:
            store.append([True, filename])

        self._backupTable = gtk.TreeView(model=store)
        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', True)
        cell.connect( 'toggled', self._backup_toggled_cb, store)
        col = gtk.TreeViewColumn("Include", cell)
        col.add_attribute(cell, "active", 0)
        col.pack_start(cell, False)
        
        self._backupTable.append_column(col)
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Filename", cell, text=1)
        col.pack_start(cell, False)
        self._backupTable.append_column(col)
                
                
        separator = gtk.VSeparator()
        hbox.pack_start(separator, False, True, 5)
        
        bButtons = gtk.VBox(False, 5)
        bButtons.set_size_request(180, -1)
        b = gtk.Button("Select All")
        b.connect('clicked', self._doSelectAll, store)
        bButtons.pack_start(b, False, False,  5)
        b = gtk.Button("Deselect All")
        b.connect('clicked', self._doDeselectAll, store)
        bButtons.pack_start(b, False, False,  5)
        b = gtk.Button("Invert Selection")
        b.connect('clicked', self._doInvert, store)
        bButtons.pack_start(b, False, False,  5)
        separator = gtk.HSeparator()
        bButtons.pack_start(separator, False, True, 5)
        b = gtk.Button("Run Backup")
        b.connect('clicked', self._doBackup, store)
        bButtons.pack_end(b, False, False,  5)
        
        hbox.pack_end(bButtons, False, True,  5)
                
                
        self._backupTable.get_selection().set_mode(gtk.SELECTION_SINGLE)
        scrolled_window.add_with_viewport(self._backupTable)

        return hbox
        
    def _backup_toggled_cb( self, cell, path, model ):
        model[path][0] = not model[path][0]
        return
        
    def _doSelectAll(self, target, model):
        treeiter = model.get_iter_first()
        while treeiter:
            model[treeiter][0] = True
            treeiter = model.iter_next(treeiter)
        
    def _doDeselectAll(self, target, model):
        treeiter = model.get_iter_first()
        while treeiter:
            model[treeiter][0] = False
            treeiter = model.iter_next(treeiter)
        
    def _doInvert(self, target, model):
        treeiter = model.get_iter_first()
        while treeiter:
            model[treeiter][0] = not model[treeiter][0]
            treeiter = model.iter_next(treeiter)
            
    def _doBackup(self, target, model):
        files = []
        treeiter = model.get_iter_first()
        while treeiter:
            if model[treeiter][0]:
                files.append(model[treeiter][1])
            treeiter = model.iter_next(treeiter)
        if len(files) > 0:
            domain_backup.do_backup(files)
        self._updateRestoreList()
        
        
        
    def _getRestoreBox(self):
        hbox = gtk.HBox(False, 5)
        
        vbox = gtk.VBox(False, 5)
        
        self._combo = gtk.combo_box_new_text()
        for x in domain_backup.getBackupList():
            self._combo.append_text(x)
        self._combo.connect('changed', self._comboSelected)

        vbox.pack_start(self._combo, False, True, 5)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        vbox.pack_start(scrolled_window, True, True, 0)
        
        store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)

        self._restoreTable = gtk.TreeView(model=store)
        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', True)
        cell.connect( 'toggled', self._restore_toggled_cb, store)
        col = gtk.TreeViewColumn("Include", cell)
        col.add_attribute(cell, "active", 0)
        col.pack_start(cell, False)
        self._restoreTable.append_column(col)
        
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Filename", cell, text=1)
        col.pack_start(cell, False)
        self._restoreTable.append_column(col)
        self._restoreTable.get_selection().set_mode(gtk.SELECTION_SINGLE)
        scrolled_window.add_with_viewport(self._restoreTable)

        hbox.pack_start(vbox, True, True,  5)
        
        separator = gtk.VSeparator()
        hbox.pack_start(separator, False, True, 5)
        
        bButtons = gtk.VBox(False, 5)
        bButtons.set_size_request(180, -1)
        b = gtk.Button("Delete selected Backup")
        bButtons.pack_start(b, False, False,  5)
        b.connect('clicked', self._doDeleteBackup)
        separator = gtk.HSeparator()
        bButtons.pack_start(separator, False, True, 5)
        
        b = gtk.Button("Select All")
        b.connect('clicked', self._doSelectAll, store)
        bButtons.pack_start(b, False, False,  5)
        b = gtk.Button("Deselect All")
        b.connect('clicked', self._doDeselectAll, store)
        bButtons.pack_start(b, False, False,  5)
        b = gtk.Button("Invert Selection")
        b.connect('clicked', self._doInvert, store)
        bButtons.pack_start(b, False, False,  5)
        
        b = gtk.Button("Restore selected Files")
        b.connect('clicked', self._doRestore)
        bButtons.pack_end(b, False, False,  5)
        separator = gtk.HSeparator()
        bButtons.pack_end(separator, False, True, 5)
        
        hbox.pack_end(bButtons, False, True,  5)
        return hbox
        
    def _restore_toggled_cb( self, cell, path, model ):
        model[path][0] = not model[path][0]
        return
        
    def _comboSelected(self, target):
        self._updateRestoreFileList()
        
    def _updateRestoreList(self):
        store = self._combo.get_model()
        store.clear()
        for x in domain_backup.getBackupList():
            store.append([x])
        
    def _updateRestoreFileList(self):
        string = self._combo.get_active_text()
        model = self._restoreTable.get_model()
        model.clear()
        if string:
            for filename in domain_backup.getFilesForBackup(string):
                model.append([True, filename])
        
    def _doDeleteBackup(self, target):
        string = self._combo.get_active_text()
        domain_backup.do_deleteBackup(string)
        self._updateRestoreList()
        
    def _doRestore(self, target):
        files = []
        string = self._combo.get_active_text()
        model = self._restoreTable.get_model()
        treeiter = model.get_iter_first()
        while treeiter:
            if model[treeiter][0]:
                files.append(model[treeiter][1])
            treeiter = model.iter_next(treeiter)
        if len(files) > 0:
            domain_backup.do_restore(string, files)
    
