from base.herramienta import Herramienta
import os


class ADodeploy(Herramienta):
    def cambiarADodeploy(self):
        directorio = self.contexto['directorio'] if 'directorio' in self.contexto else ""
        archivosWar = [f for f in os.listdir(directorio) if ".deployed" in f or ".failed" in f or ".undeployed" in f]

        for archivo in archivosWar:
            completoOriginal = os.path.join(directorio, archivo)
            
            buscado = None
            if ".deployed" in archivo:
                buscado = "deployed"
            elif ".failed" in archivo:
                buscado = "failed"
            elif ".undeployed" in archivo:
                buscado = "undeployed"
                
            completoNuevo = os.path.join(directorio, archivo).replace(buscado, "dodeploy")
        
            os.rename(completoOriginal, completoNuevo)
    
    @classmethod
    def nombre_plugin(cls):
        return 'ADodeploy'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'A dodeploy'
    
    def run(self):
        try:
            self.cambiarADodeploy()
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Cambio realizado")
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error al cambiar a .dodeploy")
