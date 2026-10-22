import sqlite3
from flask import Flask, request, jsonify
from validador import ValidadorDeAvistamiento

app = Flask(__name__)
DB = "avistamientos.db"
CAMPOS = ["especie", "lugar", "fecha", "observador"]
validador = ValidadorDeAvistamiento()

def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def crear_tabla():
    con = conectar()
    con.execute("""CREATE TABLE IF NOT EXISTS avistamientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        especie TEXT NOT NULL,
        lugar TEXT NOT NULL,
        fecha TEXT NOT NULL,
        observador TEXT NOT NULL)""")
    con.commit()
    con.close()

@app.get("/avistamientos")
def listar():
    con = conectar()
    filas = con.execute("SELECT * FROM avistamientos").fetchall()
    con.close()
    return jsonify([dict(f) for f in filas]), 200

@app.post("/avistamientos")
def crear():
    datos = request.get_json(silent=True) or {}
    error = validador.validar(datos)
    if error:
        return jsonify({"error": error}), 400
    
    con = conectar()
    cur = con.execute(
        "INSERT INTO avistamientos (especie, lugar, fecha, observador) VALUES (?, ?, ?, ?)",
        tuple(datos[c] for c in CAMPOS))
    con.commit()
    nuevo_id = cur.lastrowid
    con.close()
    return jsonify({"id": nuevo_id, **{c: datos[c] for c in CAMPOS}}), 201

def buscar(id):
    con = conectar()
    fila = con.execute("SELECT * FROM avistamientos WHERE id = ?", (id,)).fetchone()
    con.close()
    return fila

@app.get("/avistamientos/<int:id>")
def ver(id):
    fila = buscar(id)
    if fila is None:
        return jsonify({"error": "No existe"}), 404
    return jsonify(dict(fila)), 200

#actualizar
@app.put("/avistamientos/<int:id>")
def actualizar(id):
    if buscar(id) is None:
        return jsonify({"error": "No existe"}), 404
    datos = request.get_json(silent=True) or {}
    error = validador.validar(datos)
    if error:
        return jsonify({"error": error}), 400
    
    con = conectar()
    con.execute(
        "UPDATE avistamientos SET especie=?, lugar=?, fecha=?, observador=? WHERE id=?",
        tuple(datos[c] for c in CAMPOS) + (id,))
    con.commit()
    con.close()
    return jsonify({"id": id, **{c: datos[c] for c in CAMPOS}}), 200

@app.delete("/avistamientos/<int:id>")
def eliminar(id):
    if buscar(id) is None:
        return jsonify({"error": "No existe"}), 404
    con = conectar()
    con.execute("DELETE FROM avistamientos WHERE id = ?", (id,))
    con.commit()
    con.close()
    return "", 204

@app.get("/avistamientos/resumen")
def resumen():
    con = conectar()
    filas = con.execute(
        "SELECT especie, COUNT(*) AS total FROM avistamientos GROUP BY especie").fetchall()
    con.close()
    return jsonify([dict(f) for f in filas]), 200

if __name__ == "__main__":
    crear_tabla()
    app.run(debug=True)