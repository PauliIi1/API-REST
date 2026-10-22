import pytest
 
import app as api
 
DATOS = {"especie": "colibri", "lugar": "Chia", "fecha": "2026-09-20", "observador": "Paula"}
 
 
@pytest.fixture
def cliente(tmp_path, monkeypatch):
    # Cada prueba usa su propia base de datos temporal: son independientes
    # y no tocan avistamientos.db
    monkeypatch.setattr(api, "DB", str(tmp_path / "prueba.db"))
    api.crear_tabla()
    return api.app.test_client()
 
 
def registrar(cliente, **cambios):
    return cliente.post("/avistamientos", json={**DATOS, **cambios})
 
 
#poost
 
def test_post_valido_devuelve_201_y_el_avistamiento_creado(cliente):
    respuesta = registrar(cliente)
 
    assert respuesta.status_code == 201
    assert respuesta.is_json
    assert respuesta.get_json() == {"id": 1, **DATOS}
 
 
def test_post_valido_queda_guardado_y_se_puede_consultar(cliente):
    nuevo = registrar(cliente).get_json()
 
    respuesta = cliente.get(f"/avistamientos/{nuevo['id']}")
 
    assert respuesta.status_code == 200
    assert respuesta.get_json() == nuevo
 
 
def test_post_con_especie_muy_corta_devuelve_400_y_dice_el_campo(cliente):
    respuesta = registrar(cliente, especie="ab")
 
    assert respuesta.status_code == 400
    assert "especie" in respuesta.get_json()["error"]
 
 
def test_post_con_fecha_futura_devuelve_400_y_no_guarda(cliente):
    respuesta = registrar(cliente, fecha="2999-01-01")
 
    assert respuesta.status_code == 400
    assert "fecha" in respuesta.get_json()["error"]
    assert cliente.get("/avistamientos").get_json() == []
 
 
# get
 
def test_get_lista_sin_registros_devuelve_200_y_lista_vacia(cliente):
    respuesta = cliente.get("/avistamientos")
 
    assert respuesta.status_code == 200
    assert respuesta.get_json() == []
 
 
def test_get_lista_devuelve_los_avistamientos_registrados(cliente):
    registrar(cliente)
    registrar(cliente, especie="oso de anteojos", lugar="Chingaza")
 
    respuesta = cliente.get("/avistamientos")
 
    assert respuesta.status_code == 200
    assert [a["especie"] for a in respuesta.get_json()] == ["colibri", "oso de anteojos"]
 
 
def test_get_por_id_inexistente_devuelve_404(cliente):
    respuesta = cliente.get("/avistamientos/999")
 
    assert respuesta.status_code == 404
    assert respuesta.get_json() == {"error": "No existe"}
 
 
# put
 
def test_put_valido_devuelve_200_y_cambia_los_datos(cliente):
    nuevo = registrar(cliente).get_json()
 
    respuesta = cliente.put(f"/avistamientos/{nuevo['id']}", json={**DATOS, "lugar": "Bogota"})
 
    assert respuesta.status_code == 200
    assert respuesta.get_json()["lugar"] == "Bogota"
    assert cliente.get(f"/avistamientos/{nuevo['id']}").get_json()["lugar"] == "Bogota"
 
 
def test_put_invalido_devuelve_400_y_no_cambia_los_datos(cliente):
    nuevo = registrar(cliente).get_json()
 
    respuesta = cliente.put(f"/avistamientos/{nuevo['id']}", json={**DATOS, "observador": ""})
 
    assert respuesta.status_code == 400
    assert "observador" in respuesta.get_json()["error"]
    assert cliente.get(f"/avistamientos/{nuevo['id']}").get_json() == nuevo
 
 
def test_put_por_id_inexistente_devuelve_404(cliente):
    respuesta = cliente.put("/avistamientos/999", json=DATOS)
 
    assert respuesta.status_code == 404
 
 
# dili
 
def test_delete_devuelve_204_y_despues_el_get_devuelve_404(cliente):
    nuevo = registrar(cliente).get_json()
 
    respuesta = cliente.delete(f"/avistamientos/{nuevo['id']}")
 
    assert respuesta.status_code == 204
    assert cliente.get(f"/avistamientos/{nuevo['id']}").status_code == 404
 
 
def test_delete_por_id_inexistente_devuelve_404(cliente):
    respuesta = cliente.delete("/avistamientos/999")
 
    assert respuesta.status_code == 404
 
 
# resumen
 
def test_resumen_cuenta_los_avistamientos_por_especie(cliente):
    registrar(cliente)
    registrar(cliente, lugar="Bogota")
    registrar(cliente, especie="guacamaya")
 
    respuesta = cliente.get("/avistamientos/resumen")
 
    assert respuesta.status_code == 200
    assert sorted(respuesta.get_json(), key=lambda r: r["especie"]) == [
        {"especie": "colibri", "total": 2},
        {"especie": "guacamaya", "total": 1},
    ]