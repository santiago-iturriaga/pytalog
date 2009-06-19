'''
Created on Jun 5, 2009

@author: santiago
'''

import sys
import gtk

class About(object):
    '''
    Code-behind del dialogo de About 
    '''
    
    def __init__(self):
        '''
        Constructor por defecto
        '''
        self.__builderAbout = gtk.Builder()
        self.__builderAbout.add_from_file('about.glade')
        self.__builderAbout.connect_signals(self)
                
        self.__windowAbout = self.__builderAbout.get_object('aboutdialog')
    
    def show(self):
        '''
        Muestra el dialogo
        '''
        self.__windowAbout.run()
        self.__windowAbout.destroy();
        