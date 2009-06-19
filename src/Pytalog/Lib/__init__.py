__pytalog_manager = None

def get_manager():
    from Pytalog.Lib import __pytalog_manager
    from Pytalog.Lib.PytalogManager import PytalogManager
    
    if (not __pytalog_manager):
        __pytalog_manager = PytalogManager()
        
    return __pytalog_manager