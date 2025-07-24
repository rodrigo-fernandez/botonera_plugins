import os
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox, QComboBox, QCheckBox, QRadioButton, QGroupBox
from PySide6.QtGui import QIcon
from base.herramienta import Herramienta

class GenerarUrlApp(Herramienta):
    
    def esDeWildfly(self, aplicacion):
        return aplicacion in self.contexto['aplicaciones_wildfly'].split(',')
    
    def esDeJboss(self, aplicacion):
        return aplicacion in self.contexto['aplicaciones_jboss'].split(',')
    
    def cabezaClave(self):
        aplicacion = self.nombre_proyecto_cb.currentText()

        if self.esDeWildfly(aplicacion):
            return "wildfly"
        
        if self.esDeJboss(aplicacion):
            return "jboss"

        return ""

    def cuerpoClave(self):
        rta = ""

        if self.localRadio.isChecked():
            rta = "local"

        else:
            if self.desRadio.isChecked():
                rta = "des"

            elif self.intRadio.isChecked():
                rta = "int"

            elif self.preProdRadio.isChecked():
                rta = "preprod"

            elif self.prodRadio.isChecked():
                rta = "prod"
            
            if self.nodo1.isChecked():
                rta = f'{rta}_01'
            elif self.nodo2.isChecked():
                rta = f'{rta}_02'
            elif self.nodo3.isChecked():
                aplicacion = self.nombre_proyecto_cb.currentText()

                if self.esDeWildfly(aplicacion):
                    rta = f'{rta}_03'
        
        return rta
    
    def piesClave(self):
        return "acelerada" if self.acelerada_chk.isChecked() else "comun"
    
    def getPrefijo(self):
        clave = f"{self.cabezaClave()}_{self.cuerpoClave()}_{self.piesClave()}"
        
        return self.contexto[clave] if clave in self.contexto else ""

    def getUrl(self):
        aplicacion = self.nombre_proyecto_cb.currentText()
        prefijo = self.getPrefijo()
        return f"{prefijo}{aplicacion}"
    
    @classmethod
    def nombre_plugin(cls):
        return 'GenerarUrlApp'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Generar Url App'
    
    def getIcono(self):
        icono = QIcon(os.path.dirname(__file__) + "/../../config/iconos/link_url.svg")
        return icono
    
    def get_dialogo(self):
        self.nombre_proyecto_cb = QComboBox()
        aux = self.contexto['aplicaciones_wildfly'].split(',') + self.contexto['aplicaciones_jboss'].split(',')
        aux.sort()
        self.nombre_proyecto_cb.addItems([''] + aux)
        
        self.acelerada_chk = QCheckBox('Acelerada')
        
        hboxApp = QHBoxLayout()
        hboxApp.addWidget(self.nombre_proyecto_cb)
        hboxApp.addWidget(self.acelerada_chk)
        grupoApp = QGroupBox('Aplicación')
        grupoApp.setLayout(hboxApp)

        self.localRadio = QRadioButton('Local')
        self.localRadio.setChecked(True)
        self.desRadio = QRadioButton('Des')
        self.intRadio = QRadioButton('Int')
        self.preProdRadio = QRadioButton('PreProd')
        self.prodRadio = QRadioButton('Prod')

        hboxAmbiente = QHBoxLayout()
        hboxAmbiente.addWidget(self.localRadio)
        hboxAmbiente.addWidget(self.desRadio)
        hboxAmbiente.addWidget(self.intRadio)
        hboxAmbiente.addWidget(self.preProdRadio)
        hboxAmbiente.addWidget(self.prodRadio)

        grupoAmbiente = QGroupBox('Ambiente')
        grupoAmbiente.setLayout(hboxAmbiente)

        self.balanceada = QRadioButton('Balanceada')
        self.balanceada.setChecked(True)
        self.nodo1 = QRadioButton('Nodo 1')
        self.nodo2 = QRadioButton('Nodo 2')
        self.nodo3 = QRadioButton('Nodo 3')
                            
        hboxNodos = QHBoxLayout()
        hboxNodos.addWidget(self.balanceada)
        hboxNodos.addWidget(self.nodo1)
        hboxNodos.addWidget(self.nodo2)
        hboxNodos.addWidget(self.nodo3)
        grupoNodo = QGroupBox('Nodos')
        grupoNodo.setLayout(hboxNodos)

        aceptar = QPushButton('Aceptar')
        aceptar.clicked.connect(self.aceptar)
        cancelar = QPushButton('Cancelar')
        cancelar.clicked.connect(self.cancelar)

        botonera = QDialogButtonBox()
        botonera.addButton(aceptar, QDialogButtonBox.AcceptRole)
        botonera.addButton(cancelar, QDialogButtonBox.RejectRole)

        layout = QVBoxLayout()
        layout.addWidget(grupoApp)
        layout.addWidget(grupoAmbiente)
        layout.addWidget(grupoNodo)
        layout.addWidget(botonera)

        dialogo = QDialog()
        dialogo.setWindowTitle(self.etiqueta_plugin())

        dialogo.setLayout(layout)
        dialogo.setWindowIcon(self.getIcono())
        return dialogo

    def aceptar(self):
        try:
            url = self.getUrl()
            
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText(url)
            
            if 'firefox' in self.contexto and self.contexto['firefox']:
                comando = f'"{self.contexto['firefox']}" -private-window {url}'
                os.system(comando)
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
