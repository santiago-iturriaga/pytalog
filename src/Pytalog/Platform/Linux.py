'''
Created on Jun 18, 2009

@author: santiago
'''

import pymediafinder
from Pytalog.Platform import VolumeInformation

def get_drives():
    '''
    Retorna una lista con todos las unidades de almacenamiento disponibles junto con su espacio disponible.
    '''
    raw_drives = pymediafinder.find()
    drives = []
    
    for raw_drive in raw_drives:
        (dev_name, mount_path, format_type, label) = raw_drive
        
        drive = VolumeInformation()
        drive.dev_name = dev_name
        drive.mount_path = mount_path
        drive.format_type = format_type
        drive.label = label
        
        drives.append(drive)
        
    return drives
