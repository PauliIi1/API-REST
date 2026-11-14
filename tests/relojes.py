class RelojFijo:
    """Reloj falso (stub) para las pruebas: siempre devuelve la misma fecha."""

    def __init__(self, fecha):
        self._fecha = fecha

    def hoy(self):
        return self._fecha
