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
    #size = Column(Numeric, nullable=False)
    created_on = Column(DateTime, nullable=False)
    
    catalog_id = Column(Integer, ForeignKey("catalogs.catalog_id"), nullable=False)
    catalog = relation("Catalog", backref=backref('volumes'), cascade="all, delete", single_parent=True)

    def __init__(self, catalog_id, label, created_on):
        self.catalog_id = catalog_id
        self.label = label
        #self.size = size
        self.created_on = created_on
        
    def __repr__(self):
        return "<Entities.Volume('%s','%s','%s','%s','%s')>" % \
            (self.volume_id, self.label, self.created_on, self.catalog_id)
        
class VolumeDirectory(Base):
    '''
    Representa un directorio dentro de un volumen.
    '''
    
    __tablename__ = "volumesdirectories"
    
    directory_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    
    volume_id = Column(Integer, ForeignKey(Volume.volume_id), nullable=False)
    volume = relation(Volume, backref=backref('directories'), cascade="all, delete", single_parent=True)
    
    parent_directory_id = Column(Integer, ForeignKey('volumesdirectories.directory_id'), nullable=True)
    parent_directory = relation('VolumeDirectory', cascade="all, delete", single_parent=True) #, backref=backref('children_directories')
    
    def __init__(self, name, full_name, volume_id, parent_directory_id):
        self.name = name
        self.full_name = full_name
        self.volume_id = volume_id
        self.parent_directory_id = parent_directory_id
        
    def __repr__(self):
        return "<Entities.VolumeDirectory('%s','%s','%s','%s','%s')>" % \
            (self.directory_id, self.name, self.full_name, self.volume_id, self.parent_directory_id)
        
class VolumeFile(Base):
    '''
    Representa un archivo dentro de un volumen.
    '''
    
    __tablename__ = "volumesfiles"
    
    file_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    size = Column(Numeric, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    
    volume_id = Column(Integer, ForeignKey(Volume.volume_id), nullable=False)
    volume = relation(Volume, backref=backref('files'), cascade="all, delete", single_parent=True)

    parent_directory_id = Column(Integer, ForeignKey(VolumeDirectory.directory_id), nullable=False)
    parent_directory = relation(VolumeDirectory, backref=backref('files'), cascade="all, delete", single_parent=True)
    
    def __init__(self, name, full_name, size, modified_on, volume_id, parent_directory_id):
        self.name = name
        self.full_name = full_name
        self.size = size
        self.modified_on = modified_on
        self.volume_id = volume_id
        self.parent_directory_id = parent_directory_id
        
    def __repr__(self):
        return "<Entities.VolumeFile('%s','%s','%s','%s','%s')>" % \
            (self.file_id, self.name, self.full_name, self.size, self.volume_id)
            