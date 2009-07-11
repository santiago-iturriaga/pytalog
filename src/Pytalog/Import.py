'''
Created on Jul 10, 2009

@author: santiago
'''

import sys, gtk

class Import(object):
    '''
    Import window code-behind
    '''

    def __init__(self, principal):
        self.__principal = principal
        
        self.__builder = gtk.Builder()
        self.__builder.add_from_file("import.glade")
        self.__builder.connect_signals(self)
        
        self.__assistant = self.__builder.get_object("assistant")        
        #self.__assistant.set_forward_page_func(self.page_func)

        self.__combo_intro_type = self.__builder.get_object("liststore_source_type")
                 
    def show(self):
        self.__assistant.show()
        
    def 
        
    '''
    Assistant signals
    '''
        
    def on_assistant_apply(self, widget, data=None):
        print "on_assistant_apply"
    
    def on_assistant_cancel(self, widget, data=None):
        print "on_assistant_cancel"
        self.__assistant.destroy()
    
    def on_assistant_close(self, widget, data=None):
        print "on_assistant_close"
        self.__assistant.destroy()
    
    def on_assistant_prepare(self, widget, page, data=None):
        print "on_assistant_prepare"
        self.__assistant.set_page_complete(page, True)
    
    def page_func(self, current_page, user_data):
        print "page_func"