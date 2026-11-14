"""Pruebas unitarias de los casos de uso.

No usan Flask ni SQLite: el repositorio es uno en memoria y el reloj es fijo.
Esto es lo que permite la arquitectura: probar las reglas de la aplicación solas.
"""
from datetime import date

import pytest

from avistamientos.entities.validador import ValidadorDeAvistamiento
from avistamientos.use_cases.casos_de_uso import (
    ActualizarAvistamiento, EliminarAvistamiento, ListarAvistamientos,
    RegistrarAvistamiento, ResumenPorEspecie, VerAvistamiento)
from avistamientos.use_cases.errores import AvistamientoNoEncontrado, DatosInvalidos
from tests.relojes import RelojFijo
from tests.repositorio_en_memoria import RepositorioEnMemoria

DATOS = {"especie": "colibri", "lugar": "Chia", "fecha": "2026-09-20", "observador": "Paula"}


@pytest.fixture
def repositorio():
    return RepositorioEnMemoria()


@pytest.fixture
def validador():
    return ValidadorDeAvistamiento(RelojFijo(date(2026, 10, 21)))


def test_registrar_valido_guarda_y_devuelve_el_id(repositorio, validador):
    salida = RegistrarAvistamiento(repositorio, validador).ejecutar(DATOS)

    assert salida.id == 1
    assert salida.especie == "colibri"
    assert len(repositorio.listar()) == 1


def test_registrar_invalido_lanza_error_y_no_guarda(repositorio, validador):
    with pytest.raises(DatosInvalidos) as error:
        RegistrarAvistamiento(repositorio, validador).ejecutar({**DATOS, "especie": "ab"})

    assert "especie" in str(error.value)
    assert repositorio.listar() == []


def test_ver_existente_devuelve_los_datos(repositorio, validador):
    nuevo = RegistrarAvistamiento(repositorio, validador).ejecutar(DATOS)

    assert VerAvistamiento(repositorio).ejecutar(nuevo.id) == nuevo


def test_ver_inexistente_lanza_no_encontrado(repositorio):
    with pytest.raises(AvistamientoNoEncontrado):
        VerAvistamiento(repositorio).ejecutar(999)


def test_listar_devuelve_todos(repositorio, validador):
    registrar = RegistrarAvistamiento(repositorio, validador)
    registrar.ejecutar(DATOS)
    registrar.ejecutar({**DATOS, "especie": "guacamaya"})

    assert [a.especie for a in ListarAvistamientos(repositorio).ejecutar()] == ["colibri", "guacamaya"]


def test_actualizar_valido_cambia_los_datos(repositorio, validador):
    nuevo = RegistrarAvistamiento(repositorio, validador).ejecutar(DATOS)

    salida = ActualizarAvistamiento(repositorio, validador).ejecutar(nuevo.id, {**DATOS, "lugar": "Bogota"})

    assert salida.lugar == "Bogota"
    assert VerAvistamiento(repositorio).ejecutar(nuevo.id).lugar == "Bogota"


def test_actualizar_inexistente_responde_no_encontrado_antes_que_invalido(repositorio, validador):
    # Aunque los datos sean inválidos, primero se revisa que el id exista.
    with pytest.raises(AvistamientoNoEncontrado):
        ActualizarAvistamiento(repositorio, validador).ejecutar(999, {**DATOS, "especie": ""})


def test_actualizar_invalido_no_cambia_los_datos(repositorio, validador):
    nuevo = RegistrarAvistamiento(repositorio, validador).ejecutar(DATOS)

    with pytest.raises(DatosInvalidos):
        ActualizarAvistamiento(repositorio, validador).ejecutar(nuevo.id, {**DATOS, "observador": ""})

    assert VerAvistamiento(repositorio).ejecutar(nuevo.id) == nuevo


def test_eliminar_borra_el_avistamiento(repositorio, validador):
    nuevo = RegistrarAvistamiento(repositorio, validador).ejecutar(DATOS)

    EliminarAvistamiento(repositorio).ejecutar(nuevo.id)

    with pytest.raises(AvistamientoNoEncontrado):
        VerAvistamiento(repositorio).ejecutar(nuevo.id)


def test_eliminar_inexistente_lanza_no_encontrado(repositorio):
    with pytest.raises(AvistamientoNoEncontrado):
        EliminarAvistamiento(repositorio).ejecutar(999)


def test_resumen_cuenta_por_especie(repositorio, validador):
    registrar = RegistrarAvistamiento(repositorio, validador)
    registrar.ejecutar(DATOS)
    registrar.ejecutar({**DATOS, "lugar": "Bogota"})
    registrar.ejecutar({**DATOS, "especie": "guacamaya"})

    conteo = {c.especie: c.total for c in ResumenPorEspecie(repositorio).ejecutar()}

    assert conteo == {"colibri": 2, "guacamaya": 1}
