from datetime import date
 
from validador import ValidadorDeAvistamiento, RelojFijo
 
HOY = date(2026, 10, 21)  #hoy es esta fecha
 
 
def crear_validador():
    return ValidadorDeAvistamiento(RelojFijo(HOY))
 
 
def datos_validos(**cambios):
    datos = {"especie": "colibri", "lugar": "Chia", "fecha": "2026-09-20", "observador": "Paula"}
    datos.update(cambios)
    return datos
 
 
# :D
 
def test_avistamiento_completo_y_correcto_es_valido():
    validador = crear_validador()
    resultado = validador.validar(datos_validos())
    assert resultado is None
 
 
# ---------- especie: límites 2 / 3 / 50 / 51 ----------
 
def test_especie_vacia_es_invalida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(especie=""))
    assert "especie" in resultado
 
 
def test_especie_de_2_caracteres_es_invalida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(especie="ab"))
    assert "especie" in resultado
 
 
def test_especie_de_3_caracteres_es_valida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(especie="abc"))
    assert resultado is None
 
 
def test_especie_de_50_caracteres_es_valida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(especie="a" * 50))
    assert resultado is None
 
 
def test_especie_de_51_caracteres_es_invalida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(especie="a" * 51))
    assert "especie" in resultado
 
 
# fecha
 
def test_fecha_de_hoy_es_valida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(fecha="2026-10-21"))
    assert resultado is None
 
 
def test_fecha_de_manana_es_invalida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(fecha="2026-10-22"))
    assert "fecha" in resultado
 
 
def test_fecha_con_formato_dia_mes_anio_es_invalida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(fecha="20/09/2026"))
    assert "fecha" in resultado
 
 
def test_fecha_sin_ceros_a_la_izquierda_es_invalida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(fecha="2026-9-5"))
    assert "fecha" in resultado
 
 
def test_fecha_que_no_existe_es_invalida():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(fecha="2026-02-30"))
    assert "fecha" in resultado
 
 
# 
 
def test_lugar_vacio_es_invalido():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(lugar=""))
    assert "lugar" in resultado
 
 
def test_observador_con_solo_espacios_es_invalido():
    validador = crear_validador()
    resultado = validador.validar(datos_validos(observador="   "))
    assert "observador" in resultado
 
 
def test_falta_un_campo_es_invalido():
    validador = crear_validador()
    datos = datos_validos()
    del datos["especie"]
    resultado = validador.validar(datos)
    assert "especie" in resultado
 
 
def test_cuerpo_que_no_es_un_objeto_es_invalido():
    validador = crear_validador()
    resultado = validador.validar(["colibri"])
    assert resultado is not None