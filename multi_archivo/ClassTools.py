#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'scale'
__name__ == 'ClassTools'

import logging

# Establezco un objeto logger y su nombre
logger = logging.getLogger(__name__)


class msg():
    """Clase que implementa mensajes en una tupla.

    Métodos: info(mensaje), warning(mensaje), error(mensaje), get_tMsg, set_tMsg(mensaje,tipo)

    Ejemplo: obj.info(mensaje)
    """
    def __init__(self):
        # Inicializo la tupla de mensajes
        self.tmsg = ()

    def get_tMsg(self):
        """Devuelve la tupla de mensajes como tupla y la borra."""
        x = getattr(self,'tmsg')

        # Borro la tupla de mensajes.
        self.tmsg = ()
        return x

    def set_tMsg(self, message, mtype):
        """Seteo la tupla de mensajes"""
        # Cuando la tupla de mensajes está vacía
        if (len(self.tmsg) == 0):
            # Si el mensaje no es una tupla
            if (type(message) is not tuple):
                self.tmsg = ((message, mtype),)
                #logger.debug('len: %s' % len(self.tmsg))
            # Si el mensaje es una tupla
            else:
                self.tmsg = message
        # Cuando la tupla de mensajes no está vacía
        else:
            # Si el mensaje no es una tupla
            if (type(message) is not tuple):
                self.tmsg += ((message, mtype),)
                #logger.debug('len: %s' % len(self.tmsg))
            # Si el mensaje es una tupla la concateno a la tupla de mensajes
            else:
                self.tmsg += message

    def get_textMsg(self):
        """Devuelve los mensajes de la tupla de mensajes como un texto y borra la tupla"""
        ix = ''
        for imessage, itype in self.tmsg:
            ix += itype + ": " + imessage + '\n'
        # Borro la tupla de mensajes.
        self.tmsg = ()
        return ix

    def print_tMsg(self):
        """Imprime en la salida estándar los mensajes de la tupla de mensajes formateada renglón por renglón.

        Ej.: Info: Una Sarasa
            Warning: Es una advertencia
            Info: Otra sarasa
            Error: Es un error
        """
        for imessage, itype in self.tmsg:
            print "%s: %s" % (itype, imessage)

    def clear_tMsg(self):
        """Limpia la tupla de mensajes."""
        self.tmsg = ()

    def info(self, message):
        self.set_tMsg(message,'info')

    def warning(self, message):
        self.set_tMsg(message,'warning')

    def error(self, message):
        self.set_tMsg(message,'error')

"""
a = msg()
a.info("Es una info")
a.warning("Advertencia")
print (a.get_tMsg())
a.print_tMsg()
a.clear_tMsg()  #Limpia la tupla
a.error("Un error")
a.info("Otra info")
print (a.get_tMsg())
a.print_tMsg()
"""