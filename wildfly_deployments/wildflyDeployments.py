import os
from datetime import date
from base.herramienta import Herramienta


class WildflyDeployments(Herramienta):
    def getHoy(self, format):
        #return date.today().strftime(str(format))
        return date.today().strftime("%Y%m%d")
    
    @classmethod
    def nombre_plugin(cls):
        return 'WildflyDeployments'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Wildfly Deployments'
    
    def run(self):
        print(self.contexto['wildfly_deployments'])
        comando = f'explorer /n,"{self.contexto['wildfly_deployments']}"'
        print(comando)
        os.system(comando)
        
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            self.contexto['barraEstado'].setText(self.contexto['wildfly_deployments'])
