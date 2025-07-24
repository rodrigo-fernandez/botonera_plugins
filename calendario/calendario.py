from datetime import date
from PySide6.QtWidgets import QCalendarWidget, QDateEdit
from base.herramienta import Herramienta, BotoneraPopUp, Popup


class Calendario(Herramienta):    
    @classmethod
    def nombre_plugin(cls):
        return 'Calendario'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Calendario'
    
    def aceptar(self):
        print(type(self.campoFecha.date().toPython()))
        print(self.campoFecha.date().toPython().strftime("%Y%m%d"))
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            self.contexto['barraEstado'].setText("Cerro el calendario")
        self.dialogo.close()

    def cancelar(self):
        self.dialogo.close()

    def get_dialogo(self):
        contenido = []

        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        contenido.append(self.calendario)

        self.campoFecha = QDateEdit()
        self.campoFecha.setCalendarPopup(True)
        self.campoFecha.setDate(date.today())
        
        contenido.append(self.campoFecha)

        botonera = BotoneraPopUp(self.aceptar, self.cancelar)
        contenido.append(botonera)

        return Popup(self.etiqueta_plugin(), contenido)

    def run(self):
        self.dialogo = self.get_dialogo()
        self.dialogo.open()
