"""Círculo 4 (Frameworks y Drivers): la web, con Flask.

Aquí está todo lo que sabe de Flask: las rutas, leer el JSON de la petición
y armar la respuesta HTTP. Es código de pegamento: toda la decisión la toma
el controlador.
"""
from flask import Flask, jsonify, request


def _responder(cuerpo, codigo):
    if cuerpo is None:
        return "", codigo
    return jsonify(cuerpo), codigo


def crear_app_flask(controlador):
    app = Flask(__name__)

    @app.get("/avistamientos")
    def listar():
        return _responder(*controlador.listar())

    @app.post("/avistamientos")
    def crear():
        datos = request.get_json(silent=True) or {}
        return _responder(*controlador.crear(datos))

    @app.get("/avistamientos/<int:id>")
    def ver(id):
        return _responder(*controlador.ver(id))

    @app.put("/avistamientos/<int:id>")
    def actualizar(id):
        datos = request.get_json(silent=True) or {}
        return _responder(*controlador.actualizar(id, datos))

    @app.delete("/avistamientos/<int:id>")
    def eliminar(id):
        return _responder(*controlador.eliminar(id))

    @app.get("/avistamientos/resumen")
    def resumen():
        return _responder(*controlador.resumen())

    return app
