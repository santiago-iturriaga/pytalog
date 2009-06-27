'''
Created on Jun 11, 2009

@author: santiago
'''

from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref

from Pytalog.Lib.Data import Base

class Volume(Base):
    '''
    Un volumen representa una unidad de almacenamiento (CD/DVD/etc.).
    '''

    __tablename__ = "volumes"

    volume_id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    size = Column(Numeric, nullable=False)
    created_on = Column(DateTime, nullable=False)
    
    catalog_id = Column(Integer, ForeignKey("catalogs.catalog_id"), nullable=False)
    catalog = relation("Catalog", backref=backref('volumes'))

    def __init__(self, catalog_id, label, size, created_on):
        self.catalog_id = catalog_id
        self.label = label
        self.size = size
        self.created_on = created_on
        
    def __repr__(self):
        return "<Entities.Volume('%s','%s','%s','%s','%s'>" % \
            (self.volume_id, self.label, self.size, self.created_on, self.catalog_id)
    