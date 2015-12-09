=============
multi_archivo
=============


Aplicación para archivo y clasificación de documentos pdf.


Descripción
===========

Esta aplicación permite seleccionar archivos pdf y contrastarlos contra un archivo de
patrones (patterns.conf) expresados como expresiones regulares, a fin de encontrar una
coincidencia que permita clasificarlos y renombrarlos automáticamente según el criterio
preestablecido dicho archivo.


Instalación
===========

Para instalar la aplicación tenemos diversos métodos:


Instalación general:
--------------------

	Desde la carpeta "dist", descargar el archivo wheel (que tiene la extensión .whl).
	Por ej: multi_archivo-x.x.lo.que.sea.whl
	Y en una terminal ejecutamos:

		pip install archivo_wheel.whl

	Se recomienda crear un ambiente virtual python previamente a la instalación usando
	la aplicación virtualenv, activarlo para luego realizar la instalación.


Instalación en Ubuntu:
----------------------

	Se pueden descargar todos los archivo de la carpeta Ubuntu-dist y utilizar el script
	de instalación install-py.sh
	Dicho archivo crea un entorno virtual de python, insala la aplicación y crea un
	lanzador para Unity. Realizamos los siguientes pasos:

		* 1- Abrimos una terminal y lo hacemos ejecutable.
			chmod ug+x install-py.sh

		* 2- En la terminal ejecutamos:
			install-py.sh -i multi_archivo Ruta_de_archivos_de_instalación


Nota
====

Este proyecto se estructuró para su distribución utilizando el paquete PyScaffold 2.4.4.
Para más detalles sobre PyScaffold véase: http://pyscaffold.readthedocs.org/.
