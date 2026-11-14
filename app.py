"""Punto de entrada y raíz de composición.

Es el único archivo que conoce todas las piezas de todos los círculos: crea
cada una y se la pasa a la que la necesita. Para cambiar la base de datos,
el reloj o la web, se cambia aquí y nada de adentro se entera.

Ejecutar: python app.py
"""
from avistamientos.entities.validador import ValidadorDeAvistamiento
from avistamientos.frameworks_and_drivers.reloj_sistema import RelojSistema
from avistamientos.frameworks_and_drivers.web_flask import crear_app_flask
from avistamientos.interface_adapters.controlador import ControladorDeAvistamientos
from avistamientos.interface_adapters.repositorio_sqlite import RepositorioSqlite
from avistamientos.use_cases.casos_de_uso import (
    ActualizarAvistamiento, EliminarAvistamiento, ListarAvistamientos,
    RegistrarAvistamiento, ResumenPorEspecie, VerAvistamiento)

DB = "avistamientos.db"


def crear_aplicacion(ruta_db=DB, reloj=None):
    repositorio = RepositorioSqlite(ruta_db)
    repositorio.crear_tabla()
    validador = ValidadorDeAvistamiento(reloj or RelojSistema())

    controlador = ControladorDeAvistamientos(
        listar=ListarAvistamientos(repositorio),
        ver=VerAvistamiento(repositorio),
        registrar=RegistrarAvistamiento(repositorio, validador),
        actualizar=ActualizarAvistamiento(repositorio, validador),
        eliminar=EliminarAvistamiento(repositorio),
        resumen=ResumenPorEspecie(repositorio),
    )
    return crear_app_flask(controlador)


if __name__ == "__main__":
    crear_aplicacion().run(debug=True)
