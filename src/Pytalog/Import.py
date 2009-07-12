#coding=utf-8
'''
Created on Jul 10, 2009

@author: santiago
'''

import sys, gtk, gobject

from Pytalog import Humanize, Dialogs
from Pytalog.Lib import get_manager
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

        self.__intro_combostore_type = self.__builder.get_object("liststore_src_type")
        self.__intro_combo_type = self.__builder.get_object("combobox_src_type")

        self.load_importers()
        self.__selected_importer = None
        
        self.__intro_file_location = self.__builder.get_object("filechooserbutton_src_location")
        self.__selected_file = None
        
        self.__intro_combostore_dest = self.__builder.get_object("liststore_catalog_dest")
        self.__intro_combo_dest = self.__builder.get_object("combobox_catalog_dest")
        
        self.load_catalogs()
        self.__selected_catalog = None        

        self.__progress_bar = self.__builder.get_object("progressbar")
        self.__progress_label = self.__builder.get_object("labelprogress")
        
        self.__operation_summary = ""
                 
    def show(self):
        self.__assistant.show()
        
    def load_importers(self):
        self.__importers = {0:VVVCSVImport()}
        self.__intro_combostore_type.append([0, self.__importers[0].description()])

    def load_catalogs(self):
        self.__catalogs = get_manager().get_data().get_catalogs()
        for catalog in self.__catalogs:
            self.__intro_combostore_dest.append([catalog.catalog_id, catalog.name])
       
    def check_intro_complete(self):
        if self.__selected_file and self.__selected_importer and self.__selected_catalog:
            intro = self.__assistant.get_nth_page(Import.INTRO_PAGE)
            self.__assistant.set_page_complete(intro, True)
       
    def do_import(self):
        progress_task = self.__selected_importer.import_data(self.__selected_catalog, self.__selected_file, self.do_import_callback)
        gobject.idle_add(progress_task.next)
        
    def do_import_callback(self, current_progress, text, total, error):
        if error:
            self.__operation_summary = "Operation aborted with an error."
            
            Dialogs.ShowErrorMessage(self.__assistant, text)
            
            progress = self.__assistant.get_nth_page(Import.PROGRESS_PAGE)
            self.__assistant.set_page_complete(progress, True)   
        else:
            self.__progress_bar.set_fraction(current_progress/100.0)
            self.__progress_bar.set_text("{0} volumes imported...".format(total))
            self.__progress_label.set_text(text)
            
            if current_progress == 100:
                self.__operation_summary = "Operation ended successfully."
                progress = self.__assistant.get_nth_page(Import.PROGRESS_PAGE)
                self.__assistant.set_page_complete(progress, True)
                self.__principal.update()        
       
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
        
    '''
    Intro signals
    '''
    
    def on_combobox_src_type_changed(self, widget, data=None):
        iter = self.__intro_combo_type.get_active_iter()
        
        if iter:
            self.__selected_importer = self.__importers[self.__intro_combostore_type.get_value(iter, 0)]
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

    def on_combobox_src_catalog_dest_changed(self, widget, data=None):
        iter = self.__intro_combo_dest.get_active_iter()
        
        if iter:
            self.__selected_catalog = self.__intro_combostore_dest.get_value(iter, 0)
        else:
            self.__selected_catalog = None
            
        self.check_intro_complete()
        