from base.herramienta import Herramienta
from pyperclip import copy

class LimpiarEstado(Herramienta):
    def limpiarEstado(self):
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            self.contexto['barraEstado'].setText("")
    
    @classmethod
    def nombre_plugin(cls):
        return 'LimpiarEstado'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Limpiar Estado'
    
    def run(self):
        self.limpiarEstado()
