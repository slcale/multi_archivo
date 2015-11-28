#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'scale'
__name__ == 'ClasesGui'

# Use Tkinter for python 2, tkinter for python 3
#import Tkinter as tk
from Tkinter import *
#import ttk
#from ttk import Separator
import os.path
import logging


# Establezco un objeto logger y su nombre
logger = logging.getLogger(__name__)

# Clase para implementar la GUI
class MainWindow(Frame):
    """Clase que implementa la GUI"""

    def __init__(self, root_win, confdoc, com_obj, titulo, dimension='800x500'): #arch_conf, com_obj, titulo, dimension
        self.confdoc = confdoc
        #print 'conf_doc: %s' % self.confdoc['general']['app_icon']

        self.mw = root_win

        self.mc = com_obj
        self.mw.geometry(dimension)
        self.mw.title(titulo)

        # Cargo el ícono de la aplicación
        icon_file = self.confdoc['general']['app_icon']
        img = PhotoImage(file=icon_file)
        self.mw.tk.call('wm', 'iconphoto', self.mw._w, img)

    def crear_menu(self):
        # Selecciono el diccionario del menu
        menubar_dic = self.confdoc["menubar"]
        menugroups = menubar_dic["menugroups"]
        menuitems = menubar_dic["menuitems"]
        logger.debug('tipo menugroups: %s' % type(menugroups))

        menubar = Menu(self.mw)

        # Loop que recorre cada grupo del menú
        ix_gr = 0
        menugr = []
        for item_gr in menugroups:
            logger.debug('-- Inicio Loop de los grupos del menu --')
            logger.debug('ix_gr: %s' % ix_gr)
            logger.debug('item_gr: %s' % item_gr)
            menugr.append(Menu(menubar, tearoff=0))

            # Loop que recorre cada item de un grupo del menú
            ix_item = 0
            for ix_item in range(len(menuitems[menugroups[ix_gr]])):
                logger.debug('-- Inicio el Loop de los items --')
                logger.debug('ix_item: %s' % ix_item)
                logger.debug('Item: %s' % menuitems[menugroups[ix_gr]][ix_item])
                logger.debug('Item tipo: %s' % type(menuitems[menugroups[ix_gr]][ix_item]))

                opt = menuitems[menugroups[ix_gr]][ix_item].split(',')
                logger.debug('menugr: %s' % menugr[ix_gr])
                logger.debug('options: %s' % opt)
                logger.debug('option1: %s' % opt[0])
                logger.debug('option2: %s' % opt[1])
                logger.debug('option1 - tipo: %s' % type(opt[0]))
                logger.debug('option2: - tipo: %s' % type(opt[1]))

                menugr[ix_gr].add_command(label=opt[0].strip(), command=getattr(self.mc,opt[1].strip()))
                if (len(opt) > 2) and (opt[2].strip() == 'separator'):
                    menugr[ix_gr].add_separator()

                ix_item += 1

            menubar.add_cascade(label=menugroups[ix_gr], menu=menugr[ix_gr])
            ix_gr += 1

        self.mw.config(menu=menubar)

    def crear_toolbar(self):
        # Selecciono el diccionario del toolbar
        toolbar_dic = self.confdoc["toolbar"]
        tbargroups = toolbar_dic["tbargroups"]
        tbaritems = toolbar_dic["tbaritems"]
        logger.debug('tipo tbargroups: %s' % type(tbargroups))

        #tb = Frame(self.mw, bg="blue", height=64)
        #tb.pack(side=TOP, fill=X)

        # Loop que recorre cada grupo del toolbar
        ix_gr = 0
        tbargr = []
        for item_gr in tbargroups:
            logger.debug('-- Inicio Loop de los grupos del toolbar --')
            logger.debug('ix_gr: %s' % ix_gr)
            logger.debug('item_gr: %s' % item_gr)
            # Nombre del Frame que contiene el toolbar (Para poder referenciarlo luego si deseo cambiarlo o eliminarlo)
            item_gr_name = 'f_' + item_gr
            tbargr.append(Frame(self.mw, name = item_gr_name, bg="blue", height=64))
            tbargr[ix_gr].pack(side=TOP, fill=X)

            # Loop que recorre cada item de un grupo del menú
            ix_item = 0
            button = []
            for ix_item in range(len(tbaritems[tbargroups[ix_gr]])):
                logger.debug('-- Inicio el Loop de los items --')
                logger.debug('ix_item: %s' % ix_item)
                logger.debug('Item: %s' % tbaritems[tbargroups[ix_gr]][ix_item])
                logger.debug('Item tipo: %s' % type(tbaritems[tbargroups[ix_gr]][ix_item]))

                opt = tbaritems[tbargroups[ix_gr]][ix_item].split(',')
                logger.debug('tbargr: %s' % tbargr[ix_gr])
                logger.debug('options: %s' % opt)
                logger.debug('option1: %s' % opt[0])
                logger.debug('option2: %s' % opt[1])
                logger.debug('option1 - tipo: %s' % type(opt[0]))
                logger.debug('option2: - tipo: %s' % type(opt[1]))

                button.append(Button(tbargr[ix_gr], text="%s" % opt[0].strip(), command=getattr(self.mc,opt[1].strip())))
                button[ix_item].pack(side=LEFT)

                ix_item += 1
            ix_gr += 1

    def mostrar(self):

        # Creo el frame principal donde luego voy a poner los widgets
        main_frame = Frame(self.mw, name = 'f_main', bg="red")
        main_frame.pack(side=LEFT, fill=BOTH, expand=1)

        self.mw.mainloop()


class TkGui:
    def __init__(self,root_win, default_side=TOP):
        #self.auxwin = Tk(className ="My first GUI") #add a root window named Myfirst GUI
        self.auxwin = root_win
        self.def_side = default_side
        #foo = Label(root,text="Hello World") # add a label to root window

    def mensaje(self, msg, side=None):
        #msg
        var = StringVar()
        #winmsg = Message(auxwin,textvariable=var)   # used instead of label, when the text is long
        winmsg = Message(self.auxwin, textvariable=var, relief=RAISED)   # used instead of label, when the text is long
        #var.set("Hey!? How are you doing?")
        var.set(msg)
        winmsg.config(width=600, anchor=NW, justify=LEFT, relief=RAISED) # width=50, bg='lightgreen'font=('times', 24, 'italic')
        #winmsg.pack(side=RIGHT, fill=Y)

        #op1 if condition else op2
        val_side = self.def_side if (side == None) else side
        winmsg.pack(side=val_side)

    def msg_text(self, msg, tag='normal', side=None):
        '''Recibe una tupla con mensajes y los muestra formateados dentro de un widget de texto.
        El formato de la tupla es del tipo: (('mensaje_1', 'tag'), ('mensaje_2', 'tag'), etc ...)
        Los tags pueden ser: bold, normal, warning, error, info.
        Por ej.: (('Primer mensaje', 'info'), ('Segundo mensaje', 'warning'), ('Tercer mensaje', 'warning'))
       '''

        wintext = Text(self.auxwin, wrap=WORD, state=NORMAL, height=20, width=100)
        scroll = Scrollbar(self.auxwin, command=wintext.yview)
        scroll.pack(side=RIGHT, fill=Y)

        wintext.configure(yscrollcommand=scroll.set)
        wintext.tag_configure('bold', font=('Arial', 10, 'bold'))
        wintext.tag_configure('normal', font=('Arial', 10))
        wintext.tag_configure('warning', foreground='#FCEF03', font=('Arial', 10, 'bold'))
        wintext.tag_configure('error', foreground='#FC0303', font=('Verdana', 10, 'bold'))
        #wintext.tag_bind('follow', '<1>', lambda e, t=wintext: t.insert(END, "Not now, maybe later!"))

        for item in msg:
            #print 'item: ', item
            if (item[1] == 'info'):
                #print 'item[0]: ', item[0]
                #print 'item[1]: ', item[1]
                wintext.insert(END, item[0] + '\n', 'normal')
                #wintext.insert(END, item[0], 'normal')
        #        quote = """
        #        To be, or not to be that is the question:
        #        Whether 'tis Nobler in the mind to suffer
        #        The Slings and Arrows of outrageous Fortune,
        #        Or to take Arms against a Sea of troubles,
        #        """
            elif (item[1] == 'warning'):
                wintext.insert(END, item[0] + '\n', 'warning')

            elif (item[1] == 'error'):
                wintext.insert(END, item[0] + '\n', 'error')

        #wintext.insert(END, 'follow-up\n', 'follow')
        wintext.config(state=DISABLED)
        #wintext.pack(side=RIGHT, fill=Y)
        #wintext.pack()
        #op1 if condition else op2
        val_side = self.def_side if (side == None) else side
        wintext.pack(side=val_side)

    def mostrar(self):
        mainloop()


'''
from Tkinter import *
win = Tk()
button = Button( Frame( win, name = "myframe" ), name = "mybutton" )
win.nametowidget("myframe.mybutton")
<Tkinter.Button instance at 0x2550c68>

'''
#    def quitar(self, obj_tk):
        #obj_tk = Button(root, text="Delete me", command=lambda: b.pack_forget())
#b.pack()

#root.mainloop()

'''
#En desuso
class View(Tkinter.Frame):
    initial_dir = ''
    texto = ''
    t = ''

    def __init__(self,root,initial_dir):
        Tkinter.Frame.__init__(self,root)
        b = Tkinter.Button(self,text='Seleccionar Archivo',command=self.mi_funcion)
        self.t = Tkinter.Label(self,textvariable=self.texto)
        b.pack(side='top')
        self.t.pack(side='top')
        # self.initial_dir es la variable de la clase, la otra es de la función
        self.initial_dir = initial_dir

    def mi_funcion(self):
        #tkMessageBox.showinfo('Otra Cacona','Click')
        filez = tkFileDialog.askopenfilenames(parent=self,initialdir=self.initial_dir, title='Elija uno o más archivos pdf', filetypes=[('archivos pdf', '*.pdf')])
        arch_select = self.tk.splitlist(filez)
        if len(arch_select) > 0:
            ruta_orig = os.path.dirname(arch_select[0]) + '/'

            # Recorro los archivos seleccionados
            msg = ''
            for a_sel in arch_select:
                msg += arch_magic(general_dic,pattern_dic,ruta_orig,a_sel)

            #self.texto.insert(Tkinter.INSERT,msg)
            self.t = Tkinter.Label(self,text=msg, justify=Tkinter.LEFT, padx=10, wraplength=580)
            #self.texto = msg
            self.t.pack()
            #tkMessageBox.showinfo('Resultado',msg)
            #print "Archivos seleccionados", archivos_sel

            #return arch_select
        else:
            sys.exit('-- No se seleccionó ningún archivo --')


#En desuso
# Función que genera una ventana de diálogo para seleccionar uno o mas archivos pdfs.
def crea_gui(initial_dir):
    print 'initial_dir:',initial_dir
    #Diálogo para seleccionar los archivos a procesar
    root = Tkinter.Tk()
    root.geometry("600x500")
    view = View(root,initial_dir)
    view.pack(side='top',fill='both',expand=True)
    root.mainloop()
    #root.geometry("600x500")
    # define options for opening or saving a file
'''

'''
    def menu(self):
        menubar = Menu(self.mw)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.mw.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)
        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.mw.config(menu=menubar)





        with open('./comunes/multi-archivo.conf', 'r') as fconfig:
            confdoc = yaml.load(fconfig)
        # Selecciono el diccionario del menu
        menu_dic = confdoc["menubar"]
        menugroups_dic = menu_dic["menugroups"]

        for mitem in menugroups_dic:
            print mitem
            for sitem in menugroups_dic[mitem]:
                print '\t', sitem
                print '\t\t', menugroups_dic[mitem][sitem]
'''