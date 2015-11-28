#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'scale'
__name__ == 'GuiLayout'

# Use Tkinter for python 2, tkinter for python 3
#import Tkinter as tk
from Tkinter import *
import yaml
import logging


# Establezco un objeto logger y su nombre
logger = logging.getLogger(__name__)


# Páginas para implementar la GUI

import ClasesGui as CG
import ClassTools as CT

# Declaro la Ventana principal de la GUI
root = Tk()

result = CG.TkGui(root,default_side=LEFT)

mensaje = CT.msg()
mensaje.info('Es una información')
mensaje.error('Es un error')
mensaje.warning('Es una advertencia')
mensaje.getMsg()
result.msg_text(mensaje.getMsg())
#result.mostrar()


#msg = (('Un mensaje informativo','info'),('Otro mensaje informativo','info'),('Un mensaje de advertencia','warning'),
#       ('Este mensaje final es de error','error'))
#result.msg_text(msg)

result.mensaje('La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa y sigue sigue la cosa '
               'La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa '
               'La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa ')

result.mostrar()
