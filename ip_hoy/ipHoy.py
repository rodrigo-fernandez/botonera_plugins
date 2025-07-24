import sys
import socket
from base.herramienta import Herramienta


class IpHoy(Herramienta):
    def ipHoy(self):
        return socket.gethostbyname(socket.gethostname())
    
    @classmethod
    def nombre_plugin(cls):
        return 'IpHoy'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'IP Hoy'
    
    def run(self):
        ip_hoy = self.ipHoy()
        
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            self.contexto['barraEstado'].setText(ip_hoy)
