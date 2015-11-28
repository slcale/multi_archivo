#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'scale'
__name__ == 'ClassDef'

import Tkinter, tkFileDialog
import tkMessageBox
import FunctionsDef as fd
import sys,  os.path
import logging
import ClassTools as CT

import ClasesGui as CG

# Establezco un objeto logger y su nombre
logger = logging.getLogger(__name__)
#logger = logging.getLogger('multi-archivo')


#log_format = "%(asctime)s - %(name)s - [%(levelname)s]: [Sarasa %(module)s -  - %(funcName)s] %(message)s"    # asctime
#log_datefmt = "%Y-%m-%d %H:%M:%S"
#logging.Formatter.__init__(fmt=log_format, datefmt=log_datefmt)
#logging.basicConfig(format=log_format)
#logging.getLogger().__format__(log_format)

class Log():
    """ There are five levels of logging (in ascending order): DEBUG, INFO, WARNING, ERROR and CRITICAL.
        By default, if you run this code multiple times, it will append to the log if it already exists.
    """
    def __init__(self, arch_log,level='info'):
        LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
        # add filemode="w" to overwrite overwrite the log
        logging.basicConfig(filename=arch_log, level=LEVELS[level], format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y %m %d - %H:%M:%S', filemode='w')

        # logging.basicConfig(level=logging.DEBUG,
        #            format='%(asctime)s %(levelname)-8s %(message)s',
        #            datefmt='%a, %d %b %Y %H:%M:%S',
        #            filename='/temp/myapp.log',
        #            filemode='w')

    def debug(self,msg):
        logging.debug(msg)

    def aviso(self,msg):
        logging.info(msg)

    def advertencia(self,msg):
        logging.warning(msg)


class MenuCommands():
    """Clase que agrupa todas los comandos o funciones del menú de la aplicación

    windows: es la ventana que contiene el menú.
    conf_file: es el archivo de configuración formato YAML que debe contener los diccionarios con los parámetros
        necesarios de la aplicación"""

    def __init__(self,window, conf_file):
        # Ventana principal
        self.window = window
        # Selecciono el diccionario general y el de los patrones en el archivo de configuración
        self.pattern_dic = conf_file["patterns"]
        self.general_dic = conf_file["general"]
        self.ruta_inicial = self.general_dic["ruta_inicial"]

        #Inicializo una tupla de mensajes
        self.__msg = CT.msg()

    def init_frame(self):
        """Este método inicializa el frame principal.

        Setea la variable self.main_frame con la referencia al frame principal y elimina todos los widgets que el frame
        contenga.
        """
        # Frame principal
        self.main_frame = self.window.nametowidget('f_main')

        # Elimino todos los widgets que contiene el frame principal
        for child in self.main_frame.winfo_children():
            child.destroy()

    def donothing(self):
        """Este método realmente no hace nada.

        No, en serio, no hace nada!"""
        #logger.info("Se llamó a la función que no hace nada - %s" % self.__class__)
        logger.info("Se llamó a la función que no hace nada")
        pass

    def aviso_sel(self):
        """Método que tira un aviso."""
        logging.info('Se llamó a una función que avisa que se seleccionó un elemanto del menú - Me seleccionaron !!')

        # Inicializo el Frame principal. Esto crea la variable main_frame y borra todos los widgets del frame principal.
        self.init_frame()

        tkMessageBox.showinfo("Información", "Se seleccionó un elemento del menú.")

        result = CG.TkGui(self.main_frame)
        result.mensaje('La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa '
                       'La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa '
                       'La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa La sarasa ')
        result.mostrar()

    def otro_aviso_sel(self):
        """Método que tira otro tipo de aviso."""
        #tkMessageBox.showinfo("Información", "Se seleccionó un elemento del menú.")
        logging.info('Se llamó a una función que avisa que se seleccionó un elemento del menú - Me seleccionaron !!')

        # Inicializo el Frame principal. Esto crea la variable main_frame y borra todos los widgets del frame principal.
        self.init_frame()

        result = CG.TkGui(self.main_frame)
        msg = (('Un mensaje informativo','info'),('Otro mensaje informativo','info'),('Un mensaje de advertencia','warning'),
               ('Este mensaje final es de error','error'))
        result.msg_text(msg)
        result.mostrar()

    def gpdfatexto(self):
        """Método GUI para convertir archivo pdf a texto RAW."""

        # Inicializo el Frame principal. Esto crea la variable main_frame y borra todos los widgets del frame principal.
        self.init_frame()

        # Abro una ventana independiente para el selector de archivos
        root = Tkinter.Tk()
        root.withdraw()

        filez = tkFileDialog.askopenfilenames(parent=root, initialdir=self.ruta_inicial, title='Elija uno o más archivos pdf', filetypes=[('archivos pdf', '*.pdf')])
        logger.debug('-- tipo filez: %s' % type(filez))
        logger.debug("filez: %s", filez)
        if len(filez) > 0:
            #ruta_orig = os.path.dirname(filez[0]) + '/'

            # Recorro los archivos seleccionados
            logger.debug('Recorro los archivos seleccionados')
            for a_sel in filez:
                # Voy cargando la tupla de mensajes a medida  que convierto los pdfs seleccionados a texto.
                # Codifico en utf-8 los archivos seleccionados por si tienen acentos. Uso: a_sel.encode('utf-8')
                self.__msg.info(fd.pdfatexto(a_sel.encode('utf-8')))

            # Muestro los mensajes en una ventana
            msg = self.__msg.get_textMsg()
            tkMessageBox.showinfo("Información", msg)
            logger.info(msg)
#            self.__msg.clear_tMsg() #Limpio la tupla de mensajes

        else:
            logger.info('-- No se seleccionó ningún archivo --')
            tkMessageBox.showinfo("Información", "No se seleccionó ningún archivo")

    def gdir_magic(self):
        """Método GUI para seleccionar los archivos pdf dentro de un directorio, compararlos con los patrones,
            renombrarlos y moverlos para archivar."""

        self.garch_magic('directory')
        logger.info('Se invocó a la función gdir_magic')

    def garch_magic(self,dialog_type='file'):
        """Método GUI para seleccionar archivos, compararlos con los patrones, renombrarlos y moverlos para archivar

        Args:
            Puede ser tipo 'file' (por defecto) ó 'directory'
        """

        # Inicializo el Frame principal. Esto crea la variable main_frame y borra todos los widgets del frame principal.
        self.init_frame()

        # Abro una ventana independiente para el selector de archivos
        root = Tkinter.Tk()
        root.withdraw()

        # Verifico que tipo de diálogo debo abrir.
        # (file -> Si voy a seleccionar archivos, directory -> si voy a seleccionar un directorio)
        if (dialog_type == 'file'):
            filez = tkFileDialog.askopenfilenames(parent=root, initialdir=self.ruta_inicial, title='Elija uno o más archivos pdf', filetypes=[('archivos pdf', '*.pdf')])
        elif (dialog_type == 'directory'):
            dirz = tkFileDialog.askdirectory(parent=root, initialdir=self.ruta_inicial, title='Elija un directorio', mustexist=True)
            filez = ()  # Defino la tupla vacía donde voy a meter los archivos pdf del directorio
            for ix_file in os.listdir(dirz):
                if ix_file.endswith(".pdf"):
                    # Armo la lista de archivos agregando uno por uno al final de la tupla filez
                    filez += (dirz + '/' + ix_file,)
        else:
            self.__msg.error('No se ha seleccionado un tipo de dialogo permitido (file ó directory)')
            logger.error(self.__msg.get_textMsg())
            tkMessageBox.showerror('Error',self.__msg.get_textMsg())
            sys.exit('Error: Salgo de la función')

        logger.debug('-- tipo filez: %s' % type(filez))
        logger.debug("filez: %s", filez)

        if len(filez) > 0:
            #ruta_orig = os.path.dirname(filez[0]) + '/'

            # Recorro los archivos seleccionados
            logger.debug('Recorro los archivos seleccionados')
            for a_sel in filez:
                logger.debug('Se seleccionó: %s' % a_sel.split())
                # Voy cargando la tupla de mensajes a medida  que proceso los pdfs seleccionados.
                # Codifico en utf-8 los archivos seleccionados por si tienen acentos. Uso: a_sel.encode('utf-8')
                self.__msg.info(fd.arch_magic(self.general_dic, self.pattern_dic, a_sel.encode('utf-8')))

            # Muestro los mensajes dentro de un widget de texto.
            result = CG.TkGui(self.main_frame)
            result.msg_text(self.__msg.get_tMsg())
            result.mostrar()

            logger.info(self.__msg.get_tMsg())

        else:
            logger.info('-- No se seleccionó ningún archivo --')
            tkMessageBox.showinfo("Información", "No se seleccionó ningún archivo")

#        #Limpio la tupla de mensajes
#        self.__msg.clear_tMsg()

    def quit(self):
        """Método que cierra el menú del programa."""
        logger.info('Se invocó el método que cierra el menú del programa')
        exit('Se invocó el método que cierra el menú del programa')

    def quit_frame(self, frame_name="f_Main"):
        # Lo logré, esto lo hice como prueba y hace desaparecer el toolbar
        self.window.nametowidget(frame_name).pack_forget()
