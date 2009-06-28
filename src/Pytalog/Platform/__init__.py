class VolumeInformation(object):
    def __init__(self):
        pass
    
    @property
    def dev_name(self):
        return self.__dev_name
    
    @dev_name.setter
    def dev_name(self, value):
        self.__dev_name = value
        
    @property
    def mount_path(self):
        return self.__mount_path
    
    @mount_path.setter
    def mount_path(self, value):
        self.__mount_path = value
        
    @property
    def format_type(self):
        return self.__format_type

    @format_type.setter
    def format_type(self, value):
        self.__format_type = value
        
    @property
    def label(self):
        return self.__label
    
    @label.setter
    def label(self, value):
        self.__label = value
