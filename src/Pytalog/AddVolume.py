'''
Created on Jun 18, 2009

@author: santiago
'''

import sys
import gtk

from Pytalog.Lib import get_manager 

if sys.platform == 'win32':
    import Pytalog.Platform.Windows as sysinfo
elif 'linux' in sys.platform:
    import Pytalog.Platform.Linux as sysinfo
else:
    import Pytalog.Platform.NotSupported as sysinfo

class AddVolume(object):
    '''
    Code behind encargado de manejar el agregado de medios removibles a un catalogo.
    '''

    FILE_CHOOSER = 'filechooser'

    def __init__(self):
        self.__builder = gtk.Builder()
        self.__builder.add_from_file('add_volume.glade')
        self.__builder.connect_signals(self)
        
        self.__filechooser = self.__builder.get_object(AddVolume.FILE_CHOOSER)

    def show(self, parent_widget, catalog_id):
        self.__parent = parent_widget
        self.__catalog = get_manager().get_data().get_catalog(catalog_id)
        
        drives = sysinfo.get_drives()
        print "Dispositivos:\n"
        print drives
        
        self.__filechooser.show()
   