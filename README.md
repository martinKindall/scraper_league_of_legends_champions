# Scraper de campeones de League of Legends

### Instalar Chrome Driver

- Deben descargar una versión reciente del navegador Chrome
https://www.google.com/intl/es/chrome/

- Luego deben descargar chromeDriver según la versión de su navegador Chrome y el sistema operativo en el que estén.

- Deben colocar el archivo chromedriver.exe en el path mostrado en el código, al momento de usar Selenium, o pueden cambiar el path y el código también.

Si lo anterior no funciona, es posible que sea necesario que agreguen el chromedriver al PATH del sistema, para Windows hay que hacer esto:
https://stackoverflow.com/questions/49788257/what-is-default-location-of-chromedriver-and-for-installing-chrome-on-windows

### Inicializar DB

- Hay que crear una tabla en la base de datos mariaDB con el nombre que quieran.
- Deben copiar el archivo .env.default y crear un archivo .env que tenga las mismas variables, pero con las credenciales de la DB.

### Instalar requerimientos

Ejecutar en el proyecto:

```
pip install -r requirements.txt
```
