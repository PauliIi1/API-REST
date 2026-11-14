"""Círculo 1 (Entities): el objeto de negocio central.

No importa nada de Flask, de SQLite ni de ninguna otra capa del proyecto.
"""
from dataclasses import dataclass
from typing import Optional

# Los campos que describen un avistamiento (el id lo asigna quien guarda).
CAMPOS = ("especie", "lugar", "fecha", "observador")


@dataclass
class Avistamiento:
    id: Optional[int]
    especie: str
    lugar: str
    fecha: str
    observador: str
