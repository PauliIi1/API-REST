"""Círculo 3 (Interface Adapters): el adaptador que habla SQLite.

Implementa el puerto RepositorioDeAvistamientos. Todo el SQL del proyecto
vive aquí: ninguna capa de adentro sabe que existe una base de datos.
Convierte entre filas de SQLite y la entidad Avistamiento.
"""
import sqlite3

from avistamientos.entities.avistamiento import Avistamiento
from avistamientos.use_cases.modelos import ConteoPorEspecie
from avistamientos.use_cases.puertos import RepositorioDeAvistamientos


class RepositorioSqlite(RepositorioDeAvistamientos):
    def __init__(self, ruta_db):
        self._ruta_db = ruta_db

    def _conectar(self):
        con = sqlite3.connect(self._ruta_db)
        con.row_factory = sqlite3.Row
        return con

    @staticmethod
    def _a_entidad(fila):
        return Avistamiento(
            id=fila["id"],
            especie=fila["especie"],
            lugar=fila["lugar"],
            fecha=fila["fecha"],
            observador=fila["observador"],
        )

    def crear_tabla(self):
        con = self._conectar()
        con.execute("""CREATE TABLE IF NOT EXISTS avistamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            especie TEXT NOT NULL,
            lugar TEXT NOT NULL,
            fecha TEXT NOT NULL,
            observador TEXT NOT NULL)""")
        con.commit()
        con.close()

    def listar(self):
        con = self._conectar()
        filas = con.execute("SELECT * FROM avistamientos").fetchall()
        con.close()
        return [self._a_entidad(f) for f in filas]

    def buscar(self, id):
        con = self._conectar()
        fila = con.execute("SELECT * FROM avistamientos WHERE id = ?", (id,)).fetchone()
        con.close()
        return None if fila is None else self._a_entidad(fila)

    def guardar(self, avistamiento):
        con = self._conectar()
        cur = con.execute(
            "INSERT INTO avistamientos (especie, lugar, fecha, observador) VALUES (?, ?, ?, ?)",
            (avistamiento.especie, avistamiento.lugar, avistamiento.fecha, avistamiento.observador))
        con.commit()
        nuevo_id = cur.lastrowid
        con.close()
        return Avistamiento(nuevo_id, avistamiento.especie, avistamiento.lugar,
                            avistamiento.fecha, avistamiento.observador)

    def actualizar(self, avistamiento):
        con = self._conectar()
        con.execute(
            "UPDATE avistamientos SET especie=?, lugar=?, fecha=?, observador=? WHERE id=?",
            (avistamiento.especie, avistamiento.lugar, avistamiento.fecha,
             avistamiento.observador, avistamiento.id))
        con.commit()
        con.close()

    def eliminar(self, id):
        con = self._conectar()
        con.execute("DELETE FROM avistamientos WHERE id = ?", (id,))
        con.commit()
        con.close()

    def contar_por_especie(self):
        con = self._conectar()
        filas = con.execute(
            "SELECT especie, COUNT(*) AS total FROM avistamientos GROUP BY especie").fetchall()
        con.close()
        return [ConteoPorEspecie(f["especie"], f["total"]) for f in filas]
