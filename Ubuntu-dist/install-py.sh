#!/bin/bash
#install-py.sh
#Script de instalación de proyectos python en Ubuntu
#autor: Santiago L. Calé
#version: 1.2
#fecha: 8/12/2015


#Ej.: -> ./install-py.sh -i nombre_proy /media/pendrive/dir_instalacion

#Funcion de Ayuda
ayuda()
{
  cat <<AYUDA

Uso:	install-py.sh OPCIONES NOMBRE_PROYECTO DIR_ARCHIVOS_INSTALACION -> Instalador de proyectos python en ubuntu.

	Ej.: install-py.sh -i nombre_proy "/media/usb/dir_archivos_instalacion"  ->  Instala dependencias, entorno virtual, 
									 	     el proyecto python y el lanzador de Unity.

Opciones:	-h	Ayuda del comando
		-i	Instala las dependencias, el entorno virtual, el proyecto python y el lanzador en Unity. 
			Se debe proporcionar el nombre del proyecto, y la ruta del directorio con los archivos de instalación,
			que debe contener: 1 archivo wheel (whl), 1 archivo .desktop, 1 archivo con el icono.

AYUDA
  exit 0
}


#Si no ingreso ningún parámetro muestro la ayuda
if [ ! $1 ]; then
	ayuda
fi


#Para pausar la ejecución del script
function f_pausa(){
	read -n1 -r -p "Press any key to continue..." key
	#The -n1 specifies that it only waits for a single character. The -r puts it into raw mode, which is necessary 
	#because otherwise, if you press something like backslash, it doesn't register until you hit the next key. 
	#The -p specifies the prompt, which must be quoted if it contains spaces. The key argument is only necessary 
	#if you want to know which key they pressed, in which case you can access it through $key.
}


#chequea e instala paquetes ó librerías.
f_check_paquete() {
	#Ayuda: check_paquete NOMBRES_PAQUETES	Ej: check_paquete paquete1 paquete2 paquete3
	# NOMBRES_PAQUETES: es una cadena con los nombres de uno o más paquetes separados por espacios.
	# -> Si el paquete está instalado => continua con el script. 
	# -> Si el paquete no está instalado => lo instala
	# -> Si el paquete no está instalado y no puede instalarlo (p.ej.: porque no lo encuentra en el repositorio) => da error y aborta ejecución del script. 

	#Para declarar un array:
	#declare -a array_name=(element1 element2 element3)
	#Si los elementos tiene espacios en blanco, como por ej. nombres de archivos:
	#declare -a array_name=('element1' 'element2' 'element3')
	#P. ej.:declare -a array_name=('El primer elemento' 'Segundo elemento' 'tercero')
	# $*	El conjunto de todos los parámetros en un solo argumento
	# $@	El conjunto de argumentos (un argumento por parámetro)

	declare -a array_paquete=($@) #Ojo no poner entre comillas al $@

	#Cantidad total de items seleccionados
	nitems=${#array_paquete[*]}
	echo "Número de paquetes/librerías a chequear:"$nitems

	#Loop que barre los items seleccionados uno a uno.
	nitem=0
	while [ $nitem -lt $nitems ]; do

		item="${array_paquete[$nitem]}"
		echo -e "\n*** CHEQUEANDO PAQUETE o LIBRERIA: ""$item"" ***"
		PKG_OK=$(dpkg-query -W --showformat='${Status}\n' "$item" |grep "install ok installed")
		echo "$PKG_OK"

		if [ "" == "$PKG_OK" ]; then
 			echo "No instalado. Instalando el paquete: ""$item"
			if sudo apt-get --force-yes --yes install "$item"; then
				echo "Paquete instalado correctamente"
			else
				echo "*****************************************************"
				echo "--- ERROR al instalar paquete: ""$item"" ---"
				echo "--- SE ABORTO LA INSTALACION ---"
				echo "*****************************************************"
				exit
			fi
		fi

		nitem=$[$nitem+1]
	done

	echo -e "\n*** Continuamos con el script ... ***"
}


# Función que pone el lanzador en la carpeta ~/.local/applications para usar en Unity.
f_poner_user() {
	echo "--- Vamos a copiar el lanzador desde su directorio a "~/.local/share/applications/". ---"
	#Ruta completa y nombre del script a instalar.
	RUTAEXE="$1"
	#echo "RUTAEXE: ""$1"  
	if [ ! -e "$RUTAEXE" ]; then                                  # Si el archivo no existe...
	 echo "--- ERROR: El archivo no existe.  Abortado. ---"
	 exit                                                # ...salimos del script.
	fi
	NOMBRE_LANZADOR=`basename "$RUTAEXE"`
	cp -f "$RUTAEXE" ~/.local/share/applications/"$NOMBRE_LANZADOR"
	chown $USER:$USER ~/.local/share/applications/"$NOMBRE_LANZADOR"      	# Hacemos que el lanzador pertenezca al usuario
	chmod ug+x ~/.local/share/applications/"$NOMBRE_LANZADOR"	# Hago al lanzador ejecutable.
	sed -i "s/<HOME>/\/home\/$USER/" ~/.local/share/applications/"$NOMBRE_LANZADOR"   # Reemplazo TAG <HOME> por directorio home.
	#echo "sed -i ""s/<HOME>/$HOME/" ~/.local/share/applications/"$NOMBRE_LANZADOR"
	echo "--- Lanzador colocado en "~/.local/share/applications/". Arrástrelo desde alli hasta la barra de Unity ---"
}


# Función que instala el paquete python en Ubuntu a partir de un archivo wheel.
instalo_wheel() {
	echo "*** COMIENZO DE VALIDACIÓN ***"
	echo "*** Valido la cantidad de parámetros ingresados. ***"
	if [ $# -lt 3 ]; then
		echo "Error: Cantidad insuficiente de Parámetros."
		exit
	fi
	if [ $# -gt 3 ]; then
		echo "Error: Cantidad de Parámetros excedida."
		exit
	fi
	
	echo "*** Verifico e instalo las dependencias de paquetes ***"
	#Verifico e instalo las dependencias de paquetes: pip, python-virtualenv, python-tk (Tkinter) y wmctrl (control de ventanas)
	f_check_paquete python-pip python-virtualenv python-tk wmctrl

	echo "*** Creo el entorno virtual ***"
	name_proj="$1"	#Nombre del proyecto
	echo "name_proj: $name_proj"
	dir_inst=${2%/}	#Directorio de los instalables. Si tiene una barra / al final se la saqué.
	echo "dir_inst: $dir_inst"
	dest_inst=~/.config/$name_proj	#Directorio destino de instalación
	#dest_inst="/usr/local/$name_proj"	#Directorio destino de instalación
	echo "dest_inst: $dest_inst"
	mkdir -p "$dest_inst"
	virtualenv "$dest_inst/venv"

	echo "*** Activo el entorno virtual ***"
	if source "$dest_inst/venv/bin/activate"; then
		echo "*** Instalo el paquete python en el destino: \"$dest_inst\" ***"
		#para fabricar el paquete wheel se hace: python setup.py bdist_wheel
		#para instalarlo: pip install archivo.whl
		arch_wheel=`ls "$dir_inst/"*.whl`
		echo "*** Archivo Wheel: $arch_wheel ***"
		if [ "$3" == "install" ]; then
			pip install "$arch_wheel"
		elif [ "$tipo_inst" == "upgrade" ]; then
			pip install --upgrade "$arch_wheel"
			#pip install --upgrade multi_archivo-0.1+g6bab378.dirty-py2.py3-none-any.whl
		fi
	fi

	echo "*** Copio el icono e instalo el lanzador ***"
	sudo cp -f "$dir_inst/"*.png "/usr/share/app-install/icons/" # cp del icono a: /usr/share/app-install/icons/
	arch_desktop=`ls "$dir_inst/"*.desktop`
	echo "*** Archivo desktop: $arch_desktop ***"
	f_poner_user "$arch_desktop"

	#Abro la ventana donde están los lanzadores .desktop instalados para poder arrastrarlos a la barra de Unity.	
	xdg-open ~/.local/share/applications
	#Le doy el foco a la ventana.
	wmctrl -R applications
	echo "-----------------------------------------------------------------------------------------------"
	echo "--- Lanzador colocado en '/usr/share/applications/'. Arrástrelo hasta la barra de Unity ---"
	echo "-----------------------------------------------------------------------------------------------"
	echo " ****** FIN DE LA INSTALACIÓN ******"
}


#Subrrutina de Selección de opciones de linea de comando
while [ -n "$1" ]; do
case $1 in
    -h) ayuda;shift 1;; # llamamos a la función ayuda
    -i) i=1;shift 1;; # instala el archivo wheel dado
    -u) u=1;shift 1;; # actualiza el archivo wheel dado
    --) shift;break;; # end of options
    -*) echo "error: no existe la opción $1. -h para ayuda";exit 1;;
    *)  break;;
esac
done


# Invoco la funcion según las opciones del script.
if [ $i ]; then
	instalo_wheel "$@" "install"
	exit
fi
if [ $u ]; then
	instalo_wheel "$@" "upgrade"
	exit
fi
