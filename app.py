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
validador = ValidadorDeAvistamiento(RelojSistema())

def crear_tabla():
    RepositorioSqlite(DB).crear_tabla()

def controlador():
    repo = RepositorioSqlite(DB)
    return ControladorDeAvistamientos(
        ListarAvistamientos(repo), VerAvistamiento(repo),
        RegistrarAvistamiento(repo, validador), ActualizarAvistamiento(repo, validador),
        EliminarAvistamiento(repo), ResumenPorEspecie(repo))

def responder(cuerpo, codigo):
    if cuerpo is None:
        return "", codigo
    return jsonify(cuerpo), codigo

@app.get("/avistamientos")
def listar():
    return responder(*controlador().listar())

@app.post("/avistamientos")
def crear():
    datos = request.get_json(silent=True) or {}
    return responder(*controlador().crear(datos))

@app.get("/avistamientos/<int:id>")
def ver(id):
    return responder(*controlador().ver(id))

@app.put("/avistamientos/<int:id>")
def actualizar(id):
    datos = request.get_json(silent=True) or {}
    return responder(*controlador().actualizar(id, datos))

@app.delete("/avistamientos/<int:id>")
def eliminar(id):
    return responder(*controlador().eliminar(id))

@app.get("/avistamientos/resumen")
def resumen():
    return responder(*controlador().resumen())

if __name__ == "__main__":
    crear_tabla()
    app.run(debug=True)
