"""
Tests de sistema para la API REST del termostato.

Nivel    : Sistema (end-to-end contra servidor HTTP real)
Diferencia: Usa requests contra un proceso real, no el cliente Flask de test.

Prerequisitos:
    # Levantar el servidor en una terminal separada:
    python run.py

Ejecución:
    # Solo tests de sistema:
    pytest tests/test_sistema.py -v -m sistema

    # Con servidor en URL alternativa:
    TEST_BASE_URL=http://localhost:8080 pytest tests/test_sistema.py -v

    # Incluir en suite completa (el servidor debe estar corriendo):
    pytest -v
"""

import os
import time

import pytest
import requests

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:5050")
TIMEOUT = 5  # segundos por request


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get(ruta, **kwargs):
    return requests.get(f"{BASE_URL}{ruta}", timeout=TIMEOUT, **kwargs)


def _post(ruta, json_data, **kwargs):
    return requests.post(f"{BASE_URL}{ruta}", json=json_data, timeout=TIMEOUT, **kwargs)


def _servidor_disponible():
    try:
        requests.get(f"{BASE_URL}/comprueba/", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False


# ---------------------------------------------------------------------------
# Skip global si el servidor no está levantado
# ---------------------------------------------------------------------------

pytestmark = [
    pytest.mark.sistema,
    pytest.mark.skipif(
        not _servidor_disponible(),
        reason=f"Servidor no disponible en {BASE_URL}. Ejecutar: python run.py",
    ),
]


# ---------------------------------------------------------------------------
# TS-HC: Health Check
# ---------------------------------------------------------------------------

class TestHealthCheck:
    """TS-HC — Health check del servidor."""

    def test_hc01_responde_correctamente(self):
        """TS-HC-01: GET /comprueba/ retorna estructura completa con valores válidos."""
        resp = _get("/comprueba/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert isinstance(data["uptime_seconds"], int)
        assert data["uptime_seconds"] >= 0
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
        assert len(data["timestamp"]) > 0

    def test_hc01_content_type_json(self):
        """TS-HC-01: La respuesta es application/json."""
        resp = _get("/comprueba/")
        assert "application/json" in resp.headers["Content-Type"]

    def test_hc02_uptime_crece_entre_llamadas(self):
        """TS-HC-02: uptime_seconds es mayor en la segunda llamada."""
        t1 = _get("/comprueba/").json()["uptime_seconds"]
        time.sleep(2)
        t2 = _get("/comprueba/").json()["uptime_seconds"]
        assert t2 > t1


# ---------------------------------------------------------------------------
# TS-EST: Estado Completo
# ---------------------------------------------------------------------------

class TestEstadoCompleto:
    """TS-EST — GET /termostato/ retorna estado unificado."""

    def test_est01_todos_los_campos_presentes(self):
        """TS-EST-01: GET /termostato/ retorna los cinco campos esperados."""
        resp = _get("/termostato/")
        assert resp.status_code == 200
        data = resp.json()
        assert "temperatura_ambiente" in data
        assert "temperatura_deseada" in data
        assert "carga_bateria" in data
        assert "estado_climatizador" in data
        assert "indicador" in data

    def test_est02_refleja_cambios_previos(self):
        """TS-EST-02: GET /termostato/ refleja los últimos valores actualizados."""
        _post("/termostato/temperatura_ambiente/", {"ambiente": 33})
        _post("/termostato/temperatura_deseada/", {"deseada": 27})
        data = _get("/termostato/").json()
        assert data["temperatura_ambiente"] == 33
        assert data["temperatura_deseada"] == 27


# ---------------------------------------------------------------------------
# TS-TA: Temperatura Ambiente
# ---------------------------------------------------------------------------

class TestTemperaturaAmbiente:
    """TS-TA — Endpoint /termostato/temperatura_ambiente/."""

    def test_ta01_get_retorna_entero(self):
        """TS-TA-01: GET retorna temperatura_ambiente como entero."""
        resp = _get("/termostato/temperatura_ambiente/")
        assert resp.status_code == 200
        data = resp.json()
        assert "temperatura_ambiente" in data
        assert isinstance(data["temperatura_ambiente"], int)

    def test_ta02_post_actualiza_y_get_refleja(self):
        """TS-TA-02: POST actualiza valor y GET lo refleja."""
        resp = _post("/termostato/temperatura_ambiente/", {"ambiente": 30})
        assert resp.status_code == 201
        assert resp.json()["mensaje"] == "dato registrado"
        assert _get("/termostato/temperatura_ambiente/").json()["temperatura_ambiente"] == 30

    def test_ta03_limite_inferior(self):
        """TS-TA-03: POST acepta límite inferior (0) y GET lo confirma."""
        assert _post("/termostato/temperatura_ambiente/", {"ambiente": 0}).status_code == 201
        assert _get("/termostato/temperatura_ambiente/").json()["temperatura_ambiente"] == 0

    def test_ta04_limite_superior(self):
        """TS-TA-04: POST acepta límite superior (50) y GET lo confirma."""
        assert _post("/termostato/temperatura_ambiente/", {"ambiente": 50}).status_code == 201
        assert _get("/termostato/temperatura_ambiente/").json()["temperatura_ambiente"] == 50

    def test_ta05_string_numerico_convertido_a_int(self):
        """TS-TA-05: POST acepta string numérico '25' y lo convierte a int 25."""
        assert _post("/termostato/temperatura_ambiente/", {"ambiente": "25"}).status_code == 201
        valor = _get("/termostato/temperatura_ambiente/").json()["temperatura_ambiente"]
        assert valor == 25
        assert isinstance(valor, int)

    def test_ta06_float_truncado_a_int(self):
        """TS-TA-06: POST acepta 22.7 (float) y lo almacena como int 22."""
        assert _post("/termostato/temperatura_ambiente/", {"ambiente": 22.7}).status_code == 201
        valor = _get("/termostato/temperatura_ambiente/").json()["temperatura_ambiente"]
        assert valor == 22
        assert isinstance(valor, int)

    def test_ta07_rechaza_mayor_al_maximo(self):
        """TS-TA-07: POST rechaza valor 51 (> máximo 50) con 400."""
        assert _post("/termostato/temperatura_ambiente/", {"ambiente": 51}).status_code == 400

    def test_ta08_rechaza_menor_al_minimo(self):
        """TS-TA-08: POST rechaza valor -1 (< mínimo 0) con 400."""
        assert _post("/termostato/temperatura_ambiente/", {"ambiente": -1}).status_code == 400

    def test_ta09_rechaza_json_vacio(self):
        """TS-TA-09: POST con JSON vacío retorna 400."""
        assert _post("/termostato/temperatura_ambiente/", {}).status_code == 400

    def test_ta10_rechaza_campo_incorrecto(self):
        """TS-TA-10: POST con campo 'temperatura' (incorrecto) retorna 400."""
        assert _post("/termostato/temperatura_ambiente/", {"temperatura": 25}).status_code == 400

    def test_ta11_rechaza_content_type_form(self):
        """TS-TA-11: POST con Content-Type form-urlencoded retorna 415."""
        resp = requests.post(
            f"{BASE_URL}/termostato/temperatura_ambiente/",
            data="ambiente=25",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=TIMEOUT,
        )
        assert resp.status_code == 415


# ---------------------------------------------------------------------------
# TS-TD: Temperatura Deseada
# ---------------------------------------------------------------------------

class TestTemperaturaDeseada:
    """TS-TD — Endpoint /termostato/temperatura_deseada/."""

    def test_td01_get_retorna_valor(self):
        """TS-TD-01: GET retorna temperatura_deseada."""
        resp = _get("/termostato/temperatura_deseada/")
        assert resp.status_code == 200
        assert "temperatura_deseada" in resp.json()

    def test_td02_post_actualiza_y_get_refleja(self):
        """TS-TD-02: POST actualiza valor y GET lo refleja."""
        assert _post("/termostato/temperatura_deseada/", {"deseada": 20}).status_code == 201
        assert _get("/termostato/temperatura_deseada/").json()["temperatura_deseada"] == 20

    def test_td03_limite_inferior(self):
        """TS-TD-03: POST acepta límite inferior (15) y GET lo confirma."""
        assert _post("/termostato/temperatura_deseada/", {"deseada": 15}).status_code == 201
        assert _get("/termostato/temperatura_deseada/").json()["temperatura_deseada"] == 15

    def test_td04_limite_superior(self):
        """TS-TD-04: POST acepta límite superior (30) y GET lo confirma."""
        assert _post("/termostato/temperatura_deseada/", {"deseada": 30}).status_code == 201
        assert _get("/termostato/temperatura_deseada/").json()["temperatura_deseada"] == 30

    def test_td05_rechaza_mayor_al_maximo(self):
        """TS-TD-05: POST rechaza valor 31 (> máximo 30) con 400."""
        assert _post("/termostato/temperatura_deseada/", {"deseada": 31}).status_code == 400

    def test_td06_rechaza_menor_al_minimo(self):
        """TS-TD-06: POST rechaza valor 14 (< mínimo 15) con 400."""
        assert _post("/termostato/temperatura_deseada/", {"deseada": 14}).status_code == 400


# ---------------------------------------------------------------------------
# TS-BA: Batería
# ---------------------------------------------------------------------------

class TestBateria:
    """TS-BA — Endpoint /termostato/bateria/."""

    def test_ba01_get_retorna_float(self):
        """TS-BA-01: GET retorna carga_bateria como float."""
        resp = _get("/termostato/bateria/")
        assert resp.status_code == 200
        data = resp.json()
        assert "carga_bateria" in data
        assert isinstance(data["carga_bateria"], float)

    def test_ba02_post_actualiza_y_get_refleja(self):
        """TS-BA-02: POST actualiza valor y GET lo refleja."""
        assert _post("/termostato/bateria/", {"bateria": 3.5}).status_code == 201
        assert _get("/termostato/bateria/").json()["carga_bateria"] == 3.5

    def test_ba03_limite_inferior(self):
        """TS-BA-03: POST acepta límite inferior (0.0) y GET lo confirma."""
        assert _post("/termostato/bateria/", {"bateria": 0.0}).status_code == 201
        assert _get("/termostato/bateria/").json()["carga_bateria"] == 0.0

    def test_ba04_limite_superior(self):
        """TS-BA-04: POST acepta límite superior (5.0) y GET lo confirma."""
        assert _post("/termostato/bateria/", {"bateria": 5.0}).status_code == 201
        assert _get("/termostato/bateria/").json()["carga_bateria"] == 5.0

    def test_ba05_redondeo_dos_decimales(self):
        """TS-BA-05: POST redondea 3.14159 a 3.14 (2 decimales)."""
        assert _post("/termostato/bateria/", {"bateria": 3.14159}).status_code == 201
        assert _get("/termostato/bateria/").json()["carga_bateria"] == 3.14

    def test_ba06_entero_convertido_a_float(self):
        """TS-BA-06: POST acepta entero (3) y lo retorna como float (3.0)."""
        assert _post("/termostato/bateria/", {"bateria": 3}).status_code == 201
        valor = _get("/termostato/bateria/").json()["carga_bateria"]
        assert valor == 3.0
        assert isinstance(valor, float)

    def test_ba07_rechaza_mayor_al_maximo(self):
        """TS-BA-07: POST rechaza valor 5.1 (> máximo 5.0) con 400."""
        assert _post("/termostato/bateria/", {"bateria": 5.1}).status_code == 400

    def test_ba08_rechaza_menor_al_minimo(self):
        """TS-BA-08: POST rechaza valor -0.1 (< mínimo 0.0) con 400."""
        assert _post("/termostato/bateria/", {"bateria": -0.1}).status_code == 400


# ---------------------------------------------------------------------------
# TS-CL: Estado Climatizador
# ---------------------------------------------------------------------------

class TestEstadoClimatizador:
    """TS-CL — Endpoint /termostato/estado_climatizador/."""

    def test_cl01_get_retorna_valor(self):
        """TS-CL-01: GET retorna estado_climatizador como string."""
        resp = _get("/termostato/estado_climatizador/")
        assert resp.status_code == 200
        data = resp.json()
        assert "estado_climatizador" in data
        assert isinstance(data["estado_climatizador"], str)

    def test_cl02_post_encendido(self):
        """TS-CL-02: POST acepta 'encendido' y GET lo confirma."""
        assert _post("/termostato/estado_climatizador/", {"climatizador": "encendido"}).status_code == 201
        assert _get("/termostato/estado_climatizador/").json()["estado_climatizador"] == "encendido"

    def test_cl03_post_enfriando(self):
        """TS-CL-03: POST acepta 'enfriando' y GET lo confirma."""
        assert _post("/termostato/estado_climatizador/", {"climatizador": "enfriando"}).status_code == 201
        assert _get("/termostato/estado_climatizador/").json()["estado_climatizador"] == "enfriando"

    def test_cl04_post_calentando(self):
        """TS-CL-04: POST acepta 'calentando' y GET lo confirma."""
        assert _post("/termostato/estado_climatizador/", {"climatizador": "calentando"}).status_code == 201
        assert _get("/termostato/estado_climatizador/").json()["estado_climatizador"] == "calentando"

    def test_cl05_normaliza_mayusculas(self):
        """TS-CL-05: POST acepta 'ENCENDIDO' y lo almacena como 'encendido'."""
        assert _post("/termostato/estado_climatizador/", {"climatizador": "ENCENDIDO"}).status_code == 201
        assert _get("/termostato/estado_climatizador/").json()["estado_climatizador"] == "encendido"

    def test_cl06_normaliza_espacios(self):
        """TS-CL-06: POST acepta '  apagado  ' y elimina los espacios."""
        assert _post("/termostato/estado_climatizador/", {"climatizador": "  apagado  "}).status_code == 201
        assert _get("/termostato/estado_climatizador/").json()["estado_climatizador"] == "apagado"

    def test_cl07_rechaza_estado_invalido(self):
        """TS-CL-07: POST rechaza 'ventilando' (no reconocido) con 400."""
        assert _post("/termostato/estado_climatizador/", {"climatizador": "ventilando"}).status_code == 400

    def test_cl08_rechaza_estado_vacio(self):
        """TS-CL-08: POST rechaza string vacío con 400."""
        assert _post("/termostato/estado_climatizador/", {"climatizador": ""}).status_code == 400


# ---------------------------------------------------------------------------
# TS-IN: Indicador de Batería
# ---------------------------------------------------------------------------

class TestIndicador:
    """TS-IN — Endpoint /termostato/indicador/ (solo lectura)."""

    def test_in01_get_con_bateria_alta_es_normal(self):
        """TS-IN-01: Con batería > 3.5 el indicador es NORMAL."""
        _post("/termostato/bateria/", {"bateria": 5.0})
        resp = _get("/termostato/indicador/")
        assert resp.status_code == 200
        assert resp.json()["indicador"] == "NORMAL"

    def test_in02_bateria_media_es_bajo(self):
        """TS-IN-02: Con batería entre 2.5 y 3.5 el indicador es BAJO."""
        _post("/termostato/bateria/", {"bateria": 3.0})
        assert _get("/termostato/indicador/").json()["indicador"] == "BAJO"

    def test_in03_bateria_baja_es_critico(self):
        """TS-IN-03: Con batería < 2.5 el indicador es CRITICO."""
        _post("/termostato/bateria/", {"bateria": 1.0})
        assert _get("/termostato/indicador/").json()["indicador"] == "CRITICO"

    def test_in04_umbral_35_justo_encima_es_normal(self):
        """TS-IN-04: Batería en 3.51 (justo encima del umbral) da NORMAL."""
        _post("/termostato/bateria/", {"bateria": 3.51})
        assert _get("/termostato/indicador/").json()["indicador"] == "NORMAL"

    def test_in05_umbral_exacto_35_da_bajo(self):
        """TS-IN-05: Batería en 3.5 exacto da BAJO (condición es carga > 3.5)."""
        _post("/termostato/bateria/", {"bateria": 3.5})
        assert _get("/termostato/indicador/").json()["indicador"] == "BAJO"

    def test_in05b_umbral_exacto_25_da_bajo(self):
        """TS-IN-05b: Batería en 2.5 exacto da BAJO (condición es carga >= 2.5)."""
        _post("/termostato/bateria/", {"bateria": 2.5})
        assert _get("/termostato/indicador/").json()["indicador"] == "BAJO"

    def test_in06_post_retorna_405(self):
        """TS-IN-06: POST en /indicador/ retorna 405 Method Not Allowed."""
        resp = _post("/termostato/indicador/", {"indicador": "NORMAL"})
        assert resp.status_code == 405


# ---------------------------------------------------------------------------
# TS-HI: Historial de Temperaturas
# ---------------------------------------------------------------------------

class TestHistorial:
    """TS-HI — Endpoint /termostato/historial/."""

    def test_hi01_estructura_correcta(self):
        """TS-HI-01: GET retorna 'historial' (lista) y 'total' (entero)."""
        resp = _get("/termostato/historial/")
        assert resp.status_code == 200
        data = resp.json()
        assert "historial" in data
        assert "total" in data
        assert isinstance(data["historial"], list)
        assert isinstance(data["total"], int)
        assert data["total"] >= 0

    def test_hi02_registro_tiene_campos_correctos(self):
        """TS-HI-02: Cada entrada del historial tiene 'temperatura' y 'timestamp'.

        El historial se retorna newest-first, por lo que el POST recién hecho
        queda en registros[0].
        """
        _post("/termostato/temperatura_ambiente/", {"ambiente": 25})
        registros = _get("/termostato/historial/").json()["historial"]
        assert len(registros) > 0
        mas_reciente = registros[0]  # newest-first: el último POST está en [0]
        assert "temperatura" in mas_reciente
        assert "timestamp" in mas_reciente
        assert mas_reciente["temperatura"] == 25
        assert isinstance(mas_reciente["timestamp"], str)
        assert len(mas_reciente["timestamp"]) > 0

    def test_hi03_post_temperatura_ambiente_genera_entrada(self):
        """TS-HI-03: Cada POST a temperatura_ambiente incrementa total en 1 por cambio.

        El historial se retorna en orden newest-first (agregar() inserta en índice 0),
        por lo que el POST más reciente está en historial[0].
        """
        total_inicial = _get("/termostato/historial/").json()["total"]
        _post("/termostato/temperatura_ambiente/", {"ambiente": 22})
        _post("/termostato/temperatura_ambiente/", {"ambiente": 28})
        data = _get("/termostato/historial/").json()
        assert data["total"] == total_inicial + 2
        # newest-first: historial[0]=28 (último POST), historial[1]=22 (penúltimo POST)
        recientes = data["historial"][:2]
        assert recientes[0]["temperatura"] == 28
        assert recientes[1]["temperatura"] == 22

    def test_hi04_otros_endpoints_no_generan_historial(self):
        """TS-HI-04: POSTs a batería, deseada y climatizador no añaden entradas."""
        total_inicial = _get("/termostato/historial/").json()["total"]
        _post("/termostato/temperatura_deseada/", {"deseada": 20})
        _post("/termostato/bateria/", {"bateria": 3.0})
        _post("/termostato/estado_climatizador/", {"climatizador": "encendido"})
        assert _get("/termostato/historial/").json()["total"] == total_inicial

    def test_hi05_limite_restringe_registros_retornados(self):
        """TS-HI-05: ?limite=3 retorna exactamente 3 registros (dado que hay >= 3)."""
        for t in [10, 12, 14, 16, 18, 20]:
            _post("/termostato/temperatura_ambiente/", {"ambiente": t})
        data = _get("/termostato/historial/?limite=3").json()
        assert len(data["historial"]) == 3

    def test_hi06_sin_limite_longitud_igual_a_total(self):
        """TS-HI-06: Sin parámetro ?limite= la longitud de historial == total."""
        data = _get("/termostato/historial/").json()
        assert len(data["historial"]) == data["total"]


# ---------------------------------------------------------------------------
# TS-ERR: Manejo de Errores
# ---------------------------------------------------------------------------

class TestErrores:
    """TS-ERR — Manejo de errores HTTP."""

    def test_err01_ruta_inexistente_retorna_404(self):
        """TS-ERR-01: Ruta no registrada retorna 404."""
        assert _get("/termostato/inexistente/").status_code == 404

    def test_err02_respuesta_de_error_sigue_esquema(self):
        """TS-ERR-02: Cuerpo de error tiene campos 'error.codigo' y 'error.mensaje'."""
        resp = _post("/termostato/temperatura_ambiente/", {"ambiente": 99})
        assert resp.status_code == 400
        data = resp.json()
        assert "error" in data
        error = data["error"]
        assert "codigo" in error
        assert "mensaje" in error
        assert error["codigo"] == 400
        assert isinstance(error["mensaje"], str)
        assert len(error["mensaje"]) > 0

    def test_err03_post_sin_body_retorna_error(self):
        """TS-ERR-03: POST sin body retorna 400 o 415 (no 500)."""
        resp = requests.post(
            f"{BASE_URL}/termostato/temperatura_ambiente/",
            timeout=TIMEOUT,
        )
        assert resp.status_code in (400, 415)


# ---------------------------------------------------------------------------
# TS-F: Flujos End-to-End
# ---------------------------------------------------------------------------

class TestFlujos:
    """TS-F — Flujos de negocio completos."""

    def test_f01_ciclo_completo_actualizacion_y_lectura(self):
        """TS-F01: Actualizar todos los campos y verificar el estado unificado."""
        _post("/termostato/temperatura_ambiente/", {"ambiente": 18})
        _post("/termostato/temperatura_deseada/", {"deseada": 22})
        _post("/termostato/bateria/", {"bateria": 4.2})
        _post("/termostato/estado_climatizador/", {"climatizador": "calentando"})

        data = _get("/termostato/").json()
        assert data["temperatura_ambiente"] == 18
        assert data["temperatura_deseada"] == 22
        assert data["carga_bateria"] == 4.2
        assert data["estado_climatizador"] == "calentando"
        assert data["indicador"] == "NORMAL"  # 4.2 > 3.5

    def test_f02_degradacion_bateria_actualiza_indicador(self):
        """TS-F02: La degradación progresiva de batería cambia el indicador en cada paso."""
        _post("/termostato/bateria/", {"bateria": 5.0})
        assert _get("/termostato/indicador/").json()["indicador"] == "NORMAL"

        _post("/termostato/bateria/", {"bateria": 3.0})
        assert _get("/termostato/indicador/").json()["indicador"] == "BAJO"

        _post("/termostato/bateria/", {"bateria": 1.5})
        assert _get("/termostato/indicador/").json()["indicador"] == "CRITICO"

        # Recuperación
        _post("/termostato/bateria/", {"bateria": 4.0})
        assert _get("/termostato/indicador/").json()["indicador"] == "NORMAL"

    def test_f03_historial_registra_cambios_en_orden_newest_first(self):
        """TS-F03: Los cambios de temperatura se reflejan en historial newest-first.

        El repositorio inserta en índice 0, por lo que el último POST queda en
        historial[0]. Los N cambios más recientes están en historial[:N].
        """
        total_inicial = _get("/termostato/historial/").json()["total"]
        temperaturas = [15, 20, 25, 30, 35]
        for t in temperaturas:
            _post("/termostato/temperatura_ambiente/", {"ambiente": t})

        data = _get("/termostato/historial/").json()
        assert data["total"] == total_inicial + len(temperaturas)
        # newest-first: el último enviado (35) está en historial[0]
        recientes = data["historial"][:len(temperaturas)]
        assert [r["temperatura"] for r in recientes] == list(reversed(temperaturas))

    def test_f04_rechazo_no_modifica_estado_ni_historial(self):
        """TS-F04: Un POST rechazado no altera el valor actual ni el historial."""
        valor_actual = _get("/termostato/temperatura_ambiente/").json()["temperatura_ambiente"]
        total_inicial = _get("/termostato/historial/").json()["total"]

        _post("/termostato/temperatura_ambiente/", {"ambiente": 99})  # fuera de rango

        assert _get("/termostato/temperatura_ambiente/").json()["temperatura_ambiente"] == valor_actual
        assert _get("/termostato/historial/").json()["total"] == total_inicial

    def test_f05_ciclo_completo_estados_climatizador(self):
        """TS-F05: Todas las transiciones de estado del climatizador son aceptadas."""
        for estado in ["apagado", "encendido", "calentando", "enfriando", "apagado"]:
            resp = _post("/termostato/estado_climatizador/", {"climatizador": estado})
            assert resp.status_code == 201
            assert _get("/termostato/estado_climatizador/").json()["estado_climatizador"] == estado


# ---------------------------------------------------------------------------
# TS-BE: Casos de Borde
# ---------------------------------------------------------------------------

class TestCasosBorde:
    """TS-BE — Valores límite y comportamientos no estándar."""

    def test_be01_bateria_con_muchos_decimales_se_redondea(self):
        """TS-BE-01: 3.999999 se redondea a 4.0 (round a 2 decimales)."""
        _post("/termostato/bateria/", {"bateria": 3.999999})
        assert _get("/termostato/bateria/").json()["carga_bateria"] == 4.0

    def test_be02_bateria_negativa_minima_rechazada(self):
        """TS-BE-02: Batería -0.01 es rechazada (por debajo del mínimo 0.0)."""
        assert _post("/termostato/bateria/", {"bateria": -0.01}).status_code == 400

    def test_be03_temperatura_deseada_acepta_string_numerico(self):
        """TS-BE-03: temperatura_deseada acepta '20' (string) y lo convierte a int."""
        assert _post("/termostato/temperatura_deseada/", {"deseada": "20"}).status_code == 201
        assert _get("/termostato/temperatura_deseada/").json()["temperatura_deseada"] == 20

    def test_be04_historial_limite_cero(self):
        """TS-BE-04: ?limite=0 retorna una lista (puede ser vacía o comportamiento definido)."""
        resp = _get("/termostato/historial/?limite=0")
        assert resp.status_code == 200
        assert isinstance(resp.json()["historial"], list)

    def test_be05_tipos_de_datos_en_estado_completo(self):
        """TS-BE-05: Los tipos de datos en GET /termostato/ son los esperados."""
        _post("/termostato/temperatura_ambiente/", {"ambiente": 25})
        _post("/termostato/temperatura_deseada/", {"deseada": 22})
        _post("/termostato/bateria/", {"bateria": 3.5})
        _post("/termostato/estado_climatizador/", {"climatizador": "apagado"})

        data = _get("/termostato/").json()
        assert isinstance(data["temperatura_ambiente"], int)
        assert isinstance(data["temperatura_deseada"], int)
        assert isinstance(data["carga_bateria"], float)
        assert isinstance(data["estado_climatizador"], str)
        assert isinstance(data["indicador"], str)
        assert data["indicador"] in {"NORMAL", "BAJO", "CRITICO"}
