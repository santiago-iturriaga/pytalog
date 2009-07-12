'''
Created on Jul 12, 2009

@author: santiago
'''

import sys
import gtk

def __GetBuilder():
    builder = gtk.Builder()
    builder.add_from_file("dialogs.glade")
     
    return builder

def ShowCurrentError(parent):
    (exc_type, exc_value, exc_traceback) = sys.exc_info()
    
    print "{0} :: {1}".format(exc_type, exc_value)
    print "    :: {0}".format(exc_traceback)

    builder = __GetBuilder()
    message = builder.get_object("messagedialog_error")
    message.set_transient_for(parent)
    message.set_markup("Error: {0}".format(exc_value))
    message.run()
    message.destroy()
     
def ShowError(parent, e):
    print "{0} :: {1}".format(type(e), e)
    
    builder = __GetBuilder()
    message = builder.get_object("messagedialog_error")
    message.set_transient_for(parent)
    message.set_markup("Error: {0}".format(e))
    message.run()
    message.destroy()
    
def ShowErrorMessage(parent, text):
    builder = __GetBuilder()
    message = builder.get_object("messagedialog_error")
    message.set_transient_for(parent)
    message.set_markup(text)
    message.run()
    message.destroy()
    
def ShowQuestionMessage(parent, primary_text, secondary_text):
    builder = __GetBuilder()
    message = builder.get_object("messagedialog_question")
    
    message.set_transient_for(parent)
    message.set_markup(primary_text)
    message.format_secondary_text(secondary_text)
    
    result = message.run()
    message.destroy()

    return result