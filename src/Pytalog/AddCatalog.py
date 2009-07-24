'''
Created on Jun 15, 2009

@author: santiago
'''

import sys
import gtk

from Pytalog.Lib import get_manager

class AddCatalog(object):
    '''
    Code-behind de la ventana de agregar catalogo
    '''

    def __init__(self):
        self.__builderAddCatalog = gtk.Builder()
        self.__builderAddCatalog.add_from_file('add_catalog.glade')
        self.__builderAddCatalog.connect_signals(self)
                
        self.__window_add_catalog = self.__builderAddCatalog.get_object('window')
        self.__label_catalog_name = self.__builderAddCatalog.get_object('entryName')
        
    def show(self, updateWidget=None):
        self.__updateWidget = updateWidget
        self.__window_add_catalog.show()
             
    def on_buttonOk_clicked(self, widget, data=None):
        name = self.__label_catalog_name.get_text()
        
        if (name):
            get_manager().get_catalog_data().add_catalog(name)
            
            if (self.__updateWidget):
                self.__updateWidget.update()
                
            self.__window_add_catalog.destroy()
    
    def on_buttonCancel_clicked(self, widget, data=None):
        self.__window_add_catalog.destroy()
