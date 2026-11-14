"""Círculo 2 (Use Cases): las reglas de negocio propias de la aplicación.

Cada clase es un caso de uso. Reciben el puerto del repositorio y el
validador por el constructor (no los crean), y devuelven datos simples.
No importan nada de Flask ni de SQLite.
"""
from avistamientos.entities.avistamiento import CAMPOS, Avistamiento
from avistamientos.use_cases.errores import AvistamientoNoEncontrado, DatosInvalidos
from avistamientos.use_cases.modelos import AvistamientoSalida


def _a_salida(avistamiento):
    return AvistamientoSalida(
        id=avistamiento.id,
        especie=avistamiento.especie,
        lugar=avistamiento.lugar,
        fecha=avistamiento.fecha,
        observador=avistamiento.observador,
    )


class ListarAvistamientos:
    def __init__(self, repositorio):
        self._repositorio = repositorio

    def ejecutar(self):
        return [_a_salida(a) for a in self._repositorio.listar()]


class VerAvistamiento:
    def __init__(self, repositorio):
        self._repositorio = repositorio

    def ejecutar(self, id):
        avistamiento = self._repositorio.buscar(id)
        if avistamiento is None:
            raise AvistamientoNoEncontrado(id)
        return _a_salida(avistamiento)


class RegistrarAvistamiento:
    def __init__(self, repositorio, validador):
        self._repositorio = repositorio
        self._validador = validador

    def ejecutar(self, datos):
        error = self._validador.validar(datos)
        if error:
            raise DatosInvalidos(error)
        nuevo = Avistamiento(id=None, **{c: datos[c] for c in CAMPOS})
        return _a_salida(self._repositorio.guardar(nuevo))


class ActualizarAvistamiento:
    def __init__(self, repositorio, validador):
        self._repositorio = repositorio
        self._validador = validador

    def ejecutar(self, id, datos):
        # Primero se revisa que exista (404) y después que los datos sean válidos (400).
        if self._repositorio.buscar(id) is None:
            raise AvistamientoNoEncontrado(id)
        error = self._validador.validar(datos)
        if error:
            raise DatosInvalidos(error)
        cambiado = Avistamiento(id=id, **{c: datos[c] for c in CAMPOS})
        self._repositorio.actualizar(cambiado)
        return _a_salida(cambiado)


class EliminarAvistamiento:
    def __init__(self, repositorio):
        self._repositorio = repositorio

    def ejecutar(self, id):
        if self._repositorio.buscar(id) is None:
            raise AvistamientoNoEncontrado(id)
        self._repositorio.eliminar(id)


class ResumenPorEspecie:
    def __init__(self, repositorio):
        self._repositorio = repositorio

    def ejecutar(self):
        return self._repositorio.contar_por_especie()
