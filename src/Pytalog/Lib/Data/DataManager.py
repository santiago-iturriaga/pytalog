# coding=utf-8
'''
Created on Jun 11, 2009

@author: santiago
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Pytalog.Lib.Data import Base
from Pytalog.Lib.Data.Entities.Catalog import Catalog
from Pytalog.Lib.Data.Entities.Volume import Volume

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
        '''
        session = self.__db_session()
        new_catalog = Catalog(name)
        
        session.add(new_catalog)
        session.commit()
        
        return new_catalog
    
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
        session =  self.__db_session()
        catalog = self.get_catalog(id, session)
        
        if (catalog):
            catalog.name = new_name

            session.add(catalog)
            session.commit()
            return True
    
        return False
    
    def get_catalog(self, id, session=None):
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
    
    def del_volume(self, id):
        pass
    
    def ren_volume(self, id, label):
        pass
    
    def get_volumes(self, catalog_id):
        '''
        Retorna todos los volumenes de un catalogo.
        '''
        session = self.__db_session()
        catalog = session.query(Catalog).filter_by(catalog_id=catalog_id).one()
        volumes = catalog.volumes

        return volumes
    