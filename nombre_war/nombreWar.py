import os
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QDialog, QDialogButtonBox, QComboBox, QLabel
from PySide6.QtGui import QIcon
from base.herramienta import Herramienta

class GenerarNombreWar(Herramienta):
        
    def generarNombreWar(self):
        aux = self.nombre_proyecto_cb.currentText().replace(".war", "")
        return f'{aux}-{self.version_pom.text()}.war'

    @classmethod
    def nombre_plugin(cls):
        return 'GenerarNombreWar'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Generar Nombre War'
    
    def aceptar(self):
        try:
            nombreWar = self.generarNombreWar()
            
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText(nombreWar)
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error al generar nombre del war")
        finally:
            self.dialogo.close()
    
    def cancelar(self):
        self.dialogo.close()

    def getIcono(self):
        icono = QIcon(os.path.dirname(__file__) + "/../../config/iconos/package.svg")
        return icono
    
    def get_dialogo(self):
        aplicaciones_label = QLabel('Aplicaciones')
        self.nombre_proyecto_cb = QComboBox()
        self.nombre_proyecto_cb.addItems([''] + self.contexto['aplicaciones'].split(','))
        
        version_pom_label = QLabel('Versión pom.xml')
        self.version_pom = QLineEdit()

        aceptar = QPushButton('Aceptar')
        aceptar.clicked.connect(self.aceptar)
        cancelar = QPushButton('Cancelar')
        cancelar.clicked.connect(self.cancelar)

        botonera = QDialogButtonBox()
        botonera.addButton(aceptar, QDialogButtonBox.AcceptRole)
        botonera.addButton(cancelar, QDialogButtonBox.RejectRole)

        layout = QVBoxLayout()
        layout.addWidget(aplicaciones_label)
        layout.addWidget(self.nombre_proyecto_cb)
        layout.addWidget(version_pom_label)
        layout.addWidget(self.version_pom)
        layout.addWidget(botonera)

        dialogo = QDialog()
        dialogo.setWindowTitle(self.etiqueta_plugin())

        dialogo.setLayout(layout)
        dialogo.setWindowIcon(self.getIcono())
        return dialogo

    def run(self):
        self.dialogo = self.get_dialogo()
        self.dialogo.open()
