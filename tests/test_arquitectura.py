"""Verifica la regla de dependencia (Martin, 2012): el código fuente solo puede
apuntar hacia adentro. Lee los import de cada archivo y falla si una capa
importa algo de una capa más externa, o si una capa interna importa Flask o SQLite.
"""
import ast
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent / "avistamientos"

# De adentro hacia afuera
CAPAS = ["entities", "use_cases", "interface_adapters", "frameworks_and_drivers"]


def _archivos(capa):
    return sorted((RAIZ / capa).glob("*.py"))


def _imports(archivo):
    arbol = ast.parse(archivo.read_text(encoding="utf-8"))
    nombres = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            nombres += [a.name for a in nodo.names]
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            nombres.append(nodo.module)
    return nombres


TODOS = [(capa, archivo) for capa in CAPAS for archivo in _archivos(capa)]


@pytest.mark.parametrize("capa,archivo", TODOS, ids=lambda x: x.name if hasattr(x, "name") else x)
def test_ninguna_capa_importa_de_una_capa_mas_externa(capa, archivo):
    posicion = CAPAS.index(capa)
    mas_externas = {f"avistamientos.{c}" for c in CAPAS[posicion + 1:]}

    prohibidos = [n for n in _imports(archivo)
                  if any(n == c or n.startswith(c + ".") for c in mas_externas)]

    assert prohibidos == [], f"{archivo.name} ({capa}) importa de una capa más externa: {prohibidos}"


@pytest.mark.parametrize("capa,archivo",
                         [(c, a) for c, a in TODOS if c in ("entities", "use_cases")],
                         ids=lambda x: x.name if hasattr(x, "name") else x)
def test_entities_y_use_cases_no_conocen_flask_ni_sqlite(capa, archivo):
    externos = [n for n in _imports(archivo) if n.split(".")[0] in ("flask", "sqlite3")]

    assert externos == [], f"{archivo.name} ({capa}) importa tecnología de afuera: {externos}"


@pytest.mark.parametrize("archivo", ["controlador.py", "presentador.py"])
def test_controlador_y_presentador_no_importan_flask_ni_sqlite(archivo):
    externos = [n for n in _imports(RAIZ / "interface_adapters" / archivo)
                if n.split(".")[0] in ("flask", "sqlite3")]

    assert externos == []
