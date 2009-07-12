#coding=utf-8
'''
Created on Jul 12, 2009

@author: santiago
'''

class DataError(Exception):
    '''
    Error genérico de la capa de datos
    '''
    pass

class DuplicateNameError(DataError):
    '''
    No es posible tener dos registros con el mismo nombre.
    '''   
    
    def __init__(self, description=None):
        self.description = description
        
    def __str__(self):
        return repr(self.description)
    