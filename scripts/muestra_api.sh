#!/usr/bin/env bash
# Muestra de que la API responde: hace una secuencia fija de peticiones
# contra un servidor que ya está corriendo y escribe el código HTTP y el cuerpo.
# Uso: bash scripts/muestra_api.sh [URL_BASE]
BASE="${1:-http://127.0.0.1:5000}"
JSON="Content-Type: application/json"

pedir() {
  echo "### $1 $2"
  if [ -n "$3" ]; then
    curl -s -X "$1" "$BASE$2" -H "$JSON" -d "$3" -w '[HTTP %{http_code}]\n'
  else
    curl -s -X "$1" "$BASE$2" -w '[HTTP %{http_code}]\n'
  fi
  echo
}

pedir POST   /avistamientos '{"especie":"colibri","lugar":"Chia","fecha":"2026-09-20","observador":"Paula"}'
pedir POST   /avistamientos '{"especie":"guacamaya","lugar":"Leticia","fecha":"2026-10-01","observador":"Paula"}'
pedir POST   /avistamientos '{"especie":"colibri","lugar":"Bogota","fecha":"2026-10-02","observador":"Paula"}'
pedir POST   /avistamientos '{"especie":"ab","lugar":"Chia","fecha":"2026-09-20","observador":"Paula"}'
pedir POST   /avistamientos '{"especie":"colibri","lugar":"Chia","fecha":"2999-01-01","observador":"Paula"}'
pedir GET    /avistamientos
pedir GET    /avistamientos/1
pedir GET    /avistamientos/999
pedir PUT    /avistamientos/1 '{"especie":"colibri","lugar":"Bogota","fecha":"2026-09-21","observador":"Paula"}'
pedir PUT    /avistamientos/1 '{"especie":"colibri","lugar":"Bogota","fecha":"2026-09-21","observador":""}'
pedir PUT    /avistamientos/999 '{"especie":"colibri","lugar":"Bogota","fecha":"2026-09-21","observador":"Paula"}'
pedir GET    /avistamientos/resumen
pedir DELETE /avistamientos/2
pedir DELETE /avistamientos/2
pedir GET    /avistamientos
