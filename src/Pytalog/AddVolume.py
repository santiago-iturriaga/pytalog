'''
Created on Jun 18, 2009

@author: santiago
'''

import sys
import gtk

from os import listdir
from os.path import exists, isdir, isfile, getsize, join, getmtime, splitext
from thread import start_new_thread
from datetime import date, datetime

from Pytalog.Lib import get_manager
from Pytalog import Humanize
from Pytalog import Dialogs
from Pytalog.Lib.Data import Errors

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
        
        self.__selected = None

    def show(self, parent_widget, catalog_id):
        self.__parent = parent_widget
        self.__catalog = get_manager().get_catalog_data().get_catalog(catalog_id)

        icon_media = self.__builder.get_object(AddVolume.ICON_MEDIA)
        icon_media_stock_id = icon_media.get_stock()[0]
        
        icon_custom = self.__builder.get_object(AddVolume.ICON_CUSTOM)
        icon_custom_stock_id = icon_custom.get_stock()[0]
        
        drives = sysinfo.get_drives()
        if drives:
            self.__drives = drives
            for drive in drives:
                self.__liststore.prepend([drive.dev_name, icon_media_stock_id, drive.label, True])
                
            self.__window.show()
        else:
            Dialogs.ShowErrorMessage(self.__window, "No mounted removable device could be found. Please mount a removable device and try again.")
            self.__window.destroy()
   
    def on_volume_cancel_clicked(self, widget, data=None):
        self.__window.destroy()
   
    def on_volume_add_clicked(self, widget, data=None):
        try:
            if self.__selected:
                (dev_name, label, is_media) = self.__selected
                
                if is_media:
                    def filter_dev_name(x): return x.dev_name == dev_name
                    result_selected = filter(filter_dev_name, self.__drives)
               
                    if result_selected:
                        if len(result_selected) > 0:
                            self.add_volume(result_selected[0].mount_path, result_selected[0].label)
        except Errors.DuplicateNameError:
            Dialogs.ShowErrorMessage(self.__window, "A volume with that name already exists. You cannot have two volumes with the same name.")
        except:
            Dialogs.ShowCurrentError(self.__window)
   
    def on_combobox_volume_changed(self, widget, data=None):
        index = widget.get_active()
        if index >= 0:
            iter = widget.get_model().get_iter(index)
            dev_name = widget.get_model().get_value(iter, AddVolume.LISTSTORE_DEV_NAME)
            label = widget.get_model().get_value(iter, AddVolume.LISTSTORE_LABEL)
            is_media = widget.get_model().get_value(iter, AddVolume.LISTSTORE_MEDIA)
     
            self.__selected = (dev_name, label, is_media)
    
    def add_volume(self, path, label):
        new_volume_id = get_manager().get_volume_data().add_volume(self.__catalog.catalog_id, label)
        if new_volume_id:
            self.__window.hide()
            
            progressBuilder = gtk.Builder()
            progressBuilder.add_from_file("progress.glade")
            progressWindow = progressBuilder.get_object("progress.window")
            progress = progressBuilder.get_object("progress.progressbar")
            progressWindow.show()
            
            while gtk.events_pending():
                gtk.main_iteration()
            
            try:
                load_directory_content(progress, new_volume_id, None, path, path)
            except Exception as e:
                Dialogs.ShowCurrentError(self.__window)
            finally:
                progressWindow.destroy()
                self.__parent.update()
                self.__window.destroy()

'''
Operaciones de carga de contenido.
'''

def load_directory_content(progress, volume_id, parent_id, path, base_path):
    refresh_progress(progress)
    
    #Leer los archivos.
    (directories, files) = get_directory_content(path, base_path)

    #Agregar archivos a la DB.
    get_manager().get_volume_data().add_files_to_volume(volume_id, files, parent_id)
    
    for directory in directories:
        refresh_progress(progress, False)
        
        new_directory_id = get_manager().get_volume_data().add_directory_to_volume(volume_id, directory, parent_id)
        
        directory_name = directory['name']
        directory_path = join(path, directory_name)
        
        load_directory_content(progress, volume_id, new_directory_id, directory_path, base_path)

def get_directory_content(path, base_path):
    files = []
    directories = []
    
    if exists(path) and isdir(path):
        content = listdir(path)
        
        for item in content:
            full_item = join(path, item)
            relative_item = full_item[len(base_path):].lstrip('/')
            
            if isdir(full_item):
                directories.append({'name':unicode(item), 
                                    'full_name':unicode(relative_item)})
                
            elif isfile(full_item):
                size = getsize(full_item)
                mod_time = datetime.fromtimestamp(getmtime(full_item))
                (name_without_extension, name_extension_only) = splitext(item)  
                
                files.append({'name':unicode(item), 
                              'full_name':unicode(relative_item),
                              'name_extension_only':unicode(name_extension_only.strip().lower()),
                              'name_without_extension':unicode(name_without_extension),
                              'size':size, 
                              'mtime':mod_time})
            
        return (directories, files)
    else:
        return None
    
def refresh_progress(progress, do_pulse=True):
    if do_pulse:
        progress.pulse()
        
    while gtk.events_pending():
        gtk.main_iteration()
        