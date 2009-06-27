'''
Created on Jun 10, 2009

@author: santiago
'''

from Pytalog.Lib.Data.DataManager import DataManager

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
    