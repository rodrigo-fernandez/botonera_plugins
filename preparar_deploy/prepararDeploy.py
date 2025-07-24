import os
from datetime import date
from PySide6.QtWidgets import QLineEdit, QComboBox, QLabel, QDateEdit
from PySide6.QtGui import QIcon
from base.herramienta import Herramienta, BotoneraPopUp, Popup


class PrepararDeploy(Herramienta):
    def getHoy(self):
        return date.today().strftime("%Y%m%d")
    
    def crearDirectorio(self):
        directorio = self.contexto['directorio'] if 'directorio' in self.contexto else ""
        aplicacion = self.nombre_proyecto_cb.currentText()
        nuevoDirectorio = self.fecha.date().toPython().strftime("%Y%m%d")
        nuevoDirectorio = nuevoDirectorio if nuevoDirectorio and len(nuevoDirectorio) != 0 else self.getHoy()
        
        directorioACrear = os.path.join(directorio, aplicacion, nuevoDirectorio)
        
        if not os.path.exists(directorioACrear):
            os.makedirs(directorioACrear)

        return directorioACrear

    def versionPomToTagVersionPom(self, versionPom):
        return versionPom.replace('.', '-')

    def obtenerTag(self, nombre_proyecto, fecha_creacion_tag, version_pom, nro_release=None):
        sufijo_tag = f'V{nro_release}_{fecha_creacion_tag}_{version_pom}' if nro_release else f'{fecha_creacion_tag}_{version_pom}'
        return f'TAG_{nombre_proyecto}_{sufijo_tag}'
    
    def generarTag(self):
        aplicacion = self.nombre_proyecto_cb.currentText()
        hoy = self.getHoy()
        pom = self.version_pom.text()
        release = self.release.text()
        return self.obtenerTag(aplicacion, hoy, self.versionPomToTagVersionPom(pom), release)

    def generarNombreWar(self, nombre_proyecto, version_pom):
        aux = nombre_proyecto.replace(".war", "")
        return f'{aux}-{version_pom}.war'

    def getContenido(self, tag):
        aplicacion = self.nombre_proyecto_cb.currentText()
        pom = self.version_pom.text()

        nombreWar = self.generarNombreWar(aplicacion, pom)

        contenido = [tag, '\n\n', nombreWar, '\n']
        return contenido

    def crearArchivoInfoDeploy(self, nuevoDirectorio):
        tag = self.generarTag()
        contenido = self.getContenido(tag)
        
        with open(os.path.join(nuevoDirectorio, f'{tag}.txt'), mode='w') as f:
            f.writelines(contenido)

    def crear(self):
        nuevoDirectorio = self.crearDirectorio()
        self.crearArchivoInfoDeploy(nuevoDirectorio)
        
        return nuevoDirectorio

    @classmethod
    def nombre_plugin(cls):
        return 'PrepararDeploy'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Preparar Deploy'
    
    def getIcono(self):
        icono = QIcon(os.path.dirname(__file__) + "/../../config/iconos/folder.svg")
        return icono
    
    def get_dialogo(self):
        contenido = []
        
        contenido.append(QLabel('Aplicaciones'))

        self.nombre_proyecto_cb = QComboBox()
        self.nombre_proyecto_cb.addItems([''] + self.contexto['aplicaciones'].split(','))
        contenido.append(self.nombre_proyecto_cb)

        contenido.append(QLabel('Versión pom.xml'))
        self.version_pom = QLineEdit()
        contenido.append(self.version_pom)

        contenido.append(QLabel('Release'))
        self.release = QLineEdit()
        contenido.append(self.release)

        contenido.append(QLabel('Fecha'))
        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(date.today())
        contenido.append(self.fecha)

        botonera = BotoneraPopUp(self.aceptar, self.cancelar)
        contenido.append(botonera)

        return Popup(self.etiqueta_plugin(), contenido, icono=self.getIcono())

    def aceptar(self):
        try:
            nuevoDirectorio = self.crear()
            
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText(nuevoDirectorio)
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error al preparar el deploy")
        finally:
            self.dialogo.close()
    
    def cancelar(self):
        self.dialogo.close()
    
    def run(self):
        self.dialogo = self.get_dialogo()
        self.dialogo.open()
