"""Círculo 1 (Entities): la regla de negocio de un avistamiento.

Un avistamiento es válido si la especie tiene entre 3 y 50 caracteres, la
fecha tiene el formato AAAA-MM-DD y no es posterior a hoy, y el lugar y el
observador no están vacíos.

No sabe nada de Flask ni de la base de datos. Tampoco sabe de dónde sale la
fecha de hoy: la recibe de un reloj que le inyectan (cualquier objeto con un
método hoy()).
"""
import re
from datetime import datetime

FORMATO_FECHA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class ValidadorDeAvistamiento:
    def __init__(self, reloj):
        self.reloj = reloj

    def validar(self, datos):
        """Devuelve None si es válido, o un mensaje que dice qué campo falló."""
        if not isinstance(datos, dict):
            return "el cuerpo debe ser un objeto JSON"

        error = self._validar_especie(datos.get("especie"))
        if error:
            return error
        error = self._validar_fecha(datos.get("fecha"))
        if error:
            return error
        error = self._validar_texto("lugar", datos.get("lugar"))
        if error:
            return error
        return self._validar_texto("observador", datos.get("observador"))

    def _validar_especie(self, especie):
        if not isinstance(especie, str) or not 3 <= len(especie.strip()) <= 50:
            return "especie: debe tener entre 3 y 50 caracteres"
        return None

    def _validar_fecha(self, fecha):
        if not isinstance(fecha, str) or not FORMATO_FECHA.fullmatch(fecha):
            return "fecha: debe tener el formato AAAA-MM-DD"
        try:
            fecha_real = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return "fecha: no es una fecha que exista"
        if fecha_real > self.reloj.hoy():
            return "fecha: no puede ser posterior a hoy"
        return None

    def _validar_texto(self, campo, valor):
        if not isinstance(valor, str) or not valor.strip():
            return f"{campo}: no puede estar vacío"
        return None
