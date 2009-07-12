#coding=utf-8

KILOBYTE = 1024
MEGABYTE = 1048576
GIGABYTE = 1073741824
TERABYTE = 1099511627776

def HumanizeSize(size):
    '''
    Dado un tamaño en bytes retorna ese mismo tamaño human-friendly.
    '''
    
    if size < KILOBYTE:
        return "{0} b".format(size)
    elif size < MEGABYTE:
        return "{0:.1f} kb".format(size/KILOBYTE)
    elif size < GIGABYTE:
        return "{0:.1f} mb".format(size/MEGABYTE)
    elif size < TERABYTE:
        return "{0:.1f} gb".format(size/GIGABYTE)
    else:
        return "{0:.1f} tb".format(size/TERABYTE)
    