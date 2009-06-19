'''
Created on Jun 18, 2009

@author: santiago
'''

def get_drives():
    '''
    Retorna una lista con todos las unidades de almacenamiento disponibles junto con su espacio disponible.
    '''
    import subprocess

    output = subprocess.Popen(['/bin/df', '-B 1024'], stdout=subprocess.PIPE).communicate()[0]
    lines = output.split('\n')
    
    for line in lines[1:]:
        if (line):
            fs, blocks_total, blocks_used, blocks_available, usage, mount = line.split()
        
            #return dict(total=blocks_total, used=blocks_used, available=blocks_available)
            print "fs:%s total:%s used:%s free:%s usage:%s mount:%s\n" % (fs, blocks_total, blocks_used, blocks_available, usage, mount)
