'''
Created on Jun 18, 2009

@author: santiago
'''

import sys
import gtk

from os import listdir
from os.path import exists, isdir, isfile, getsize, join, getmtime

from Pytalog.Lib import get_manager

if sys.platform == 'win32':
    import Pytalog.Platform.Windows as sysinfo
elif 'linux' in sys.platform:
    import Pytalog.Platform.Linux as sysinfo
else:
    import Pytalog.Platform.NotSupported as sysinfo

from Pytalog.Platform import VolumeInformation

class AddVolume(object):
    '''
    Code behind encargado de manejar el agregado de medios removibles a un catalogo.
    '''

    FILE_CHOOSER = 'filechooser'
    WINDOW = 'window'
    
    LISTSTORE = 'liststore_volumes'
    LISTSTORE_DEV_NAME = 0
    LISTSTORE_LABEL = 2
    LISTSTORE_MEDIA = 3
    
    ICON_MEDIA = 'image_volume_media'
    ICON_CUSTOM = 'image_volume_custom'
    
    def __init__(self):
        self.__builder = gtk.Builder()
        self.__builder.add_from_file('add_volume.glade')
        self.__builder.connect_signals(self)
        
        self.__filechooser = self.__builder.get_object(AddVolume.FILE_CHOOSER)
        self.__window = self.__builder.get_object(AddVolume.WINDOW)
        self.__liststore = self.__builder.get_object(AddVolume.LISTSTORE)

    def show(self, parent_widget, catalog_id):
        self.__parent = parent_widget
        self.__catalog = get_manager().get_data().get_catalog(catalog_id)

        icon_media = self.__builder.get_object(AddVolume.ICON_MEDIA)
        icon_media_stock_id = icon_media.get_stock()[0]
        
        icon_custom = self.__builder.get_object(AddVolume.ICON_CUSTOM)
        icon_custom_stock_id = icon_custom.get_stock()[0]
        
        drives = sysinfo.get_drives()
        if drives:
            for drive in drives:
                self.__drives = drives
                self.__liststore.prepend([drive.dev_name, icon_media_stock_id, drive.label, True])
                self.__window.show()
   
    def on_volume_cancel_clicked(self, widget, data=None):
        self.__window.destroy()
   
    def on_volume_add_clicked(self, widget, data=None):
       if self.__selected:
           (dev_name, label, is_media) = self.__selected
           
           if is_media:
               def filter_dev_name(x): return x.dev_name == dev_name
               result_selected = filter(filter_dev_name, self.__drives)
               
               if result_selected:
                   if len(result_selected) > 0:
                       self.add_volume(result_selected[0].mount_path, result_selected[0].label)
           else:
               pass
   
    def on_combobox_volume_changed(self, widget, data=None):
        index = widget.get_active()
        if index >= 0:
            iter = widget.get_model().get_iter(index)
            dev_name = widget.get_model().get_value(iter, AddVolume.LISTSTORE_DEV_NAME)
            label = widget.get_model().get_value(iter, AddVolume.LISTSTORE_LABEL)
            is_media = widget.get_model().get_value(iter, AddVolume.LISTSTORE_MEDIA)
     
            self.__selected = (dev_name, label, is_media)
    
    def add_volume(self, path, label):
        new_volume_id = get_manager().get_data().add_volume(self.__catalog.catalog_id, label)
        if new_volume_id:
            self.load_directory_content(new_volume_id, None, path, path)
            self.__parent.update()
            self.__window.destroy()

    def load_directory_content(self, volume_id, parent_id, path, base_path):
        #Leer los archivos.
        (directories, files) = self.get_directory_content(path, base_path)

        #Agregar archivos a la DB.
        get_manager().get_data().add_files_to_volume(volume_id, files, parent_id)
        
        for directory in directories:
            new_directory_id = get_manager().get_data().add_directory_to_volume(volume_id, directory, parent_id)
            
            directory_name = directory['name']
            directory_path = join(path, directory_name)
            
            self.load_directory_content(volume_id, new_directory_id, directory_path, base_path)
    
    def get_directory_content(self, path, base_path):
        files = []
        directories = []
        
        if exists(path) and isdir(path):
            content = listdir(path)
            
            for item in content:
                full_item = join(path, item)
                relative_item = full_item[len(base_path):].lstrip('/')
                
                if isdir(full_item):
                    directories.append({'name':unicode(item), 'full_name':unicode(relative_item)})
                elif isfile(full_item):
                    size = getsize(full_item)
                    mod_time = getmtime(full_item)
                    files.append({'name':unicode(item), 'full_name':unicode(relative_item), 'size':size, 'mtime':mod_time})
                    
            return (directories, files)
        else:
            return None
        