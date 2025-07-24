import os
from base.herramienta import Herramienta

class LimpiarLogsWildfly(Herramienta):
    def limpiarArchivos(self):
        archivos = ["server.log", "boot.log"]
        directorio = self.contexto['directorio'] if 'directorio' in self.contexto else ""

        for archivo in archivos:
            rutaArchivo = os.path.join(directorio, archivo)

            a = open(rutaArchivo, 'w')
            a.close()

    @classmethod
    def nombre_plugin(cls):
        return 'LimpiarLogsWildfly'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Limpiar logs Wildfly'
    
    def run(self):
        try:
            self.limpiarArchivos()
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Logs limpios")
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error al limpiar logs")


class LimpiarLogsJboss(Herramienta):
    def limpiarArchivos(self):
        archivos = ["server.log", "boot.log"]
        directorio = self.contexto['directorio'] if 'directorio' in self.contexto else ""

        for archivo in archivos:
            rutaArchivo = os.path.join(directorio, archivo)

            a = open(rutaArchivo, 'w')
            a.close()

    @classmethod
    def nombre_plugin(cls):
        return 'LimpiarLogsJboss'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Limpiar logs Jboss'
    
    def run(self):
        try:
            self.limpiarArchivos()
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Logs limpios")
        except:
            if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
                self.contexto['barraEstado'].setText("Error al limpiar logs")
