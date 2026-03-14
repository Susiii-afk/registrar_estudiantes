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


# Conectar a la base de datos
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

    return jsonify({
        "mensaje": "Estudiante registrado correctamente"
    }), 201


# Endpoint GET /estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    conn = get_db_connection()
    estudiantes = conn.execute("SELECT * FROM estudiantes").fetchall()
    conn.close()

    lista_estudiantes = []

    for estudiante in estudiantes:
        lista_estudiantes.append({
            "id": estudiante["id"],
            "nombre": estudiante["nombre"],
            "carrera": estudiante["carrera"],
            "semestre": estudiante["semestre"]
        })

    return jsonify(lista_estudiantes)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)