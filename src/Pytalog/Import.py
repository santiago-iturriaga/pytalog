#coding=utf-8
'''
Created on Jul 10, 2009

@author: santiago
'''

import sys, gtk
from functools import partial

from Pytalog.Lib.External.VVVCSVImport import VVVCSVImport 

class Import(object):
    '''
    Import window code-behind
    '''

    INTRO_PAGE = 0
    CONFIG_PAGE = 1
    PROGRESS_PAGE = 2
    SUMMARY_PAGE = 3

    def __init__(self, principal):
        self.__principal = principal
        
        self.__builder = gtk.Builder()
        self.__builder.add_from_file("import.glade")
        self.__builder.connect_signals(self)
        
        self.__assistant = self.__builder.get_object("assistant")        
        #self.__assistant.set_forward_page_func(self.page_func)

        self.__intro_combosource_type = self.__builder.get_object("liststore_source_type")
        self.__intro_combo_type = self.__builder.get_object("combobox_src_type")
        self.__intro_file_location = self.__builder.get_object("filechooserbutton_src_location")
        
        self.load_importers()
        self.__selected_importer = None
        self.__selected_file = None
                 
    def show(self):
        self.__assistant.show()
        
    def load_importers(self):
        self.__importers = {0:VVVCSVImport()}
        self.__intro_combosource_type.append([0, self.__importers[0].description()])
       
    def check_intro_complete(self):
        if self.__selected_file and self.__selected_importer:
            intro = self.__assistant.get_nth_page(Import.INTRO_PAGE)
            self.__assistant.set_page_complete(intro, True)
       
    def do_import(self):
        progress = self.__assistant.get_nth_page(Import.PROGRESS_PAGE)
        self.__assistant.set_page_complete(progress, True)
       
    def close(self):
        #self.__assistant.set_forward_page_func(None)
        #self.__builder.disconnect(self.__handler_id)
        self.__assistant.destroy()
       
    '''
    Assistant signals
    '''
        
    def on_assistant_apply(self, widget, data=None):
        pass
    
    def on_assistant_cancel(self, widget, data=None):
        '''
        Se ejecuta cuando el usuario aborta el wizzard.
        '''
        self.close()
    
    def on_assistant_close(self, widget, data=None):
        '''
        Se ejecuta cuando el usuario termina exitosamente el wizzard (Rincewind style)
        '''
        self.close()
    
    def on_assistant_prepare(self, widget, page, data=None):
        index = self.__assistant.get_current_page()
        
        if index == Import.CONFIG_PAGE:
            self.__assistant.set_page_complete(page, True)
        elif index == Import.PROGRESS_PAGE:
            self.do_import()
            
    #def page_func(self, current_page):
    #    '''
    #    Es el comportamiento por defecto, lo implementé igual de pelotilla nomás.
    #    '''
    #    index = self.__assistant.get_current_page()
    #    self.__assistant.set_current_page(index+1)
        
    '''
    Intro signals
    '''
    
    def on_combobox_src_type_changed(self, widget, data=None):
        iter = self.__intro_combo_type.get_active_iter()
        
        if iter:
            self.__selected_importer = self.__importers[self.__intro_combosource_type.get_value(iter, 0)]
        else:
            self.__selected_importer = None
            
        self.check_intro_complete()
    
    def on_filechooserbutton_src_location_file_set(self, widget, data=None):
        filename = self.__intro_file_location.get_filename()
        
        if filename:
            self.__selected_file = filename
        else:
            self.__selected_file = None
            
        self.check_intro_complete()
