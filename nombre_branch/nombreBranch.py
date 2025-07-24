from datetime import date
from base.herramienta import Herramienta

class GenerarNombreBranch(Herramienta):
    def getHoy(self, format):
        return date.today().strftime(format)
    
    def generarNombreBranch(self):
        prefijoBranch = self.contexto['prefijo'] if 'prefijo' in self.contexto else ""
        sufijoBranch = self.contexto['formato_fecha'] if 'formato_fecha' in self.contexto else "%Y%m%d"
        return f'{prefijoBranch}{self.getHoy(sufijoBranch)}'

    @classmethod
    def nombre_plugin(cls):
        return 'GenerarNombreBranch'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Generar Nombre Branch'
    
    def run(self):
        try:
            nombreBranch = self.generarNombreBranch()

            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText(nombreBranch)
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error al generar nombre branch")
        
