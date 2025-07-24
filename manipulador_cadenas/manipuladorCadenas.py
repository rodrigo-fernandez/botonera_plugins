from abc import ABC, abstractmethod
from PySide6.QtWidgets import QPlainTextEdit, QLabel, QComboBox, QHBoxLayout, QGroupBox
from base.herramienta import Herramienta, BotoneraPopUp, Popup, QPushButton


class Manipulador(ABC):
    @classmethod
    @abstractmethod
    def etiqueta(self):
        pass
    
    @classmethod
    @abstractmethod
    def manipular(self, entrada):
        pass

class AMayusculas(Manipulador):
    @classmethod
    def etiqueta(self):
        return "A mayusculas"
    
    @classmethod
    def manipular(self, entrada):
        return entrada.upper()
    
class AMinusculas(Manipulador):
    @classmethod
    def etiqueta(self):
        return "A minusculas"
    
    @classmethod
    def manipular(self, entrada):
        return entrada.lower()

class AClaseCamelCase(Manipulador):
    @classmethod
    def etiqueta(self):
        return "A Clase camelCase"
    
    @classmethod
    def manipular(self, entrada):
        return entrada.title().replace(" ", "")
    
class ACamelCase(AClaseCamelCase):
    @classmethod
    def etiqueta(self):
        return "A camelCase"
    
    @classmethod
    def manipular(self, entrada):
        rta = super().manipular(entrada)
        return rta[0].lower() + rta[1:]

class ASnakeCase(Manipulador):
    @classmethod
    def etiqueta(self):
        return "A Snake case"
    
    @classmethod
    def manipular(self, entrada):
        return "_".join(entrada.lower().split(" "))

class TagParaIssue(Manipulador):
    @classmethod
    def etiqueta(self):
        return "Tag Para Issue"
    
    @classmethod
    def manipular(self, entrada):
        partes = entrada.split('/')
        partes.reverse()
        tag = partes[0]
        return f"**[{tag}]({entrada})**"

class CadenaAListaSimple(Manipulador):
    @classmethod
    def etiqueta(self):
        return "Cadena A Lista Comilla simple"
    
    @classmethod
    def manipular(self, entrada):
        aux = entrada.replace('[', '').replace(']', '')
        partes = aux.split(', ')
        
        return ", ".join([f"'{parte}'" for parte in partes])

class CadenaAListaDoble(Manipulador):
    @classmethod
    def etiqueta(self):
        return "Cadena A Lista Comilla doble"
    
    @classmethod
    def manipular(self, entrada):
        aux = entrada.replace('[').replace(']')
        partes = aux.split(', ')
        
        return ", ".join([f'"{parte}"' for parte in partes])

class ContarCaracteres(Manipulador):
    @classmethod
    def etiqueta(self):
        return "Contar caracteres"
    
    @classmethod
    def manipular(self, entrada):
        return f"{len(entrada)}"

class CadenaPorComasAListadoVertical(Manipulador):
    @classmethod
    def etiqueta(self):
        return "Cadena separada por comas a lista vertical"
    
    @classmethod
    def manipular(self, entrada):
        partes = entrada.split(', ')
        return "\n".join([f'{parte}' for parte in partes])

class MultiplicarCadena(Manipulador):
    @classmethod
    def etiqueta(self):
        return "Multiplicar Cadena (cadena*cantidad)"
    
    @classmethod
    def manipular(self, entrada):
        partes = entrada.split('*')
        return (partes[0] * int(partes[1])) if len(partes) > 1 else ''

class CadenaAHtml(Manipulador):
    @classmethod
    def paresCaracteres(self):
        rta = []
        
        rta.append(('Á', '&#193;'))
        rta.append(('É', '&#201;'))
        rta.append(('Í', '&#205;'))
        rta.append(('Ó', '&#211;'))
        rta.append(('Ú', '&#218;'))
        rta.append(('Ñ', '&#209;'))
        rta.append(('á', '&#225;'))
        rta.append(('é', '&#233;'))
        rta.append(('í', '&#237;'))
        rta.append(('ó', '&#243;'))
        rta.append(('ú', '&#250;'))
        rta.append(('ñ', '&#241;'))
        
        return rta
    
    @classmethod
    def etiqueta(self):
        return "Cadena a Cadena html"
    
    @classmethod
    def manipular(self, entrada):
        convertido = entrada
        
        for par in self.paresCaracteres():
            convertido = convertido.replace(par[0], par[1])
        
        return convertido


################################################################################

class ManipuladorCadenas(Herramienta):
    def __init__(self, contexto):
        super().__init__(contexto)
        
        self.levantarAcciones()

    @classmethod
    def nombre_plugin(cls):
        return 'ManipuladorCadenas'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Manipulador de Cadenas'
    
    def levantarAcciones(self):
        self.acciones = {}

        clases = [AMayusculas, AMinusculas, AClaseCamelCase, ACamelCase, ASnakeCase, TagParaIssue, CadenaAListaSimple, CadenaAListaDoble, ContarCaracteres, CadenaPorComasAListadoVertical, MultiplicarCadena, CadenaAHtml]
        
        for unaClase in clases:
            a = unaClase()
            self.acciones[a.etiqueta()] = a
    
    def aceptar(self):
        rta = self.salida.toPlainText()
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            self.contexto['barraEstado'].setText(rta)
        self.dialogo.close()

    def cancelar(self):
        self.dialogo.close()

    def cambioEnCombo(self, text):
        rta = self.acciones[text].manipular(self.entrada.toPlainText())
        self.salida.setPlainText(rta)

    def reaccionar(self):
        self.cambioEnCombo(self.acciones_cb.currentText())
        
    def get_dialogo(self):
        contenido = []

        self.entrada = QPlainTextEdit()
        contenido.append(self.entrada)
        
        contenido.append(QLabel('Acciones'))
        
        hboxAcciones = QHBoxLayout()
        self.acciones_cb = QComboBox()
        self.acciones_cb.addItems([''] + list(self.acciones.keys()))
        self.acciones_cb.currentTextChanged.connect(self.cambioEnCombo)
        hboxAcciones.addWidget(self.acciones_cb)
        self.reaccionar_btn = QPushButton('Reaccionar')
        self.reaccionar_btn.clicked.connect(self.reaccionar)
        hboxAcciones.addWidget(self.reaccionar_btn)
        
        grupoAcciones = QGroupBox('Ambiente')
        grupoAcciones.setLayout(hboxAcciones)
        
        contenido.append(grupoAcciones)

        self.salida = QPlainTextEdit()
        contenido.append(self.salida)

        botonera = BotoneraPopUp(self.aceptar, self.cancelar)
        contenido.append(botonera)

        return Popup(self.etiqueta_plugin(), contenido)

    def run(self):
        self.dialogo = self.get_dialogo()
        self.dialogo.open()
