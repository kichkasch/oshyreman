from constants import *

import domain_info
import gui_gps, gui_config, gui_backup

import pygtk
pygtk.require('2.0')
import gtk

DOMAINS = {'GPS Tracks':gui_gps, 'Backup and Restore':gui_backup, 'Configuration of Files':gui_config}

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
        self.window.set_size_request(400, -1)


        box = gtk.VBox(False, 5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<big><b>Offline SHR Manager</b></big>')
        box.pack_start(labelTitle, False, False, 0)

        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)

        boxDomains = gtk.VBox(False, 5)
        for domain in DOMAINS.keys():
            b = gtk.Button(domain)
            if domain == 'GPS Tracks':
                func = self.startGPS
            elif domain == 'Backup and Restore':
                func = self.startBackup
            elif domain == 'Configuration of Files':
                func = self.startConfig
            b.connect("clicked", func)
            boxDomains.pack_start(b,  True,  False,  0)            
        
        box.pack_start(boxDomains,  False,  False, 0)

        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)

        self._sysinfoPanel = self._getSysinfoPanel()
        box.pack_start(self._sysinfoPanel, False, True, 5)

        separator = gtk.HSeparator()
        box.pack_start(separator, False, True, 5)

        boxButtons = gtk.HBox(False, 5)
        bAbout = gtk.Button('About')
        bAbout.connect('clicked', self.showAbout)
        boxButtons.pack_start(bAbout,  True,  False,  0)

        bQuit = gtk.Button('Quit')
        bQuit.connect_object("clicked", gtk.Widget.destroy, self.window)
        boxButtons.pack_start(bQuit,  True,  False,  0)

        box.pack_start(boxButtons,  False,  False, 0)

        self.window.add(box)
        self.window.show_all()

    def _getSysinfoPanel(self):
        box = gtk.VBox(False, 5)
        
        self.infoLabels = {}
        self._infoTables = {}
        self._cell = {}
        if INFO_GROUPS.has_key('Status') and len(INFO_GROUPS['Status']) > 0:
            bStatus = gtk.HBox(True, 3)
            try:
                self._labelPower = gtk.Label('Bat: %s %%' %(domain_info.getSysinfo()['Battery'].strip()))
                bStatus.pack_start(self._labelPower, True, False, 0)
                self._labelsStatus = {}
                for x in ['GPS', 'Bluetooth', 'WiFi']:
                    self._labelsStatus[x] = gtk.Label() #x)
                    bStatus.pack_start(self._labelsStatus[x], True, False, 0)
                    if domain_info.getSysinfo()[x].strip().lower() == "true":
                        color = 'blue'
                    else:
                        color = 'red'
                    self._labelsStatus[x].set_markup('<span foreground="%s">%s</span>' %(color, x))
                self._labelGSM = gtk.Label('GSM: %s %%' %(domain_info.getSysinfo()['GSM'].strip()))
                bStatus.pack_end(self._labelGSM, True, False, 0)
            except KeyError:
                pass    # well; something is wrong in the config file :(
            
            box.pack_start(bStatus, False, True, 0)
            separator = gtk.HSeparator()
            box.pack_start(separator, False, True, 5)
        
        for group in INFO_GROUPS.keys():
            if group == 'Status':
                continue    # covered with extra box above
            if len(INFO_GROUPS[group]) > 0:
                infoHeading = gtk.Label() #"System information - %s" %(group))
                infoHeading.set_markup("<i>%s</i>" %(group));
                box.pack_start(infoHeading, False, False, 0)
                
                store = gtk.ListStore(str,str)
                
                for desc in INFO_GROUPS[group]:
#                    print ("appending %s %s" %(desc, domain_info.getSysinfo()[desc]))
                    store.append([desc, domain_info.getSysinfo()[desc]])

                self._infoTables[group] = gtk.TreeView(model=store)
                cell = gtk.CellRendererText()
                col = gtk.TreeViewColumn("Attribute", cell, text=0)
                col.pack_start(cell, False)
                self._infoTables[group].append_column(col)
                
                self._cell[desc] = gtk.CellRendererText()
                col = gtk.TreeViewColumn("Value", self._cell[desc], text=1)
                col.pack_start(self._cell[desc], True)
                self._infoTables[group].append_column(col)
                
                box.pack_start(self._infoTables[group], False, False, 0)
                separator = gtk.HSeparator()
                box.pack_start(separator, False, True, 5)

        boxButtons = gtk.HBox(False, 5)
        bAbout = gtk.Button('Update System Information from FreeRunner')
        bAbout.connect('clicked', self._updateSysinfo)
        boxButtons.pack_start(bAbout,  True,  False,  0)
        box.pack_start(boxButtons,  False,  False, 0)

        return box

    def _updateSysinfo(self,  target):
        domain_info.doUpdate()
        self._labelPower.set_text('Bat: %s %%' %(domain_info.getSysinfo()['Battery'].strip()))
        
        for x in ['GPS', 'Bluetooth', 'WiFi']:
            if domain_info.getSysinfo()[x].strip().lower() == "true":
                color = 'blue'
            else:
                color = 'red'
            self._labelsStatus[x].set_markup('<span foreground="%s">%s</span>' %(color, x))
        self._labelGSM.set_text('GSM: %s %%' %(domain_info.getSysinfo()['GSM'].strip()))
        for table in self._infoTables.values():
            model = table.get_model()
            treeiter = model.get_iter_first()
            while treeiter:
                desc = model.get_value(treeiter, 0)
                model.set_value(treeiter, 1, domain_info.getSysinfo()[desc])
                treeiter = model.iter_next(treeiter)

            
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


    def startBackup(self, target):
        dialog = gui_backup.BackupDialog(self.window)
        dialog.run()
        dialog.destroy()

    def startConfig(self, target):
        dialog = gui_config.FileConfigurationDialog(self.window)
        dialog.run()
        dialog.destroy()
        
    def startGPS(self, target):
        dialog = gui_gps.GPSDialog(self.window)
        dialog.run()
        dialog.destroy()


class SimpleInputDialog(gtk.Dialog):
    """
    GTK-Dialog to support Input of a single Entry
    """
    
    def __init__(self,  parent, label, title = "Please insert value", default = None):
        """
        Contructor - all components are assembled in here
        """
        gtk.Dialog.__init__(self, title,  parent,  gtk.DIALOG_MODAL ,  (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL, gtk.STOCK_OK,gtk.RESPONSE_OK))
        self.set_size_request(200, -1)
        box = gtk.VBox(False,  5)
        
        labelTitle= gtk.Label()
        labelTitle.set_markup('<b>%s</b>' %(label))
        box.pack_start(labelTitle, False, False, 0)
        
        self._entry = gtk.Entry()
        if default:
            self._entry.insert_text(default)
        box.pack_end(self._entry , False, False, 0)
        self.vbox.pack_start(box, True, True, 5)
        self.vbox.show_all() 
 
    def getValue(self):
        return self._entry.get_text()

