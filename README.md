# Buscador Semántico de Repostería

Buscador semántico desarrollado con **React** y **Flask** que permite consultar una ontología de repostería en formato `.owx`. Soporta búsqueda de productos, recetas, ingredientes, herramientas y relaciones semánticas, con resultados enriquecidos desde **DBpedia local y remota**, y traducción automática a 5 idiomas (español, inglés, portugués, francés e italiano).

---

## Índice

1. [Tecnologías](#1-tecnologías)
2. [Requisitos previos](#2-requisitos-previos)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Instalación](#4-instalación)
5. [Ejecución](#5-ejecución)
6. [Acceso](#6-acceso)

---

## 1. Tecnologías

| Capa           | Tecnología                            |
| -------------- | ------------------------------------- |
| Backend        | Python 3.14, Flask                    |
| Frontend       | React, TypeScript, Tailwind CSS, Vite |
| Ontología      | OWL XML (`.owx`)                      |
| Traducción     | deep-translator (Google Translate)    |
| Datos externos | DBpedia (SPARQL remoto y dump local)  |

---

## 2. Requisitos previos

Antes de instalar el proyecto se deben tener instalados **Python** y **Node.js**.

### Python

Descargar desde: <https://www.python.org/downloads/>

Se recomienda **Python 3.14**.

> ⚠️ Durante la instalación marcar obligatoriamente estas opciones antes de continuar:
>
> - `Add python.exe to PATH`
> - `Use admin privileges when installing py.exe`

![Instalación de Python con PATH marcado](backend/static/instalacion-python.png)

Sin la opción `Add python.exe to PATH` los comandos `python` y `pip` no funcionarán en la terminal.

### Node.js

Descargar desde: <https://nodejs.org/es/download>

Se recomienda la versión **LTS** para garantizar estabilidad y compatibilidad.

### Verificar instalación

Abrir una terminal y ejecutar:

```powershell
python --version
pip --version
node --version
npm --version
```

Todos los comandos deben devolver una versión. Si alguno falla, revisar que esté correctamente agregado al PATH.

---

## 3. Estructura del proyecto

```text
buscador-reposteria/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── cache/
│   │   └── traducciones.json
│   ├── services/
│   │   ├── i18n.py
│   │   ├── dbpedia.py
│   │   └── dbpedia_local.py
│   └── ontologia/
│   │   ├── reposteria.owx
│   │   └── dbpedia_local.owx
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── index.css
│       ├── components/
│       ├── hooks/
│       ├── types/
│       └── config/
└── README.md
```

---

## 4. Instalación

### 4.1 Clonar el repositorio

```powershell
git clone https://github.com/josuegarnicaa-rgb/buscador-reposteria.git
cd buscador-reposteria
```

### 4.2 Backend

```powershell
cd backend
pip install -r requirements.txt
```

Verificar que las dependencias se instalaron correctamente:

```powershell
pip list
```

### 4.3 Frontend

```powershell
cd frontend
npm install
```

> Si se usa **bun** en lugar de npm:
>
> ```powershell
> bun install
> ```

---

## 5. Ejecución

Backend y frontend deben ejecutarse **al mismo tiempo**, cada uno en una terminal separada.

### Terminal 1 — Backend

```powershell
cd backend
python app.py
```

Salida esperada:

```text
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Terminal 2 — Frontend

```powershell
cd frontend
npm run dev
```

Salida esperada:

```text
  VITE v6.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

> ⚠️ El backend debe estar corriendo **antes** de usar el frontend, ya que este consume la API en `localhost:5000`.

---

## 6. Acceso

| Servicio          | URL                                                        |
| ----------------- | ---------------------------------------------------------- |
| Frontend          | <http://localhost:5173>                                    |
| Backend (API)     | <http://localhost:5000>                                    |
| Endpoint búsqueda | <http://localhost:5000/api/buscar?termino=torta&idioma=es> |
