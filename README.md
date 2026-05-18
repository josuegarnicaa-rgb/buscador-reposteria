# README - Buscador Semántico de Repostería

Guía de instalación, estructura y ejecución del proyecto.

## 1. Descripción del proyecto

Este proyecto es un **Buscador Semántico de Repostería** desarrollado con **Python** y **Flask**. El sistema permite cargar una ontología en formato **`.owx`** y realizar búsquedas sobre elementos relacionados con repostería, como productos, ingredientes, recetas, herramientas, clases, propiedades y relaciones.

## 2. Tecnologías utilizadas

- **Python 3.14.5:** lenguaje principal del proyecto.
- **Flask:** framework usado para levantar el servidor web.
- **HTML:** estructura de la interfaz del buscador.
- **CSS:** estilos visuales del buscador.
- **OWX / OWL XML:** archivo de la ontología de repostería.

## 3. Descargar Python

Para que el proyecto funcione, primero se debe instalar Python desde la página oficial:

[Descargar Python para Windows](https://www.python.org/downloads/windows/)

Se recomienda usar **Python 3.14.5 (64-bit)** o una versión estable superior.

## 4. Instalación de Python

Al abrir el instalador de Python, es importante marcar las siguientes opciones antes de instalar:

- **Add python.exe to PATH**
- **Use admin privileges when installing py.exe**

> **Importante:** La opción más importante es `Add python.exe to PATH`, porque permite usar los comandos `python` y `pip` desde la terminal.

Imagen de referencia:

![Instalación de Python con PATH marcado](static/instalacion-python.png)

Después de marcar las opciones, presionar:

```text
Install Now
```

## 5. Estructura del proyecto

La estructura del proyecto debe quedar de la siguiente forma:

```text
buscador-reposteria/
│
├── app.py
├── requirements.txt
├── README.md
│
├── ontologia/
│   └── reposteria.owx
│
├── static/
│   ├── estilos.css
│   └── instalacion-python.png
│
└── templates/
    └── index.html
```

## 6. Explicación de archivos y carpetas

- **`app.py`:** archivo principal del proyecto. Contiene el código Python que carga la ontología y ejecuta el servidor Flask.
- **`requirements.txt`:** contiene las librerías necesarias para ejecutar el proyecto.
- **`ontologia/reposteria.owx`:** archivo de la ontología de repostería.
- **`templates/index.html`:** interfaz principal del buscador.
- **`static/estilos.css`:** archivo de estilos CSS del proyecto.
- **`static/instalacion-python.png`:** imagen usada como referencia para instalar Python.

## 7. Contenido de requirements.txt

El archivo **`requirements.txt`** debe contener:

```txt
Flask
```

## 8. Verificar que Python está instalado

Abrir la terminal de Visual Studio Code y ejecutar:

```powershell
python --version
```

Si todo está correcto, debe aparecer algo parecido a:

```text
Python 3.14.5
```

## 9. Entrar a la carpeta del proyecto

Desde PowerShell o la terminal de Visual Studio Code, entrar a la carpeta:

```powershell
cd "C:\Users\USUARIO\Documents\WEB - SEMANTICA\SP- WEB SEMATICA\proeycto de otros\MI.WEB.SEMANTICA\buscador-reposteria"
```

> Si el proyecto está en otra ubicación, se debe cambiar la ruta anterior por la ruta real del proyecto.

## 10. Instalar las dependencias

Ejecutar el siguiente comando:

```powershell
python -m pip install -r requirements.txt
```

Este comando instala Flask, que es necesario para ejecutar el buscador.

## 11. Ejecutar el proyecto

Para iniciar el servidor, ejecutar:

```powershell
python app.py
```

Si todo funciona correctamente, aparecerá un mensaje parecido a:

```text
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

> Cuando aparezca `Running on http://127.0.0.1:5000`, el proyecto ya está funcionando.

## 12. Abrir el buscador en el navegador

Abrir el navegador y entrar a:

```text
http://127.0.0.1:5000
```

Desde ahí se puede usar el buscador semántico.

## 13. Palabras que se pueden probar

Algunas búsquedas recomendadas son:

- `chocolate`
- `torta`
- `huevo`
- `harina`
- `batidora`
- `receta`
- `cupcake`

## 14. Cómo detener el servidor

Para detener el servidor Flask, presionar en la terminal:

```text
CTRL + C
```

## 15. Cómo volver a usar el proyecto otro día

No es necesario instalar Flask otra vez. Solo se debe abrir la terminal, entrar a la carpeta del proyecto y ejecutar:

```powershell
cd "C:\Users\USUARIO\Documents\WEB - SEMANTICA\SP- WEB SEMATICA\proeycto de otros\MI.WEB.SEMANTICA\buscador-reposteria"
python app.py
```

Luego abrir nuevamente:

```text
http://127.0.0.1:5000
```

## 16. Posibles errores y soluciones

### Error: python no se reconoce

Significa que Python no está instalado correctamente o no se marcó la opción `Add python.exe to PATH`.

**Solución:** reinstalar Python y marcar la casilla `Add python.exe to PATH`.

### Error: pip no se reconoce

Usar este comando en lugar de `pip` directamente:

```powershell
python -m pip install -r requirements.txt
```

### Error: no encuentra reposteria.owx

Verificar que el archivo esté ubicado exactamente aquí:

```text
ontologia/reposteria.owx
```

## 17. Autor

Proyecto desarrollado para la materia de **Web Semántica**.
