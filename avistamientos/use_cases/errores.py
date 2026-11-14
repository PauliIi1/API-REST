"""Círculo 2 (Use Cases): errores que los casos de uso le comunican al exterior.

Así el caso de uso no necesita saber de códigos HTTP: dice qué pasó
y quien está afuera decide cómo mostrarlo.
"""


class DatosInvalidos(Exception):
    """Los datos no cumplen la regla de negocio. El mensaje dice qué campo falló."""


class AvistamientoNoEncontrado(Exception):
    """No existe un avistamiento con ese id."""
