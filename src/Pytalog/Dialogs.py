'''
Created on Jul 12, 2009

@author: santiago
'''

import sys
import gtk

def ShowCurrentError(parent):
    (exc_type, exc_value, exc_traceback) = sys.exc_info()
    
    print "{0} :: {1}".format(exc_type, exc_value)
    print "    :: {0}".format(exc_traceback)
    
    message = gtk.MessageDialog(parent, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, None)
    message.set_markup("Error: {0}".format(exc_value))
    message.run()
    message.destroy()
     
def ShowError(parent, e):
    print "{0} :: {1}".format(type(e), e)
    
    message = gtk.MessageDialog(parent, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, None)
    message.set_markup("Error: {0}".format(e))
    message.run()
    message.destroy()
    
def ShowErrorMessage(parent, text):
    builder = gtk.Builder()
    builder.add_from_file("dialogs.glade")
    
    message = builder.get_object("messagedialog_error")
    message.set_markup(text)
    message.run()
    message.destroy()
    