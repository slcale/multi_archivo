=====================================
PASOS PARA INICIAR UN PROYECTO PYTHON
=====================================

Pre-requisitos
==============

Tener instalados:
    * pip (Herramienta para instalar y administrar paquetes Python)
    * virtualenv (Herramienta para crear entornos virtuales de Python)
    * git (Software de control de versiones)

1 - Crear entorno Virtual y activarlo
=====================================

Creo un entorno virtual llamado venv.

    Proyects_Folder$ virtualenv venv
    
    Proyects_Folder$ source venv/bin/activate
        ó
    Proyects_Folder$ . venv/bin/activate


2 - Instalar Pyscaffold
=======================

    (venv)Proyects_Folder$ pip install pyscaffold
    

3 - Crear el esqueleto del proyecto
===================================

Desde la carpeta donde alojamos los proyectos ejecutamos:

    (venv)Proyects_Folder$ putup mi_proyecto


4 - Instalo el paquete en el entorno e Inicializo el versionado
===============================================================

    (venv)Proyects_Folder$ cd mi_proyecto
        
    (venv)Proyects_Folder/mi_proyecto$ python setup.py install
    (venv)Proyects_Folder/mi_proyecto$ python setup.py develop     # Instalo el paquete en modo desarrollo
    
    (venv)Proyects_Folder/mi_proyecto$ git tag -a v0.1 -m "init release"
    
    
5 - Empujo el repositorio local al remoto
=========================================

    (venv)Proyects_Folder/mi_proyecto$ git remote add origin https://github.com/slcale/multi-archivo.git
    
    (venv)Proyects_Folder/mi_proyecto$ git push origin master


