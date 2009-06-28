# coding=utf-8
'''
Created on Jun 11, 2009

@author: santiago
'''

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Pytalog.Lib.Data import Base
from Pytalog.Lib.Data.Entities.Catalog import *
from Pytalog.Lib.Data.Entities.Volume import *

class DataManager(object):
    '''
    Manejador de la persistencia de datos.
    '''

    def __init__(self):
        '''
        Inicializa la conexión con la base de datos y verifica el schema.
        '''
        self.__setup_db__()
        self.__check_db__()
            
    def __setup_db__(self):
        '''
        Inicializa una conexion a la base de datos.
        '''
        self.__db_engine = create_engine('sqlite:///catalog.db')
        self.__db_session = sessionmaker(bind=self.__db_engine)
            
    def __check_db__(self):
        '''
        Verifica que el modelo de datos se encuentre creado.
        En caso de no estarlo las entidades que faltan son creadas.
        '''
        Base.metadata.create_all(self.__db_engine)
    
    def add_catalog(self, name):
        '''
        Agrega un nuevo catalogo.
        
        Retorna el ID del nuevo catalogo.
        '''
        session = self.__db_session()
        new_catalog = Catalog(name)
        
        session.add(new_catalog)
        session.commit()
        
        return new_catalog.catalog_id
    
    def del_catalog(self, id):
        '''
        Elimina un catalogo.
        '''
        session = self.__db_session()
        catalog = self.get_catalog(id, session)
        
        if (catalog):
            session.delete(catalog)
            session.commit()
            return True
            
        return False
    
    def ren_catalog(self, id, new_name):
        '''
        Renombra un catalogo.
        '''
        session =  self.__db_session()
        catalog = self.get_catalog(id, session)
        
        if (catalog):
            catalog.name = new_name

            session.add(catalog)
            session.commit()
            return True
    
        return False
    
    def get_catalog(self, id, session=None):
        '''
        Obtiene un catalog.
        '''
        if (not session):
            session = self.__db_session()
        
        catalogs = session.query(Catalog).filter(Catalog.catalog_id == id).all()
        
        if (len(catalogs) > 0):
            return catalogs[0]
            
        return None
    
    def get_catalogs(self):
        '''
        Retorna todos los catalogos disponibles.
        '''
        return self.__db_session().query(Catalog).order_by(Catalog.name).all()
    
    def add_volume(self, catalog_id, label):
        '''
        Crea un nuevo volúmen y lo agrega a un catalogo.
        Además crea el directorio ROOT del nuevo volúmen.
        
        Retorna el ID del nuevo volumen.
        '''
        session = self.__db_session()
        
        new_volume = Volume(catalog_id, label, datetime.datetime.today())
        session.add(new_volume)
        session.commit()
        
        new_volume_root = VolumeDirectory(".", ".", new_volume.volume_id, None)
        session.add(new_volume_root)
        session.commit()
        
        return new_volume.volume_id
    
    def del_volume(self, id):
        '''
        Elimina un volumen.
        '''
        session = self.__db_session()
        
        volume = self.get_volume(id, session)
        if volume:
            session.delete(volume)
            session.commit()
            return True
        else:
            return False
    
    def ren_volume(self, id, label):
        '''
        Renombra un volumen.
        '''
        session = self.__db_session()
        
        volume = self.get_volume(id, session)
        if volume:
            volume.label = label
            session.add(volume)
            session.commit()
            
            return True
        else:
            return False
    
    def get_volumes(self, catalog_id):
        '''
        Retorna todos los volumenes de un catalogo.
        '''
        session = self.__db_session()
        catalog = session.query(Catalog).filter_by(catalog_id=catalog_id).one()
        volumes = catalog.volumes

        return volumes
    
    def get_volume(self, volume_id, session=None):
        '''
        Obtiene un volumen.
        '''
        if (not session):
            session = self.__db_session()
            
        volumes = session.query(Volume).filter(Volume.volume_id == volume_id).all()
        
        if volumes:
            if len(volumes) > 0:
                return volumes[0]
        
        return None 
            
    def get_volume_root_directory(self, volume_id, session=None):
        '''
        Obtiene el directorio raiz de un volumen.
        Todo volumen tiene un único directorio raiz con nombre '.' 
        y sin diectorio padre. 
        '''
        if (not session):
            session = self.__db_session()
             
        directories = session.query(VolumeDirectory).filter(VolumeDirectory.volume_id==volume_id).filter(VolumeDirectory.parent_directory_id==None).all()
                                                            
        if directories:
            if len(directories) > 0:
                return directories[0]
                
        return None

    def get_volume_directory(self, volume_id, directory_id, session=None):
        '''
        Obtiene un directorio de un volumen.
        '''
        if (not session):
            session = self.__db_session()
             
        directories = session.query(VolumeDirectory).filter(VolumeDirectory.volume_id==volume_id).filter(VolumeDirectory.directory_id==directory_id).all()
                                                            
        if directories:
            if len(directories) > 0:
                return directories[0]
                
        return None
    
    def add_files_to_volume(self, volume_id, files, parent_directory_id=None):
        '''
        Agrega una lista de archivos a un directorio de un volumen.
        Si no se especifica un directorio los archivos son agregados al directorio raiz del volumen.
        
        files = {
            'name':unicode(name), 
            'full_name':unicode(full_name), 
            'name_extension_only':unicode(name_extension_only), 
            'name_without_extension':unicode(name_without_extension), 
            'size':size, 
            'mtime':mtime
            }
        '''
        session = self.__db_session()
        
        if parent_directory_id == None:
            parent_directory = self.get_volume_root_directory(volume_id, session)
        else:
            parent_directory = self.get_volume_directory(volume_id, parent_directory_id, session)
            
        if parent_directory:
            for file_desc in files:
                name = file_desc['name']
                full_name = file_desc['full_name']
                size = file_desc['size']
                mtime = file_desc['mtime']
                name_extension_only = file_desc['name_extension_only']
                name_without_extension = file_desc['name_without_extension']
                
                new_file = VolumeFile(name, full_name, name_without_extension, name_extension_only, 
                                      size, mtime, volume_id, parent_directory.directory_id)
                session.add(new_file)
                
            session.commit()
            
            return True
        else:
            return False

    def add_directory_to_volume(self, volume_id, directory, parent_directory_id=None):
        '''
        Agrega un subdirectorio a un directorio de un volumen.
        Si no se especifica un directorio destino el subdirectorio se crea en el directorio
        raiz del volumen.
        '''
        session = self.__db_session()
        
        if parent_directory_id == None:
            parent_directory = self.get_volume_root_directory(volume_id, session)
        else:
            parent_directory = self.get_volume_directory(volume_id, parent_directory_id, session)
            
        if parent_directory:
            name = directory['name']
            full_name = directory['full_name']
            
            new_directory = VolumeDirectory(name, full_name, volume_id, parent_directory.directory_id)
            session.add(new_directory)
                
            session.commit()
            
            return new_directory.directory_id
        else:
            return None
        
    def get_volume_content(self, volume_id, parent_directory_id=None):
        '''
        Obtiene el contenido de un directorio de un volumen.
        Si no se especifica un directorio se obtiene el contenido del directorio raiz.
        '''
        session = self.__db_session()
        
        if not parent_directory_id:
            parent_directory = self.get_volume_root_directory(volume_id, session)
        else:
            parent_directory = self.get_volume_directory(volume_id, parent_directory_id, session)
            
        if parent_directory:
            directories = session.query(VolumeDirectory). \
                filter(VolumeDirectory.parent_directory_id==parent_directory.directory_id). \
                order_by(VolumeDirectory.name).all()
            files = parent_directory.files
        
            return (directories, files, parent_directory.parent_directory_id)
        else:
            return None
    