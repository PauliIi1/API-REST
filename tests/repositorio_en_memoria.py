from dataclasses import replace

from avistamientos.use_cases.modelos import ConteoPorEspecie
from avistamientos.use_cases.puertos import RepositorioDeAvistamientos


class RepositorioEnMemoria(RepositorioDeAvistamientos):
    """Otro adaptador para el mismo puerto: guarda en un diccionario, sin base de datos."""

    def __init__(self):
        self._datos = {}
        self._siguiente_id = 1

    def listar(self):
        return list(self._datos.values())

    def buscar(self, id):
        return self._datos.get(id)

    def guardar(self, avistamiento):
        guardado = replace(avistamiento, id=self._siguiente_id)
        self._datos[guardado.id] = guardado
        self._siguiente_id += 1
        return guardado

    def actualizar(self, avistamiento):
        self._datos[avistamiento.id] = avistamiento

    def eliminar(self, id):
        self._datos.pop(id, None)

    def contar_por_especie(self):
        conteo = {}
        for a in self._datos.values():
            conteo[a.especie] = conteo.get(a.especie, 0) + 1
        return [ConteoPorEspecie(especie, total) for especie, total in conteo.items()]
