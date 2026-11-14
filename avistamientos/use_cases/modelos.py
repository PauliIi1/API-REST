"""Círculo 2 (Use Cases): estructuras de datos simples que cruzan la frontera.

Martin (2012) pide que por las fronteras crucen datos simples y no las
entidades ni las filas de la base de datos. Estas dos son esos datos.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AvistamientoSalida:
    id: Optional[int]
    especie: str
    lugar: str
    fecha: str
    observador: str


@dataclass(frozen=True)
class ConteoPorEspecie:
    especie: str
    total: int
