# coding=utf-8

'''
Created on Jun 5, 2009

@author: santiago
'''

import sys
import gtk

from Pytalog.About import About
from Pytalog.AddCatalog import AddCatalog
from Pytalog.AddVolume import AddVolume

from Pytalog.Lib import get_manager

from Pytalog.Humanize import HumanizeSize

class Principal(object):
    '''
    Code-behind de la ventana principal.
    '''
    
    WINDOW_MAIN = 'window'
    TOOLBAR = 'toolbar_principal'
    TOOLBAR_ADD_VOLUME = 'toolbutton_add_volume'
       
    def __init__(self):
        self.__builder = gtk.Builder()
        self.__builder.add_from_file('principal.glade')
        self.__builder.connect_signals(self)
        
        self.__principal = self.__builder.get_object(Principal.WINDOW_MAIN)
        self.__toolbar = self.__builder.get_object(Principal.TOOLBAR)
        self.__toolbar_add_volume = self.__builder.get_object(Principal.TOOLBAR_ADD_VOLUME)
             
        self.__tree_view = CatalogTreeView(self, self.__builder, self.__principal)
        self.__tree_view.load_catalogs()

        self.__list_view = CatalogListView(self, self.__builder)

    def show(self):
        self.__principal.show()

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def update(self):
        '''
        Operación invocada por otras ventanas cuando se quiere refrescar
        el tree view.
        '''
        
        self.__list_view.unload_volume()
        self.__tree_view.load_catalogs()

    def load_volume(self, volume_id):
        self.__list_view.load_volume(volume_id)

    def add_catalog(self):
        AddCatalog().show(self)
        
    def add_volume(self, catalog_id):
        AddVolume().show(self, catalog_id)
        
    def catalog_selected(self, is_catalog_selected):
        self.__toolbar_add_volume.set_sensitive(is_catalog_selected)

    '''
    Signals del menu principal.
    '''
    
    def on_menuitemQuit_activate(self, widget, data=None):
        gtk.main_quit()
    
    def on_menuitemAbout_activate(self, widget, data=None):
        About().show()
    
    def on_menuitemNewCatalog_activate(self, widget, data=None):
        self.add_catalog()        
        
    '''
    Signals del toolbar
    '''

    def on_toolbutton_new_catalog_clicked(self, widget, data=None):
        self.add_catalog()
        
    def on_toolbutton_add_volume_clicked(self, widget, data=None):
        selected = self.__tree_view.get_selected_item()
        if selected:
            (id, type) = selected
            self.add_volume(id)
        
    '''
    Signals del treeview.
    '''
    
    def on_treeviewVolumes_cursor_changed(self, widget, data=None):
        self.__tree_view.on_treeviewVolumes_cursor_changed(widget, data)
          
    def on_treeviewVolumes_row_activated(self, widget, path, view_column, data=None):
        self.__tree_view.on_treeviewVolumes_row_activated(widget, path, view_column, data)
    
    def on_treeviewVolumes_row_expanded(self, widget, iter, path, data=None):
        self.__tree_view.on_treeviewVolumes_row_expanded(widget, iter, path, data)
        
    def on_treeviewVolumes_button_release_event(self, treeview, event, data=None):
        self.__tree_view.on_treeviewVolumes_button_release_event(treeview, event, data)

    def on_menu_tree_add_volume_activate(self, widget, data=None):
        self.__tree_view.on_menu_tree_add_volume_activate(widget, data)
    
    def on_menu_tree_rename_activate(self, widget, data=None):
        self.__tree_view.on_menu_tree_rename_activate(widget, data)
    
    def on_menu_tree_delete_activate(self, widget, data=None):
        result = self.__tree_view.on_menu_tree_delete_activate(widget, data)
        if result:
            (id, type) = result
            self.__list_view.tree_item_removed(id, type)
       
    def on_cellVolumesName_edited(self, widget, path, new_text, data=None):
        self.__tree_view.on_cellVolumesName_edited(widget, path, new_text, data)

    def on_button_rename_ok_clicked(self, widget, data=None):
        self.__tree_view.on_button_rename_ok_clicked(widget, data)
    
    def on_button_rename_cancel_clicked(self, widget, data=None):
        self.__tree_view.on_button_rename_cancel_clicked(widget, data)
        
    '''
    Signals del listview
    '''
    def on_treeviewFiles_row_activated(self, widget, path, view_column, data=None):
        self.__list_view.on_treeviewFiles_row_activated(widget, path, view_column, data)

class CatalogListView(object):
    '''
    Clase encargada del comportamiento del treeview de archivos y directorios.
    '''
    
    ICON_DIRECTORY = 'image_directory'
    ICON_FILE = 'image_file'
    
    LIST_MODEL = 'listFiles'
    TREE_VIEW = 'treeviewFiles'
    
    ITEM_TYPE_PARENT = -1
    ITEM_TYPE_DIRECTORY = 0
    ITEM_TYPE_FILE = 1
    
    def __init__(self, principal, builder):
        self.__principal = principal
        self.__builder = builder
    
        imageDirectory = self.__builder.get_object(CatalogListView.ICON_DIRECTORY)
        self.__imageDirectoryStock = imageDirectory.get_stock()[0]

        imageFile = self.__builder.get_object(CatalogListView.ICON_FILE)
        self.__imageFileStock = imageFile.get_stock()[0]
        
        self.__tree_view = self.__builder.get_object(CatalogListView.TREE_VIEW)
        self.__list_store = self.__builder.get_object(CatalogListView.LIST_MODEL)
   
        self.__volume = None    
   
    def load_volume(self, volume_id):
        self.__volume = get_manager().get_data().get_volume(volume_id)
        self.load_volume_directory(None)

    def load_volume_directory(self, directory_id):
        self.unload_directory()
        
        (directories, files, parent_id) = get_manager().get_data().get_volume_content(self.__volume.volume_id, directory_id)

        if parent_id:
            self.__list_store.append([parent_id, '..', CatalogListView.ITEM_TYPE_PARENT, self.__imageDirectoryStock, '', ''])
        
        for directory in directories:
            self.__list_store.append([directory.directory_id, directory.name, CatalogListView.ITEM_TYPE_DIRECTORY, self.__imageDirectoryStock, '', ''])

        for file in files:
            self.__list_store.append([file.file_id, file.name, CatalogListView.ITEM_TYPE_FILE, self.__imageFileStock, HumanizeSize(file.size), file.modified_on])
 
    def unload_volume(self):
        self.__volume = None
        self.unload_directory()

    def unload_directory(self):
        self.__list_store.clear()
        
    def __get_item_from_path(self, path):
        '''
        Dado un path de un item en el listview retorna una tupla con (id, type, iter).
        '''
        iter = self.__list_store.get_iter(path)

        id = self.__list_store.get_value(iter, 0)
        type = self.__list_store.get_value(iter, 2)
        
        return (id, type, iter)
        
    def on_treeviewFiles_row_activated(self, widget, path, view_column, data=None):
        (id, type, iter) = self.__get_item_from_path(path)
        
        if (type == CatalogListView.ITEM_TYPE_DIRECTORY):
            self.load_volume_directory(id)
        elif (type == CatalogListView.ITEM_TYPE_PARENT):
            self.load_volume_directory(id)
            
    def tree_item_removed(self, id, tree_type):
        if self.__volume:
            if tree_type == CatalogTreeView.ITEM_TYPE_CATALOG:
                if self.__volume.catalog_id == id:
                    self.unload_volume()
            elif tree_type == CatalogTreeView.ITEM_TYPE_VOLUME:
                if self.__volume.volume_id == id:
                    self.unload_volume()
                
class CatalogTreeView(object):
    '''
    Clase encargada del comportamiento del treeview 
    de volumenes y catalogos de la ventana principal.
    '''
    
    ICON_CATALOG = 'image_catalog'
    ICON_VOLUME = 'image_volume'
    
    TREE_MODEL = 'treeVolumes'
    TREE_VIEW = 'treeviewVolumes'
    
    ITEM_TYPE_CATALOG = 0
    ITEM_TYPE_VOLUME = 1

    MENU_TREE = 'menu_tree'
    MENU_TREE_ADD_VOLUME = 'menu_tree_add_volume'
    
    def __init__(self, principal, builder, principalWindow):
        self.__principal = principal
        self.__principalWindow = principalWindow
        self.__builder = builder
        
        imageCatalog = self.__builder.get_object(CatalogTreeView.ICON_CATALOG)
        self.__imageCatalogStock = imageCatalog.get_stock()[0]

        imageVolume = self.__builder.get_object(CatalogTreeView.ICON_VOLUME)
        self.__imageVolumeStock = imageVolume.get_stock()[0]
        
        self.__tree_view = self.__builder.get_object(CatalogTreeView.TREE_VIEW)
        self.__tree_store = self.__builder.get_object(CatalogTreeView.TREE_MODEL)
        self.__menu_tree = self.__builder.get_object(CatalogTreeView.MENU_TREE)
        self.__menu_tree_add_volume = self.__builder.get_object(CatalogTreeView.MENU_TREE_ADD_VOLUME)

    def load_catalogs(self):
        self.__tree_store.clear()
        
        catalogs = get_manager().get_data().get_catalogs()
        for catalog in catalogs:        
            iter = self.__tree_store.append(None, [catalog.catalog_id, catalog.name, self.__imageCatalogStock, CatalogTreeView.ITEM_TYPE_CATALOG, True] )
            
            volumes = get_manager().get_data().get_volumes(catalog.catalog_id)
            for volume in volumes:
                self.__tree_store.append(iter, [volume.volume_id, volume.label, self.__imageVolumeStock, CatalogTreeView.ITEM_TYPE_VOLUME, True] )

    def get_selected_item(self):
        treeselection = self.__tree_view.get_selection()
        (model, iter) = treeselection.get_selected()
        if iter:
            catalog_or_volume_id = model.get_value(iter, 0)
            type = self.__tree_store.get_value(iter, 3)
            
            return (catalog_or_volume_id, type)
        else:
            return None

    def __get_item_from_path(self, path):
        '''
        Dado un path de un item en el treeview retorna una tupla con (id, type, iter).
        '''
        iter = self.__tree_store.get_iter(path)

        id = self.__tree_store.get_value(iter, 0)
        type = self.__tree_store.get_value(iter, 3)
        
        return (id, type, iter)

    def on_treeviewVolumes_cursor_changed(self, widget, data=None):
        selected = self.get_selected_item()
        if selected:
            (catalog_or_volume_id, type) = selected
            
            if type == CatalogTreeView.ITEM_TYPE_CATALOG:
                self.__principal.catalog_selected(True)
            else:
                self.__principal.catalog_selected(False)                
        else:
            self.__principal.catalog_selected(False)
          
    def on_treeviewVolumes_row_activated(self, widget, path, view_column, data=None):
        (id, type, iter) = self.__get_item_from_path(path)
        
        if (type == CatalogTreeView.ITEM_TYPE_VOLUME):
            self.__principal.load_volume(id)
    
    def on_treeviewVolumes_row_expanded(self, widget, iter, path, data=None):
        catalog_id = self.__tree_store.get_value(iter, 0)
        #print "Expanded: <'%s','%s'>" % (path, catalog_id) 
        
    def on_treeviewVolumes_button_release_event(self, treeview, event, data=None):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor(path, col, False)
                
                (id, type, iter) = self.__get_item_from_path(path)
                self.__menu_tree.current_item = (id, type, iter, path)
                
                if (type == CatalogTreeView.ITEM_TYPE_CATALOG):
                    self.__menu_tree_add_volume.show()
                else:
                    self.__menu_tree_add_volume.hide()
                
                self.__menu_tree.popup(None, None, None, event.button, time)

    def on_menu_tree_add_volume_activate(self, widget, data=None):
        (id, type, iter, path) = self.__menu_tree.current_item
        self.__principal.add_volume(id)
    
    def on_menu_tree_rename_activate(self, widget, data=None):
        (id, type, iter, path) = self.__menu_tree.current_item
        name = self.__tree_store.get_value(iter, 1)

        self.__dialog_rename = self.__builder.get_object('dialog_rename')
        self.__dialog_rename.info = (id, type, path, iter)
        self.__builder.get_object('entry_rename').set_text(name)
        
        if self.__dialog_rename.run() == gtk.RESPONSE_OK:
            pass
        
        self.__dialog_rename.hide()       
        self.__dialog_rename = None
    
    def on_menu_tree_delete_activate(self, widget, data=None):
        (id, type, iter, path) = self.__menu_tree.current_item
        name = self.__tree_store.get_value(iter, 1)
        
        message = gtk.MessageDialog(self.__principalWindow, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, None)
        message.set_markup("Are you sure you want to delete '{0}'?".format(name))
        message.format_secondary_text("NOTE: deleting catalogs may take a couple of minutes.")
        result = message.run()
        
        if result == gtk.RESPONSE_OK:
            if (type == CatalogTreeView.ITEM_TYPE_CATALOG):
                if (get_manager().get_data().del_catalog(id)):
                    self.__tree_store.remove(iter)
            else:
                if (get_manager().get_data().del_volume(id)):
                    self.__tree_store.remove(iter)
            
            message.destroy()        
            return (id, type)
        else:
            message.destroy()
            return None
        
                
    def on_button_rename_ok_clicked(self, widget, data=None):
        if self.__dialog_rename:
            (id, type, path, iter) = self.__dialog_rename.info
            new_text = self.__builder.get_object('entry_rename').get_text()
            
            if (type == CatalogTreeView.ITEM_TYPE_CATALOG):
                if (get_manager().get_data().ren_catalog(id, new_text)):
                    self.__tree_store.set_value(iter, 1, new_text)
            else:
                if (get_manager().get_data().ren_volume(id, new_text)):
                    self.__tree_store.set_value(iter, 1, new_text)
            self.__dialog_rename.response(gtk.RESPONSE_OK)
    
    def on_button_rename_cancel_clicked(self, widget, data=None):
        if self.__dialog_rename:
            self.__dialog_rename.response(gtk.RESPONSE_CANCEL)
    