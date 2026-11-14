"""Círculo 3 (Interface Adapters): presentador.

Convierte lo que devuelven los casos de uso (datos simples) en el formato
que va a salir por la web: diccionarios listos para convertir en JSON.
"""


def presentar_avistamiento(salida):
    return {
        "id": salida.id,
        "especie": salida.especie,
        "lugar": salida.lugar,
        "fecha": salida.fecha,
        "observador": salida.observador,
    }


def presentar_lista(salidas):
    return [presentar_avistamiento(s) for s in salidas]


def presentar_resumen(conteos):
    return [{"especie": c.especie, "total": c.total} for c in conteos]


def presentar_error(mensaje):
    return {"error": mensaje}
