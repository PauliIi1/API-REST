"""Círculo 2 (Use Cases): el puerto de salida hacia el almacenamiento.

Es la interfaz que los casos de uso necesitan para guardar y leer datos.
La define el círculo de adentro; la implementa uno de afuera
(avistamientos/interface_adapters/repositorio_sqlite.py).
Eso es la inversión de dependencias: el código fuente de afuera apunta hacia
adentro aunque el flujo de control vaya hacia afuera.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from avistamientos.entities.avistamiento import Avistamiento
from avistamientos.use_cases.modelos import ConteoPorEspecie


class RepositorioDeAvistamientos(ABC):
    @abstractmethod
    def listar(self) -> List[Avistamiento]:
        """Todos los avistamientos, en el orden en que se guardaron."""

    @abstractmethod
    def buscar(self, id: int) -> Optional[Avistamiento]:
        """El avistamiento con ese id, o None si no existe."""

    @abstractmethod
    def guardar(self, avistamiento: Avistamiento) -> Avistamiento:
        """Guarda uno nuevo y lo devuelve con el id asignado."""

    @abstractmethod
    def actualizar(self, avistamiento: Avistamiento) -> None:
        """Reemplaza los datos del avistamiento que tiene ese id."""

    @abstractmethod
    def eliminar(self, id: int) -> None:
        """Borra el avistamiento con ese id."""

    @abstractmethod
    def contar_por_especie(self) -> List[ConteoPorEspecie]:
        """Cuántos avistamientos hay de cada especie."""
