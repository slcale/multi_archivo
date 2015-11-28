#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'scale'
__name__ == 'Test'

# Use Tkinter for python 2, tkinter for python 3
#import Tkinter as tk
from Tkinter import *
import yaml
import logging
import ClasesGui as CG

#root = Tk(className ="My first GUI") #add a root window named Myfirst GUI
#var = StringVar()
#winmsg = Message(root,textvariable=var)# used instead of label, when the text is long
#var.set("Hey!? How are you doing?")
#winmsg.pack()
#root.mainloop()


mainwin = Tk()

result = CG.TkGui(mainwin)
result.mensaje()
result.mostrar()

