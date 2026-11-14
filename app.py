import sqlite3
from flask import Flask, request, jsonify
from avistamientos.entities.validador import ValidadorDeAvistamiento
from avistamientos.frameworks_and_drivers.reloj_sistema import RelojSistema
from avistamientos.interface_adapters.controlador import ControladorDeAvistamientos
from avistamientos.interface_adapters.repositorio_sqlite import RepositorioSqlite
from avistamientos.use_cases.casos_de_uso import (
    ActualizarAvistamiento, EliminarAvistamiento, ListarAvistamientos,
    RegistrarAvistamiento, ResumenPorEspecie, VerAvistamiento)

app = Flask(__name__)
DB = "avistamientos.db"
CAMPOS = ["especie", "lugar", "fecha", "observador"]
validador = ValidadorDeAvistamiento(RelojSistema())

def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def crear_tabla():
    RepositorioSqlite(DB).crear_tabla()

def controlador():
    repo = RepositorioSqlite(DB)
    return ControladorDeAvistamientos(
        ListarAvistamientos(repo), VerAvistamiento(repo),
        RegistrarAvistamiento(repo, validador), ActualizarAvistamiento(repo, validador),
        EliminarAvistamiento(repo), ResumenPorEspecie(repo))

# ---- lecturas: ya pasan por el controlador y los casos de uso ----
@app.get("/avistamientos")
def listar():
    cuerpo, codigo = controlador().listar()
    return jsonify(cuerpo), codigo

@app.get("/avistamientos/<int:id>")
def ver(id):
    cuerpo, codigo = controlador().ver(id)
    return jsonify(cuerpo), codigo

@app.get("/avistamientos/resumen")
def resumen():
    cuerpo, codigo = controlador().resumen()
    return jsonify(cuerpo), codigo

# ---- escrituras: todavía con el código de antes ----
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

if __name__ == "__main__":
    crear_tabla()
    app.run(debug=True)
