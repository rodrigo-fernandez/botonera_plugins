import os
from datetime import date
from PySide6.QtWidgets import QDateEdit, QLineEdit, QDialog, QComboBox, QLabel
from PySide6.QtGui import QIcon
from base.herramienta import Herramienta, BotoneraPopUp, Popup

class NombreTag(Herramienta):
    def getHoy(self):
        return date.today().strftime("%Y%m%d")

    def versionPomToTagVersionPom(self, versionPom):
        return versionPom.replace('.', '-')
    
    def obtenerTag(self, nombre_proyecto, fecha_creacion_tag, version_pom, nro_release=None):
        sufijo_tag = f'V{nro_release}_{fecha_creacion_tag}_{version_pom}' if nro_release else f'{fecha_creacion_tag}_{version_pom}'
        return f'TAG_{nombre_proyecto.upper()}_{sufijo_tag}'
     
    def generarTag(self):
        aplicacion = self.nombre_proyecto_cb.currentText()
        #hoy = self.getHoy()
        hoy = self.fecha.date().toPython().strftime("%Y%m%d")
        hoy = hoy if hoy and len(hoy) != 0 else self.getHoy()

        pom = self.version_pom.text()
        release = self.release_label.text()
        return self.obtenerTag(aplicacion, hoy, self.versionPomToTagVersionPom(pom), release)
    
    @classmethod
    def nombre_plugin(cls):
        return 'NombreTag'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Tag'
    
    def getIcono(self):
        icono = QIcon(os.path.dirname(__file__) + "/../../config/iconos/tag.svg")
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
        self.release_label = QLineEdit()
        contenido.append(self.release_label)

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
            tag = self.generarTag()
            
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText(tag)
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error generar tag")
        finally:
            self.dialogo.close()
    
    def cancelar(self):
        self.dialogo.close()
    
    def run(self):
        self.dialogo = self.get_dialogo()
        self.dialogo.open()
