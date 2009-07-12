#!/usr/bin/python
# coding=utf-8
'''
Created on Jun 9, 2009

@author: santiago
'''

import sys
import os
import gtk

current_path = os.getcwd()
sys.path.append(current_path)
os.chdir(os.path.join(current_path, "Pytalog"))

from Pytalog.Principal import Principal
from Pytalog import Humanize 

if __name__ == '__main__':   
    principal = Principal()
    principal.show()
    gtk.main()