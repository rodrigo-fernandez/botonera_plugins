# botonera_plugins

Pluings para la aplicación botonera.

<https://github.com/rodrigo-fernandez/botonera>

## Pluings

* **wildfly_deployments**
	
	*Abre el explorador de windows en la carpeta de deploy de wildfly.*
	
* **a_dodeploy**
	
	*Cambia **proyecto**.war.<deployed|fail> a **proyecto**.war.dodeploy*
	
* **calendario**
	
	*Prueba uso de calendario.*
	
* **copiar_a_portapapeles**

	*Copia el contenido del campo estado de la botonera.*
	
* **deployador**
	
	*Copia el war generado en un proyecto y lo copia en la carpeta de deploy de wildfly, cambia o genera el archivo **proyecto**.war.dodeploy*
	
* **generar_url_app**

	*Genera la url para acceder a una aplicación teniendo en cuenta el ambiente al que se quiere ingresar.*
	
* **get_hoy**

	*Genera la fecha de hoy en formato YYYYMMDD y la copia en el campo estado.*
	
* **ip_hoy**
	
	*Copia en el campo estado la ip actual de la máquina.*
	
* **limpiar_deploy**
	
	*Elimina los war en la carpeta deploy del servidor Jboss.*
	
* **limpiar_deployments**
	
	*Elimina los war en la carpeta deploy del servidor Wildfly.*
	
* **limpiar_estado**

	*Elimina el contenido del campo estado.*
	
* **limpiar_logs**

	*Vacía los archivos server.log, boot.log del servidor Wildfly y de Jboss (agrega 2 botones)*
	
* **manipulador_cadenas**

	*Permite hacer acciones sobre una cadena que se ingresa.*
	
* **nombre_branch**

	*Genera un nombre de branch con el formato *Usuario*<fecha_formato_YYYYMMDD> y lo copia en el campo estado.*
	
* **nombre_tag**

	*Genera el nombre de un tag con formato TAG_PROYECTO_VVERSIONRELEASE_FECHA_VERSIONPOM*
	
* **nombre_war**
	
	*Genera el nombre del war a deployar en Wildfly indicando la versión del pom, por ejemplo: Proyecto-1.2.3.war*
	
* **preparar_deploy**

	*Genera una carpeta con nombre fecha de hoy en formato YYYYMMDD en la carpeta del proyecto a deployarse, dentro de esta carpeta se genera un txt con el tag y el nombre del war en cuestión.*

	