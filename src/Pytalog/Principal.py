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

class Principal(object):
    '''
    Code-behind de la ventana principal.
    '''
    
    WINDOW_MAIN = 'window'
       
    def __init__(self):
        self.__builder = gtk.Builder()
        self.__builder.add_from_file('principal.glade')
        self.__builder.connect_signals(self)
        
        self.__principal = self.__builder.get_object(Principal.WINDOW_MAIN)
             
        self.__tree_view = CatalogTreeView(self, self.__builder)
        self.__tree_view.load_catalogs()

    def show(self):
        self.__principal.show()

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def update(self):
        '''
        Operación invocada por otras ventanas cuando se quiere refrescar
        el tree view.
        '''
        
        self.__tree_view.load_catalogs()

    '''
    Signals del menu principal.
    '''
    
    def on_menuitemQuit_activate(self, widget, data=None):
        gtk.main_quit()
    
    def on_menuitemAbout_activate(self, widget, data=None):
        About().show()
        
    def on_menuitemOpenCatalog_activate(self, widget, data=None):
        pass
    
    def on_menuitemNewCatalog_activate(self, widget, data=None):
        AddCatalog().show(self)
    
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
        self.__tree_view.on_menu_tree_delete_activate(widget, data)
       
    def on_cellVolumesName_edited(self, widget, path, new_text, data=None):
        self.__tree_view.on_cellVolumesName_edited(widget, path, new_text, data)
    
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
    
    def __init__(self, principal, builder):
        self.__principal = principal
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

    def __get_item_from_path(self, path):
        '''
        Dado un path de un item en el treeview retorna una lista con (id, type, iter).
        '''
        iter = self.__tree_store.get_iter(path)

        id = self.__tree_store.get_value(iter, 0)
        type = self.__tree_store.get_value(iter, 3)
        
        return (id, type, iter)

    def on_treeviewVolumes_cursor_changed(self, widget, data=None):
        treeselection = widget.get_selection()
        (model, iter) = treeselection.get_selected()
        catalog_or_volume_id = model.get_value(iter, 0)
        #print "Selected: <'%s'>" % (catalog_or_volume_id)
          
    def on_treeviewVolumes_row_activated(self, widget, path, view_column, data=None):
        #print "Activated: <'%s'>" % (path)
        pass
    
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
        AddVolume().show(self.__principal, id)
    
    def on_menu_tree_rename_activate(self, widget, data=None):
        (id, type, iter, path) = self.__menu_tree.current_item
        column = self.__tree_view.get_column(0)
        renderer = column.get_cell_renderers()[1]
                
        self.__tree_view.grab_focus()
        self.__tree_view.set_cursor_on_cell(path, column, renderer, True)
    
    def on_menu_tree_delete_activate(self, widget, data=None):
        (id, type, iter, path) = self.__menu_tree.current_item
        
        if (type == CatalogTreeView.ITEM_TYPE_CATALOG):
            if (get_manager().get_data().del_catalog(id)):
                self.__tree_store.remove(iter)
        else:
            if (get_manager().get_data().del_volume(id)):
                self.__tree_store.remove(iter)
       
    def on_cellVolumesName_edited(self, widget, path, new_text, data=None):
        (id, type, iter) = self.__get_item_from_path(path)
        
        if (type == CatalogTreeView.ITEM_TYPE_CATALOG):
            if (get_manager().get_data().ren_catalog(id, new_text)):
                self.__tree_store.set_value(iter, 1, new_text)
        else:
            if (get_manager().get_data().ren_volume(id, new_text)):
                self.__tree_store.set_value(iter, 1, new_text)
                