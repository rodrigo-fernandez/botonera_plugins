from base.herramienta import Herramienta
from pyperclip import copy

class CopiarAPortapapeles(Herramienta):
    def alPortapapeles(self):
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            copy(self.contexto['barraEstado'].text())
    
    @classmethod
    def nombre_plugin(cls):
        return 'CopiarAPortapapeles'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Copiar A Portapapeles'
    
    def run(self):
        self.alPortapapeles()
