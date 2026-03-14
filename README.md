# Registrar_Estudiantes
Registrar estudiantes en una base de datos.

# API de Registro de Estudiantes con Flask

## Descripción

Esta práctica consiste en crear una API sencilla utilizando **Flask** y una base de datos **SQLite** que permita registrar estudiantes y consultar los registros almacenados.

La API tendrá dos endpoints principales:

* **POST /estudiantes** → Permite registrar un nuevo estudiante.
* **GET /estudiantes** → Permite consultar todos los estudiantes almacenados.

Cada estudiante debe tener los siguientes datos:

* **nombre**
* **carrera**
* **semestre**

El objetivo es aprender a conectar una API con una base de datos y realizar operaciones básicas de almacenamiento y consulta.

---

# Requisitos

Antes de ejecutar el proyecto es necesario tener instalado:

* Python 3
* pip

Instalar Flask:

```bash
pip install flask
```

---

# Estructura del Proyecto

```
mi_api/
│
├── app.py
├── estudiantes.db
└── README.md
```

---

# Código de la API (app.py)

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "estudiantes.db"

# Crear tabla si no existe
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        carrera TEXT NOT NULL,
        semestre INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Endpoint POST /estudiantes
@app.route('/estudiantes', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()

    nombre = data.get('nombre')
    carrera = data.get('carrera')
    semestre = data.get('semestre')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO estudiantes (nombre, carrera, semestre) VALUES (?, ?, ?)",
        (nombre, carrera, semestre)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Estudiante registrado correctamente"}), 201


# Endpoint GET /estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    conn = get_db_connection()
    estudiantes = conn.execute("SELECT * FROM estudiantes").fetchall()
    conn.close()

    lista = []

    for estudiante in estudiantes:
        lista.append({
            "id": estudiante["id"],
            "nombre": estudiante["nombre"],
            "carrera": estudiante["carrera"],
            "semestre": estudiante["semestre"]
        })

    return jsonify(lista)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

---

# Ejecutar la API

Abrir una terminal en la carpeta del proyecto y ejecutar:

```bash
python app.py
```

El servidor se iniciará en:

```
http://127.0.0.1:5000
```

---

# Probar los Endpoints

## Registrar estudiante (POSTMAN)

Método:

```
POST /estudiantes
```

URL completa:

```
http://127.0.0.1:5000/estudiantes
```

Body (JSON):

```json
{
  "nombre": "Juan Perez",
  "carrera": "Ingenieria en Sistemas",
  "semestre": 3
}
```

Respuesta esperada:

```json
{
  "mensaje": "Estudiante registrado correctamente"
}
```

---

## Consultar estudiantes

Método:

```
GET /estudiantes
```

URL completa:

```
http://127.0.0.1:5000/estudiantes
```

Respuesta esperada:

```json
[
  {
    "id": 1,
    "nombre": "Juan Perez",
    "carrera": "Ingenieria en Sistemas",
    "semestre": 3
  }
]
```

---

# Herramientas para probar la API

Se puede probar la API utilizando herramientas como:

* Postman
* curl desde la terminal
* extensiones de REST para VS Code

---

# Objetivos de Aprendizaje

Con esta práctica se aprende a:

* Crear una API con Flask
* Conectar Python con una base de datos SQLite
* Crear tablas en una base de datos
* Insertar registros con el método POST
* Consultar datos con el método GET
* Trabajar con datos en formato JSON
