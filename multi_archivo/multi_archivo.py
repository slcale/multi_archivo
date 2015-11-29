#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'scale'
__name__ = '__main__'   # Es lo mismo poner esto o directamente llamar __main__.py al archivo.

# sudo pip install pdfminer
import argparse, os.path, yaml
import logging
from Tkinter import *

# Establece la ruta del archivo y la añade al path (solucioné problemas de importación de mis módulos)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#print "PATH: %s" % sys.path

#import FunctionsDef as fd
import ClasesGui as CG
import ClassDef as CD

def main():
    """The main routine."""

    # Parametros iniciales: Directorio del usuario y Ruta archivo de configuración
    home = os.path.expanduser("~")

    # Directorio del paquete
    package_dir = os.path.dirname(os.path.abspath(__file__))
    # print 'package_dir: %s' % package_dir

    # Cambio al directorio del paquete
    os.chdir(package_dir)
    #print "current: %s" % os.getcwd()

    arch_conf = os.path.join(package_dir, 'comunes/multi_archivo.conf')
    #print 'arch_conf: %s' % arch_conf

    patt_conf = os.path.join(package_dir, 'comunes/patterns.conf')
    #print 'patt_conf: %s' % patt_conf

    # Establezco un objeto logger y su nombre
    #logger = logging.getLogger(__name__)
    logger = logging.getLogger('multi_archivo')
    # Establezco los parámetros de configuración del log
    log_level = logging.INFO  # Niveles del log: CRITICAL, ERROR, WARNING, INFO, DEBUG
    #log_filename = '/home/scale/.shell_scripts/log/' + os.path.splitext(__file__)[0] + ".log"   # Nombre del archivo de log
    modulename = os.path.basename(os.path.splitext(__file__)[0])    # Nombre del archivo / modulo. multi_archivo
    log_filename = home + '/.config/' + modulename + '/' + modulename + ".log"   # Nombre del archivo de log
    print "log_filename: %s" % log_filename
    log_filemode = "w"  # a -> agrega al final, w -> reemplaza (sobreescribe)
    log_format = "%(asctime)s - [%(levelname)s]: [%(module)s - %(funcName)s - %(lineno)d] %(message)s"
    # asctime  - %(lineno)d  - %(name)s
    log_datefmt = "%Y-%m-%d %H:%M:%S"
    # Aplico los parámetros anteriores
    logging.basicConfig(level=log_level, filename=log_filename, filemode=log_filemode,
                        format=log_format, datefmt=log_datefmt)

    # Interpreto los argumentos de entrada del script
    oarg = argparse.ArgumentParser(description='Procesamiento de archivos pdfs.')
    # oarg = argparse.ArgumentParser(description='Procesamiento de archivos pdfs.', add_help=False)
    # oarg.add_argument("-h", "--help", action="store_true", help="show this help message and exit")
    oarg.add_argument("-g", "--gui", help="Muestra la interfaz gráfica de usuario", action="store_true", default=True)
    oarg.add_argument("-c", "--convert", help="Convierte los archivos pdf seleccionados a texto raw", action="store_true")
    oarg.add_argument("-v", "--verbose", help="Muestra información para depuración", action="store_true")
    oarg.add_argument("-d", "--dir", help="Directorio de trabajo (Por defecto el directorio actual)")  # , default=os.getcwd())
    oarg.add_argument("-f", "--file", help="Nombre de uno más archivos a procesar", nargs='+')
    # oarg.add_argument('arg1', choices=['caca', 'pis', 'culo'])
    args = oarg.parse_args()

    # Enviamos al log los datos de los argumentos
    logger.info('Argumentos: %s', args)
    logger.info('args.dir: %s', args.dir)

    # Aquí procesamos lo que se tiene que hacer con cada argumento
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("-- La depuración está activada!!! - Cambiamos el nivel del log a: DEBUG --")

    if args.dir:
        ruta_orig = args.dir.rstrip('/') + '/'
        logger.debug("-- Se ingresó el directorio de trabajo: %s --" % ruta_orig)
    else:
        ruta_orig = os.getcwd() + '/'
        logger.debug("-- Se usará el directorio de trabajo actual: %s --" % ruta_orig)

    if args.gui:
        # python multi-archivo.py -v -g -d /home/scale/temp/test_multi/

        logger.debug('Se seteó la opción gui')

        # Cargo el archivo de configuración
        logger.debug('Cargo el archivo de Configuración')
        with open(arch_conf, 'r') as fconfig:
            confdoc = yaml.load(fconfig)

        # Cargo el archivo de patrones
        logger.debug('Cargo el archivo de patrones')
        with open(patt_conf, 'r') as pconfig:
            pattdoc = yaml.load(pconfig)

        # Declaro la Ventana principal de la GUI
        root = Tk()

        # Creo el objeto que contiene las funciones o comandos que ejecutará el menú
        menucom = CD.MenuCommands(root, pattdoc)

        # Creo el objeto que implementa la clase del menú
        mainwin = CG.MainWindow(root,confdoc, menucom, 'Multi-archivo')
        mainwin.crear_menu()
        toolbar = mainwin.crear_toolbar()
        logger.debug('Muestro la interfaz gráfica')
        mainwin.mostrar()

    if args.convert:
        logger.info("-- Convierto los pdfs seleccionados a texto raw --")
        # archivos_sel = crea_gui(ruta_orig)
        # ruta_orig = os.path.dirname(archivos_sel[0]) + '/'
        # Recorro los archivos seleccionados
        # for a_sel in archivos_sel:
        #    fd.pdfatexto(a_sel)

    if args.file:
        logger.info("Archivo a procesar es: %s" % args.file)


if __name__ == "__main__":
    main()
