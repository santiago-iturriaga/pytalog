'''
Created on Jun 11, 2009

@author: santiago
'''

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref

from Pytalog.Lib.Data import Base

class Catalog(Base):
    '''
    Un catalogo contiene volumenes. 
    Cada volumen representa un medio de almacenamiento (CD/DVD/etc.).
    '''

    __tablename__ = "catalogs"
    
    catalog_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    #volumes = relation("Volume", backref=backref('catalog'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Entities.Catalog('%s','%s')>" % (self.id, self.name)