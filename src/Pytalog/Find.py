'''
Created on Jul 9, 2009

@author: santiago
'''

import sys, gtk

class Find(object):
    '''
    Code-behind de la ventana de Find
    '''

    def __init__(self, principal):
        self.__principal = principal
        
        self.__builder = gtk.Builder()
        self.__builder.add_from_file("find.glade")
        self.__builder.connect_signals(self)
        
        self.__window = self.__builder.get_object("window")
        self.__entryFindText = self.__builder.get_object("entryFindText")
    
    def show(self):
        self.__window.show()
        
    def on_buttonFind_clicked(self, widget, data=None):
        if self.__entryFindText.get_text():
            print "entry: {0}".format(self.__entryFindText.get_text())
        pass
    
    def on_buttonCancel_clicked(self, widget, data=None):
        self.__window.destroy()