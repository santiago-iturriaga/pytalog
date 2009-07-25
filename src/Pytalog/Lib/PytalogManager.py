#coding=utf-8

'''
Created on Jun 10, 2009

@author: santiago
'''

from Pytalog.Lib.Data.DataManager import DataManager, CatalogManager, VolumeManager, FindManager

class PytalogManager(object):
    '''
    Acceso a la logica del sistema.
    '''

    def __init__(self):
        '''
        Fachada de acceso al sistema.
        '''
        self.__db_manager = DataManager()
        
    def get_data(self):
        '''
        Retorna una instancia del manajador de datos.
        '''
        return self.__db_manager
    
    def get_catalog_data(self):
        '''
        Retorna una instancia del manejador de datos de catalogos.
        '''
        return CatalogManager(self.__db_manager) 
    
    def get_volume_data(self):
        '''
        Retorna una instancia del manejador de datos de volumenes.
        '''
        return VolumeManager(self.__db_manager)
    
    def get_find_data(self):
        '''
        Retorna una instanca del manejador de datos de búsquedas.
        '''
        return FindManager(self.__db_manager)