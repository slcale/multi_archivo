#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'scale'
__name__ == 'FunctionsDef'

import sys,  subprocess, os, errno, shutil, re
import ClassTools as CT
import logging

# Establezco un objeto logger y su nombre
logger = logging.getLogger(__name__)


def check_path(spath, is_dir=False):
    '''Función que evalúa si la ruta indicada existe y tiene permiso de escritura, sino la crea. Devuelve True o False

    Argumentos:
        spath -> Es el archivo con la ruta a evaluar
        is_dir -> Por defecto False si la ruta a evaluar es de un archivo.
            Si la ruta es un directorio lleva el valor True.
    Ej.: path_exist('ruta/a/evaluar/archivo.txt')
        path_exist('ruta/de/directorios', is_dir=True)
    '''
    try:
        #os.path.exists(ruta_destino) and os.access(ruta_destino, os.W_OK)
        # Si es la ruta de un archivo le saco la parte del archivo.
        if not is_dir:
            spath = os.path.dirname(spath)
        #print "Try - spath: %s" % (spath)
        # os.makedirs(path[, mode]). Default permission mode 0777
        os.makedirs(spath)
        mkout = True
    except OSError, e:
        mkout = False
        if e.errno == errno.EEXIST:
            logger.debug("Ya existe el directorio: %s" % spath)
            # Verifico que tenga permiso de escritura
            if os.access(spath, os.W_OK):
                mkout = True
            else:
                logger.error("El directorio: %s no tiene permiso de escritura" % spath)
        elif e.errno == errno.EACCES:
            logger.error("No tiene permisos suficientes para crear o acceder al archivo o directorio: %s" % spath)
        else:
            logger.error("Error al crear o acceder al archivo o directorio - %s - %s" % (e.errno, os.strerror(e.errno)))
    return mkout


def pdfatexto(arch_sel):
    """Función que convierte el pdf a texto raw

        Arg:
            arch_sel: Ruta y nombre del archivo pfd a convertir a texto
    """

    # Inicializo el objeto que acumula los mensajes en una tupla.
    msg = CT.msg()

    # Nombre del archivo pdf original a evaluar
    file_orig = os.path.basename(arch_sel)
    # Nombre de la ruta original
    ruta_orig = os.path.dirname(arch_sel) + '/'
    # Nombre del archivo convertido a modo texto
    filename = os.path.splitext(file_orig)[0] + ".txt"

    logger.info("-- Convierto archivo pdf a texto")
    logger.info("Archivo original: %s" % arch_sel)
    logger.info("Archivo original Tipo: %s" % type(arch_sel))
    logger.debug("Archivo modo texto: %s" % filename)

    # Si no existe el archivo indicado
    if not os.path.isfile(arch_sel):
        msg.error("No existe el archivo: %s" % file_orig)
        msg.print_tMsg()
        sys.exit()
    # Si no hay un archivo pdf ya convertido con el mismo nombre en el destino => Convierto el archivo indicado
    elif not os.path.isfile(ruta_orig + filename):
        # subprocess.call(["df","-h","/home"])
        subprocess.call(["pdftotext", "-f", "1", "-l", "1", "-raw", arch_sel, str(ruta_orig + filename)])
        msg.info("Archivo: %s convertido a texto" % file_orig)
    # Si llegó acá es porque ya existe un archivo convertido con el mismo nombre.
    else:
        msg.warning("El archivo: %s ya tiene un archivo convertido a texto con el mismo nombre" % file_orig)

    msg.print_tMsg()
    return  msg.get_tMsg()


# Función que analiza los patrones
def arch_magic(general_dic, pattern_dic, arch_sel):
    """Función que analiza un archivo pdf y lo compara con un diccionario de patrones

        data_dic: diccionario con la información de los patrones, nombre del archivo de salida,etc.
        ruta_orig: ruta desde donde analizo los archivos.
        file_original: nombre del archivo original a analizar
    """

    # Inicializo el objeto que acumula los mensajes en una tupla.
    msg = CT.msg()

    # Nombre del archivo pdf original a evaluar. Lo codifico en utf-8 para no tener problemas
    file_orig = os.path.basename(arch_sel)
    # Nombre de la ruta original. Lo codifico en utf-8 para no tener problemas
    ruta_orig = os.path.dirname(arch_sel) + '/'
    # Nombre del archivo convertido a modo texto
    filename = os.path.splitext(file_orig)[0] + ".txt"

    msg.info("-- Archivo original: %s --\nRuta original: %s" % (file_orig, ruta_orig))
    logger.info("-- Archivo original: %s -- Ruta original: %s" % (file_orig, ruta_orig))

    logger.debug("Archivo modo texto: %s" % filename)

    if not os.path.isfile(ruta_orig + file_orig):
        logger.debug("No existe el archivo: %s" % file_orig)
        sys.exit()

    # Si el pdf no está convertido a texto lo convierto
    msg.info(pdfatexto(arch_sel))

    # Abro el archivo de texto en modo lectura y cargo el contenido del archivo de texto a una variable
    with open(ruta_orig + filename, "r") as dataFile:
        fullData = dataFile.read()
        # fullData = dataFile.read().splitlines()

    logger.debug("-- Acá comienza el bucle --")
    comp_ok = False
    file_sal = ''   # Variable con el nombre del archivo de salida
    subdir_destino = '' # Variable con el nombre del subdirectorio de salida (Para el caso de opción group_all).
    # Ordeno y recorro el diccionario de patrones.
    for item_conf in sorted(pattern_dic):
        logger.debug('-- Analizando el patrón ...%s' % item_conf)

        # Defino ruta destino para guardar el archivo
        # Si existe una ruta especial uso esa, sino uso ruta general definida al principio del archivo de configuración.
        # Python raises a KeyError whenever a dict() object is requested (using the format a = adict[key])
        # and the key is not in the dictionary. If you don't want to have an exception but would rather a default value
        #  used instead, you can use the get() method:
        ruta_default_dest = general_dic["ruta_destino"]
        ruta_destino = pattern_dic[item_conf].get('ruta_destino', ruta_default_dest)

        # Recupero las opciones específicas del patrón, si no están definidas me quedo con las generales.
        pattern_opt_default = general_dic['pattern_opt']
        pattern_opt = pattern_dic[item_conf].get('pattern_opt', pattern_opt_default)
        copia_destino_default = pattern_opt_default.get('copia_destino')
        copia_destino = pattern_opt.get('copia_destino', copia_destino_default)

        # Patrón a utilizar "pattern", variable con el resultado de la comparación "comp"
        logger.debug(type(pattern_dic[item_conf]['pattern']))
        pattern = r'%s' % pattern_dic[item_conf]['pattern']
        logger.debug('pattern: %s' % type(pattern))
        logger.debug("pattern: %s" % pattern)
        comp = re.search(pattern, fullData, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)
        if comp:
            logger.info("Coincidencia con el patrón analizado (%s)" % item_conf)
            msg.info("Coincidencia con el patrón analizado (%s)" % item_conf)
            logger.debug("Cantidad de Grupos: %s" % len(comp.groups()))
            # Formateo del nombre del archivo de salida. Convierto la cadena file_salida separada por comas en la tupla ftxt_sal.
            ftxt_sal = tuple(pattern_dic[item_conf]['file_salida'].split(','))
            # Armo de a pedazos el nombre del archivo de salida.
            for kk in ftxt_sal:
                # Si es un entero el nombre corresponde al grupo regex, si al string definido en el archivo conf.
                try:
                    kk = int(kk)
                    vg = comp.group(kk)
                    #print 'Es numerico -> Grupo, Valor:', kk, vg
                except ValueError:
                    vg = kk
                    #print 'Es una Cadena -> Valor:', vg
                file_sal += vg
            file_sal += '.pdf'
            logger.info('Nombre nuevo archivo: %s' % file_sal)
            msg.info('Nombre nuevo archivo: %s' % file_sal)

            # Si está definida group_all tengo que meter el archivo y los directorios adyacentes todos juntos en el
            # destino agrupandolos en un subdirectorio.
            group_all_default = ''
            group_all = pattern_dic[item_conf].get('group_all', group_all_default)
            if (group_all != '' and copia_destino):
                logger.info('Se agrupa a subdirectorio')
                msg.info('Se agrupa a subdirectorio')
                # Formateo del nombre del subdirectorio de destino. Convierto la cadena group_all separada por comas
                # en la tupla subdirtxt_dest.
                subdirtxt_dest = tuple(group_all.split(','))
                logger.debug('Tipo para subdirtxt_dest: %s - %s' % (type(subdirtxt_dest), subdirtxt_dest))
                # Armo de a pedazos el nombre del subdirectorio destino.
                for dkey in subdirtxt_dest:
                    # Si es un entero el nombre corresponde al grupo regex, sino al string definido en el archivo conf.
                    try:
                        dkey = int(dkey)
                        vdg = comp.group(dkey)
                    except ValueError:
                        vdg = dkey

                    subdir_destino += vdg
                subdir_destino += '/'

                # Verifico que el subdirectorio no exista en el destino
                logger.info('Creando el subdirectorio en el destino.')
                nueva_ruta_destino = ruta_destino + subdir_destino
                msg.info(' - Ruta destino: %s' % nueva_ruta_destino)
                logger.info(' - Ruta destino: %s' % nueva_ruta_destino)
                if not os.path.exists(nueva_ruta_destino):
                    # Verifico que el destino exista y tenga permiso de escritura
                    if copia_destino and check_path(ruta_destino,is_dir=True):
                        os.makedirs(nueva_ruta_destino) # Creo el subdirectorio

                        logger.debug('Copio el archivo y los directorios adyacentes al subdirectorio destino.')

                        # Copio el archivo pdf
                        shutil.copy2(ruta_orig + file_orig, nueva_ruta_destino + file_sal)
                        msg.info('\tSe copió el archivo')
                        logger.info('\tSe copió el archivo')

                        # Copio los directorios adyacentes al sudirectorio destino
                        subdir_ady = os.walk(ruta_orig).next()[1]
                        for ix_subd in subdir_ady:
                            shutil.copytree(ruta_orig + ix_subd, nueva_ruta_destino + ix_subd)
                            msg.info('\tDirectorios adyacentes copiados: %s' % ix_subd)
                            logger.info('\tDirectorios adyacentes copiados: %s' % ix_subd)
                    else:
                        msg.warning('Atención: El directorio destino no existe o no tengo permisos de escritura.')
                        group_all_ok = False
                else:
                    msg.warning('Atención: Ya existe un archivo/directorio con el mismo nombre en el destino.')
                    logger.info('Atención: Ya existe un archivo/directorio con el mismo nombre en el destino.')
                    group_all_ok = False

            else:
                # No hay agrupamiento a subdirectorio => Solo copio el archivo
                logger.info('No agrupo a subdirectorio')
                # Verifico que no exista el archivo
                if copia_destino and not os.path.isfile(ruta_destino + file_sal):
                    logger.debug('Entro al bucle de copia 1')
                    if os.access(ruta_destino, os.W_OK):
                        logger.debug('Entro al bucle de copia 2')
                        logger.debug('Copiando archivo %s %s %s %s' % (ruta_orig, file_orig, ruta_destino, file_sal))
                        # Creo una copia y renombro el archivo
                        shutil.copy2(ruta_orig + file_orig, ruta_destino + file_sal)
                        msg.info('Se copió el archivo - Directorio destino: %s' % ruta_destino)
                        logger.info('Se copió el archivo - Directorio destino: %s' % ruta_destino)

                else:
                    logger.debug('Entro al bucle de copia 3')
                    msg.warning('Atención: No copio el archivo porque ya existe un archivo/directorio con el mismo nombre en el destino.')
                    logger.info('Atención: No copio el archivo porque ya existe un archivo/directorio con el mismo nombre en el destino.')
                    #sys.exit('Atención: No muevo el archivo porque ya existe un archivo/directorio con el mismo nombre en el destino.')

            # Renombro el archivo en el lugar
            if not os.path.isfile(ruta_orig + file_sal):
                shutil.move(ruta_orig + file_orig, ruta_orig + file_sal)
                msg.info('Se renombró el archivo en el origen.')
                logger.info('Se renombro el archivo en el origen.')
            else:
                msg.warning('Atención: No renombro el archivo en el directorio de origen porque ya existe uno con el mismo nombre.')
                logger.info('Atención: No renombro el archivo en el directorio de origen porque ya existe uno con el mismo nombre.')

            # Asigno valor a la variable que indica que hubo coincidencia y salgo del bucle.
            comp_ok = True
            break   # A la primera coincidencia salgo del bucle.

        else:
            logger.debug("-- El patrón: %s no coincide con el archivo analizado --" % item_conf)

    # Si no coincide ningún patrón.
    if not comp_ok:
        msg.warning('-- Ningún Patrón conocido coincide con el archivo %s analizado --' % file_orig)
        logger.info('-- Ningún Patrón conocido coincide con el archivo %s analizado --' % file_orig)


    # Borro el archivo convertido a texto
    if os.path.isfile(ruta_orig + filename):
        os.remove(ruta_orig + filename)

    return msg.get_tMsg()



# Elimino la barra de directorio al final "/" o  esta "\" usando: .rstrip("/\\")
