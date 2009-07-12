#coding=utf-8
'''
Created on Jul 11, 2009

@author: santiago
'''

import csv
from os import path
import datetime

from Pytalog.Lib import get_manager

class VolumeCache(object):
    '''
    Actúa como un cache de path de directorios para no recalcular siempre el camino a un directorio.
    Se utiliza un cache muy simple que solo se mantiene para un volumen a la vez. Esto asegura que no se
    utilizará mucha memoria en el cache pero resulta efectivo si todos los archivos de un mismo volumen
    se encuentran consecutivos en el archivo de importación.
    '''   
    def __init__(self, volume_id):
        self.__volume_id = volume_id
        self.__directory_cache = {}
        
    @property
    def volume_id(self):
        return self.__volume_id
        
    def add_path(self, path, directory_id):
        self.__directory_cache[path] = directory_id

    def get_path_id(self, path):
        return self.__directory_cache.get(path)

class VVVCSVImport(object):
    '''
    Clase encargada de importar el contenido de un archivo CSV exportado por el programa VVV (http://vvvapp.sourceforge.net/).
    '''

    def __init__(self):
        pass
        
    def description(self):
        return "VVV CSV file"
    
    def import_data(self, catalog_id, filename, status_callback=None):
        #try:
        catalog = get_manager().get_data().get_catalog(catalog_id)
        created_volumes = {}
        simple_cache = None
        line = 0
        
        reader = csv.reader(open(filename, "rb"))
        for row in reader:
            raw_volume_label = row[0]
            raw_path = row[1]
            raw_name = row[2]
            raw_size = row[3]
            raw_ext = row[4]
            raw_date = row[5]

            clean_volume_label = unicode(raw_volume_label.strip())
            clean_path = unicode(raw_path.strip())
            
            status_callback(len(created_volumes) %100, "Reading {0}".format(clean_volume_label), len(created_volumes), False)

            # Obtengo o creo el volumen
            volume_id = created_volumes.get(clean_volume_label)           
            if not volume_id:
                volume = get_manager().get_data().get_volume_from_catalog_by_label(catalog_id, clean_volume_label)
                if volume:
                    status_callback(None, "Error: a volume labeled '{0}' already exists on the specified catalog.".format(clean_volume_label),
                                    None, True)
                    yield False
                else:
                    volume_id = get_manager().get_data().add_volume(catalog_id, clean_volume_label)
                    created_volumes[clean_volume_label] = volume_id

            if not simple_cache:
                simple_cache = VolumeCache(volume_id)

            if simple_cache.volume_id != volume_id:
                simple_cache = VolumeCache(volume_id)
                
            # Obtengo o creo el directorio
            directory_id = simple_cache.get_path_id(clean_path)
            if not directory_id:
                directory_id = self.create_path(simple_cache, clean_path)
            
            # Creo el archivo
            clean_name = unicode(raw_name.strip())
            clean_size = long(raw_size.strip())
            clean_ext = ".{0}".format(raw_ext.strip().lower())
            
            #08/26/2005 08:45:14 AM
            #mm/dd/yyyy hh:mm:ss AM
            clean_date = datetime.datetime.strptime(raw_date, "%m/%d/%Y %I:%M:%S %p")             
            
            (split_name_without_ext, split_ext) = path.splitext(clean_name)
            clean_name_without_ext = split_name_without_ext.strip()
            
            clean_full_name = path.join(clean_path, clean_name)           
            
            file = {
                    'name':clean_name, 
                    'full_name':clean_full_name,
                    'name_extension_only':clean_ext,
                    'name_without_extension':clean_name_without_ext,
                    'size':clean_size, 
                    'mtime':clean_date }
            
            get_manager().get_data().add_files_to_volume(volume_id, [file], directory_id)
            
            line+=1
            yield True
            
        status_callback(100, "Finished", len(created_volumes), False)
        yield False
        #except e:
        #    status_callback(None, "Error!",None, True)

    def get_volume_root(self, simple_cache):
        root_id = simple_cache.get_path_id('/')
        if not root_id:
            root = get_manager().get_data().get_volume_root_directory(simple_cache.volume_id)
            root_id = root.directory_id
            simple_cache.add_path('/', root_id)

        return root_id

    def create_path(self, simple_cache, full_path):
        (parent_path, directory_name) = path.split(full_path)
        
        parent_directory_id = simple_cache.get_path_id(parent_path)
        if not parent_directory_id:
            if parent_path == '' or parent_path == '/':
                parent_directory_id = self.get_volume_root(simple_cache) 
            else:
                parent_directory_id = self.create_path(simple_cache, parent_path)
                
        if directory_name and parent_directory_id:
            directory_id = get_manager().get_data(). \
                add_directory_to_volume(simple_cache.volume_id, 
                                        {'name': directory_name, 'full_name': full_path.lstrip('/')}, 
                                        parent_directory_id)
            simple_cache.add_path(full_path, directory_id)
        else:
            directory_id = parent_directory_id

        return directory_id

    def get_path_list(self, current_path):
        '''
        Retorna una lista con los nombres de los directorios que componen el camino.
        '''
        
        (rest, tail) = path.split(current_path)
        
        if rest == '' or rest == '/':
                if tail == '':
                        return []
                else:
                        return [tail]
        else:
                rest_list = self.get_path_list(rest)
                rest_list.append(tail)
                return rest_list
