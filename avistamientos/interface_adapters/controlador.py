"""Círculo 3 (Interface Adapters): controlador.

Recibe los datos ya extraídos de la petición web, llama al caso de uso que
corresponde y devuelve (cuerpo, código HTTP). Decide qué código HTTP le toca
a cada error de negocio. No importa Flask: quien lo llama (el círculo de
Frameworks y Drivers) es el que arma la respuesta real.
"""
from avistamientos.interface_adapters import presentador
from avistamientos.use_cases.errores import AvistamientoNoEncontrado, DatosInvalidos


class ControladorDeAvistamientos:
    def __init__(self, listar, ver, registrar, actualizar, eliminar, resumen):
        self._listar = listar
        self._ver = ver
        self._registrar = registrar
        self._actualizar = actualizar
        self._eliminar = eliminar
        self._resumen = resumen

    def listar(self):
        return presentador.presentar_lista(self._listar.ejecutar()), 200

    def ver(self, id):
        try:
            return presentador.presentar_avistamiento(self._ver.ejecutar(id)), 200
        except AvistamientoNoEncontrado:
            return presentador.presentar_error("No existe"), 404

    def crear(self, datos):
        try:
            return presentador.presentar_avistamiento(self._registrar.ejecutar(datos)), 201
        except DatosInvalidos as e:
            return presentador.presentar_error(str(e)), 400

    def actualizar(self, id, datos):
        try:
            return presentador.presentar_avistamiento(self._actualizar.ejecutar(id, datos)), 200
        except AvistamientoNoEncontrado:
            return presentador.presentar_error("No existe"), 404
        except DatosInvalidos as e:
            return presentador.presentar_error(str(e)), 400

    def eliminar(self, id):
        try:
            self._eliminar.ejecutar(id)
            return None, 204
        except AvistamientoNoEncontrado:
            return presentador.presentar_error("No existe"), 404

    def resumen(self):
        return presentador.presentar_resumen(self._resumen.ejecutar()), 200
