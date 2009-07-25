'''
Created on Jul 9, 2009

@author: santiago
'''

import sys, gtk

from Pytalog.Humanize import HumanizeSize
from Pytalog.Lib import get_manager 

class Find(object):
    '''
    Code-behind de la ventana de Find
    '''

    ENTRY_FIND_TEXT = "entryFindText"
    
    IMAGE_FILE = "image_file"
    IMAGE_DIRECTORY = "image_directory"

    LIST_STORE = "liststore_result"

    ITEM_TYPE_DIRECTORY = 0
    ITEM_TYPE_FILE = 1

    def __init__(self, principal):
        self.__principal = principal
        
        self.__builder = gtk.Builder()
        self.__builder.add_from_file("find.glade")
        self.__builder.connect_signals(self)
        
        self.__window = self.__builder.get_object("window")
        self.__entryFindText = self.__builder.get_object(Find.ENTRY_FIND_TEXT)
    
        image_file_control = self.__builder.get_object(Find.IMAGE_FILE)
        self.__image_file_stockid = image_file_control.get_stock()[0]        
        
        image_directory_control = self.__builder.get_object(Find.IMAGE_DIRECTORY)
        self.__image_directory_stockid = image_directory_control.get_stock()[0]
        
        self.__list_store = self.__builder.get_object(Find.LIST_STORE)
    
    def show(self):
        self.__window.show()
        
    def on_buttonFind_clicked(self, widget, data=None):
        if self.__entryFindText.get_text():
            text_to_find = self.__entryFindText.get_text()
            (directories, files) = get_manager().get_find_data().find_text(text_to_find)
            
            self.__list_store.clear()
            
            for directory in directories:
                self.__list_store.append([directory.directory_id, 
                                          Find.ITEM_TYPE_DIRECTORY,
                                          self.__image_directory_stockid,  
                                          directory.name, 
                                          '', 
                                          directory.volume.catalog.name,
                                          directory.volume.catalog.catalog_id,
                                          directory.volume.label,
                                          directory.volume.volume_id,
                                          "",
                                          directory.parent_directory_id])

            for file in files:
                self.__list_store.append([file.file_id, 
                                          Find.ITEM_TYPE_FILE,
                                          self.__image_file_stockid,
                                          file.name, 
                                          HumanizeSize(file.size),
                                          file.volume.catalog.name,
                                          file.volume.catalog.catalog_id,
                                          file.volume.label,
                                          file.volume.volume_id,
                                          file.parent_directory.name,
                                          file.parent_directory_id])
    
    def on_buttonCancel_clicked(self, widget, data=None):
        self.__window.destroy()
        
    def __get_item_from_path(self, path):
        '''
        Dado un path de un item en el listview retorna una tupla con (id, type, iter).
        '''
        iter = self.__list_store.get_iter(path)

        id = self.__list_store.get_value(iter, 0)
        type = self.__list_store.get_value(iter, 1)
        
        return (id, type, iter)
        
    def on_treeviewResult_row_activated(self, widget, path, view_column, data=None):
        (id, type, iter) = self.__get_item_from_path(path)
        volume_id = self.__list_store.get_value(iter, 8)
        catalog_id = self.__list_store.get_value(iter, 6)
        
        if (type == Find.ITEM_TYPE_DIRECTORY):
            self.__principal.load_directory(id, (catalog_id, volume_id))
        elif (type == Find.ITEM_TYPE_FILE):
            parent_id = self.__list_store.get_value(iter, 10)
            self.__principal.load_directory(parent_id, (catalog_id, volume_id))
            