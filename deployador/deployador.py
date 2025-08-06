# https://pythonassets.com/posts/download-file-with-progress-bar-pyqt-pyside/

import os
import shutil
import time
from abc import ABC, abstractmethod
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QDialog, QDialogButtonBox, QComboBox, QProgressBar, QLabel, QLineEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThread, Signal
from base.herramienta import Herramienta, BotoneraPopUp, Popup


# Hilo para realizar la tarea en segundo plano
class WorkerThread(QThread):
    finished = Signal()     # senial para indicar fin
    deployador = None
    
    def run(self):
        if self.deployador:
            self.deployador.deployar()
        self.finished.emit()

class ProgressDialog(QDialog):
    def __init__(self, deployador):
        super().__init__()
        self.deployador = deployador
        self.setWindowTitle("Deployando...")
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 115, 300, 25)
        self.progress_bar.setRange(0, 0) # el 0,0 es porque no se cuanto se tarda

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.progress_bar)
        
        # Iniciar hilo
        self.worker = WorkerThread()
        self.worker.deployador = self.deployador
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
    
    def on_finished(self):
        self.worker.quit()
        self.worker.wait()
        self.done(0)

    
class App(object):
    def __init__(self, nombre, ruta):
        self.__nombre = nombre
        self.__ruta = ruta
    
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre
        
    @property
    def ruta(self):
        return self.__ruta
    
    @ruta.setter
    def ruta(self, ruta):
        self._ruta = ruta
    
    def __repr__(self):
        return f'App[nombre: {self.nombre}, ruta: {self.ruta}]'


class Deployador(Herramienta):
    @classmethod
    def nombre_plugin(cls):
        return 'Deployador'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Deployador'
	
    def getIcono(self):
        icono = QIcon(os.path.dirname(__file__) + "/../../config/iconos/link_url.svg")
        return icono
    
    def cambioEnCombo(self, text):
        app = self.apps[text]
        self.ruta_target.setText(app.ruta)
        
    def get_dialogo(self):
        self.nombre_proyecto_cb = QComboBox()
        aux2 = list(self.apps.keys())
        aux2.sort()
        self.nombre_proyecto_cb.addItems([''] + aux2)
        self.nombre_proyecto_cb.currentTextChanged.connect(self.cambioEnCombo)
        
        ruta_target_label = QLabel('Ruta target')
        self.ruta_target = QLineEdit()
        
        aceptar = QPushButton('Aceptar')
        aceptar.clicked.connect(self.aceptar)
        cancelar = QPushButton('Cancelar')
        cancelar.clicked.connect(self.cancelar)
        
        botonera = QDialogButtonBox()
        botonera.addButton(aceptar, QDialogButtonBox.AcceptRole)
        botonera.addButton(cancelar, QDialogButtonBox.RejectRole)
        
        layout = QVBoxLayout()
        layout.addWidget(self.nombre_proyecto_cb)
        layout.addWidget(self.ruta_target)
        layout.addWidget(botonera)
        
        dialogo = QDialog()
        dialogo.setWindowTitle(self.etiqueta_plugin())

        dialogo.setLayout(layout)
        dialogo.setWindowIcon(self.getIcono())
        return dialogo
	
    def copiar_carpeta_war(self, app, ruta_nueva=None):
        directorio = self.contexto['wildfly_deployments'] if 'wildfly_deployments' in self.contexto else ""
        directorio_war = os.path.join(directorio, f'{app.nombre}.war')
        
        if os.path.exists(directorio_war):
            if os.path.isdir(directorio_war):
                shutil.rmtree(directorio_war)
            else:
                os.remove(directorio_war)
        
        destino = os.path.join(directorio, f'{app.nombre}.war')
        ruta_aux = ruta_nueva if ruta_nueva else app.ruta
        origen = os.path.join(f'{ruta_aux}', app.nombre)
        shutil.copytree(origen, destino)
    
    def a_dodeploy(self, app):
        directorio = self.contexto['wildfly_deployments'] if 'wildfly_deployments' in self.contexto else ""
        archivosWar = [f for f in os.listdir(directorio) if ".deployed" in f or ".failed" in f or ".undeployed" in f]
        
        for archivo in archivosWar:
            archivo_deploy = os.path.join(directorio, archivo)
            os.remove(archivo_deploy)
            
        open(os.path.join(directorio, f'{app.nombre}.war.dodeploy'), 'w').close()
        
    def deployar(self):
        try:
            aplicacion = self.nombre_proyecto_cb.currentText()
            self.copiar_carpeta_war(self.apps[aplicacion], self.ruta_target.text())
            self.a_dodeploy(self.apps[aplicacion])
            
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                    self.contexto['barraEstado'].setText("Deploy exitoso")
        except Exception as e:
            print(e)
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText(f"Error al deployar - {e}" )
            
    
    def aceptar(self):
        self.progressDialog = ProgressDialog(self)
        rta = self.progressDialog.exec()
        self.dialogo.close()
        
    def cancelar(self):
        self.dialogo.close()
    
    def set_aplicaciones(self):
        self.apps = {}
        
        apps_aux = self.contexto['aplicaciones'].split(',')
        
        aux = []
        for app in apps_aux:
            nombre, ruta = app.strip().split('|')
            self.apps[nombre.strip()] = App(nombre.strip(), ruta.strip())
            
    def run(self):
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            self.contexto['barraEstado'].setText("")
        
        self.set_aplicaciones()
        self.dialogo = self.get_dialogo()
        self.dialogo.open()
