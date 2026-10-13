# API REST de avistamientos
Paula Buitrago, Ingeniería de Software 2 (Sesión 17). Hecha con Python, Flask y SQLite. Probada en un PC con Windows.

# Instalación y ejecución
1. Requisitos: Python 3.11 o superior.
2. Clonar el repositorio y entrar a la carpeta:
```
   git clone https://github.com/PauliIi1/API-REST.git
   cd API-REST
```
3. Crear y activar el entorno virtual:
   - Windows: `python -m venv venv` y luego `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` y luego `source venv/bin/activate`
   - Si PowerShell bloquea la activación, ejecutar antes: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Ejecutar (desde dentro de la carpeta del proyecto): `python app.py`

La API queda en http://127.0.0.1:5000.
La base de datos SQLite `avistamientos.db` se crea sola al iniciar.

# Endpoints y ejemplos
Ejecutar los ejemplos en este orden (con la base de datos vacía, el primer registro tiene id 1). Se necesita una segunda terminal con la API corriendo.

Seguir solo una de las dos secciones (Windows o curl). Si se repiten, cambiar el `1` de las URL por el id que devuelva el registro.

## En Windows (PowerShell)
En PowerShell `curl` no funciona con estos ejemplos, por eso se usaron estos comandos:

1. Registrar (201, o 400 si faltan datos):
```powershell
$cuerpo = '{"especie":"Copetón","lugar":"Chia","fecha":"2026-09-20","observador":"Paula"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/avistamientos" -Method Post -ContentType "application/json" -Body ([System.Text.Encoding]::UTF8.GetBytes($cuerpo))
```

2. Listar todos (200):
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/avistamientos" -Method Get
```

3. Ver uno (200, o 404 si no existe):
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/avistamientos/1" -Method Get
```

4. Actualizar (200, 400 o 404):
```powershell
$nuevo = '{"especie":"Copetón","lugar":"Bogota","fecha":"2026-09-21","observador":"Paula"}'
Invoke-RestMethod -Uri "http://127.0.0.1:5000/avistamientos/1" -Method Put -ContentType "application/json" -Body ([System.Text.Encoding]::UTF8.GetBytes($nuevo))
```

5. Resumen por especie, bonus (200):
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/avistamientos/resumen" -Method Get
```

6. Eliminar (204, o 404 si no existe):
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/avistamientos/1" -Method Delete
```

En PowerShell, los errores 400 y 404 aparecen en rojo con el mensaje de error: es lo esperado.

## Con curl (Mac, Linux o Git Bash)

1. Registrar (201, o 400 si faltan datos):
```bash
curl -i -X POST http://127.0.0.1:5000/avistamientos -H "Content-Type: application/json" -d '{"especie":"colibri","lugar":"Chia","fecha":"2026-09-20","observador":"Paula"}'
```

2. Listar todos (200):
```bash
curl -i http://127.0.0.1:5000/avistamientos
```

3. Ver uno (200, o 404 si no existe):
```bash
curl -i http://127.0.0.1:5000/avistamientos/1
```

4. Actualizar (200, 400 o 404):
```bash
curl -i -X PUT http://127.0.0.1:5000/avistamientos/1 -H "Content-Type: application/json" -d '{"especie":"colibri","lugar":"Bogota","fecha":"2026-09-21","observador":"Paula"}'
```

5. Resumen por especie, bonus (200):
```bash
curl -i http://127.0.0.1:5000/avistamientos/resumen
```

6. Eliminar (204, o 404 si no existe):
```bash
curl -i -X DELETE http://127.0.0.1:5000/avistamientos/1
```

# Uso de IA
Usé Claude (modelo Sonnet 5.5) como herramienta de apoyo y consulta para desarrollar esta API.