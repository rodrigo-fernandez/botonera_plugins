# eliminar war de wildfly

from shutil import rmtree
import os
from base.herramienta import Herramienta


class LimpiarDeploy(Herramienta):
    def limpiar(self):
        directorio = self.contexto['directorio'] if 'directorio' in self.contexto else ""
        archivosWar = [f for f in os.listdir(directorio) if ".war" in f and "ROOT" not in f]
        
        for archivo in archivosWar:
            completo = os.path.join(directorio, archivo)

            if os.path.isdir(completo):
                rmtree(completo)
            else:
                os.remove(completo)
    
    @classmethod
    def nombre_plugin(cls):
        return 'LimpiarDeploy'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Limpiar war Jboss'
    
    def run(self):
        try:
            self.limpiar()
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Deploy limpio")
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error al limpiar deploy")
