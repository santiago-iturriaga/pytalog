'''
Created on Jun 18, 2009

@author: santiago
'''

import pymediafinder

def get_drives():
    '''
    Retorna una lista con todos las unidades de almacenamiento disponibles junto con su espacio disponible.
    '''
    result = pymediafinder.find()
    print result
    
    return None