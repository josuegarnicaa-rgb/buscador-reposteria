# Buscador Semántico de Repostería

Este proyecto es un buscador semántico desarrollado con **Python** y **Flask**. Permite cargar una ontología en formato `.owx` y buscar información relacionada con productos, recetas, ingredientes, herramientas y relaciones del dominio de la repostería.

---

## 1. Descripción del proyecto

El sistema utiliza una ontología de repostería para representar conocimiento mediante clases, individuos, propiedades y relaciones.  
El buscador permite consultar elementos como:

- Productos de repostería
- Ingredientes
- Recetas
- Herramientas
- Clases
- Relaciones semánticas
- Atributos de los individuos

---

## 2. Tecnologías utilizadas

- **Python 3.14.5**
- **Flask**
- **HTML**
- **CSS**
- **Ontología OWX / OWL XML**

---

## 3. Descargar Python

Para ejecutar el proyecto se debe instalar Python desde la página oficial:

https://www.python.org/downloads/windows/

Se recomienda usar **Python 3.14.5 (64-bit)** o una versión estable superior.

---

## 4. Instalación de Python

Al abrir el instalador de Python, antes de instalar se deben marcar las siguientes opciones:

- **Add python.exe to PATH**
- **Use admin privileges when installing py.exe**

La opción más importante es:

```text
Add python.exe to PATH
```

Esta opción permite usar los comandos `python` y `pip` desde la terminal.

Imagen de referencia:

![Instalación de Python con PATH marcado](static/instalacion-python.png)

Luego presionar:

```text
Install Now
```

---

## 5. Estructura del proyecto

La estructura del proyecto debe quedar de la siguiente forma:

```text
buscador-reposteria/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
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

---

## 6. Explicación de archivos y carpetas

### `app.py`

Archivo principal del proyecto. Contiene el código Python que carga la ontología y ejecuta el servidor Flask.

### `requirements.txt`

Archivo donde se indican las librerías necesarias para ejecutar el proyecto.

### `ontologia/reposteria.owx`

Archivo de la ontología de repostería.

### `templates/index.html`

Archivo HTML principal de la interfaz del buscador.

### `static/estilos.css`

Archivo CSS que contiene los estilos visuales del proyecto.

### `static/instalacion-python.png`

Imagen de referencia para la instalación de Python.

### `.gitignore`

Archivo que evita subir a GitHub carpetas o archivos innecesarios como entornos virtuales, caché o archivos temporales.

---

## 7. Contenido de `requirements.txt`

El archivo `requirements.txt` debe contener:

```text
Flask
```

---

## 8. Verificar que Python está instalado

Abrir la terminal de Visual Studio Code o PowerShell y ejecutar:

```powershell
python --version
```

Si todo está correctamente instalado, debe aparecer algo parecido a:

```text
Python 3.14.5
```

---

## 9. Entrar a la carpeta del proyecto

Primero se debe abrir una terminal dentro de la carpeta del proyecto.

La carpeta principal debe ser:

```text
buscador-reposteria
```

Si la terminal no está dentro de esa carpeta, se puede ingresar con:

```powershell
cd buscador-reposteria
```

También se puede abrir directamente la carpeta `buscador-reposteria` desde Visual Studio Code.

---

## 10. Instalar las dependencias

Dentro de la carpeta del proyecto, ejecutar:

```powershell
python -m pip install -r requirements.txt
```

Este comando instala Flask, que es necesario para ejecutar el buscador.

---

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

Cuando aparezca:

```text
Running on http://127.0.0.1:5000
```

el proyecto ya estará funcionando.

---

## 12. Abrir el buscador en el navegador

Abrir el navegador y entrar a:

```text
http://127.0.0.1:5000
```

Desde ahí se puede usar el buscador semántico.

---

## 13. Palabras que se pueden probar

Algunas búsquedas recomendadas son:

- chocolate
- torta
- huevo
- harina
- batidora
- receta
- cupcake

---

## 14. Cómo detener el servidor

Para detener el servidor Flask, presionar en la terminal:

```text
CTRL + C
```

---

## 15. Cómo volver a usar el proyecto otro día

No es necesario instalar Flask otra vez si ya fue instalado anteriormente.

Solo se debe abrir la carpeta del proyecto en Visual Studio Code o entrar a la carpeta desde la terminal:

```powershell
cd buscador-reposteria
```

Luego ejecutar:

```powershell
python app.py
```

Después abrir nuevamente en el navegador:

```text
http://127.0.0.1:5000
```

---

## 16. Posibles errores y soluciones

### Error: `python` no se reconoce

Este error significa que Python no está instalado correctamente o no se marcó la opción:

```text
Add python.exe to PATH
```

Solución:

Reinstalar Python y marcar la casilla **Add python.exe to PATH**.

---

### Error: `pip` no se reconoce

Usar este comando en lugar de `pip` directamente:

```powershell
python -m pip install -r requirements.txt
```

---

### Error: no encuentra `reposteria.owx`

Verificar que el archivo esté ubicado exactamente aquí:

```text
ontologia/reposteria.owx
```

---

## 17. Subir cambios a GitHub

Después de modificar archivos, se pueden subir los cambios con:

```powershell
git add .
git commit -m "actualizar proyecto"
git push
```

---

## 18. Autor

Proyecto desarrollado para la materia de **Web Semántica**.
