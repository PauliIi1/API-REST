"""Círculo 4 (Frameworks y Drivers): el reloj real del computador."""
from datetime import date


class RelojSistema:
    """Reloj real: devuelve la fecha de hoy del computador."""

    def hoy(self):
        return date.today()
