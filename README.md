# 🚗 MotorRisk Analytics

API REST construida con **FastAPI** para la evaluación predictiva del riesgo de infracción grave en conductores de automoción. Diseñada para uso interno en aseguradoras de automóviles.

---

## Qué resuelve este proyecto

MotorRisk Analytics es un servicio de scoring predictivo que, dado el perfil básico de un conductor (sexo, experiencia, tramo de edad e historial de infracciones), estima la probabilidad de que cometa una infracción grave de tráfico. El modelo fue entrenado con datos reales de infracciones y se expone a través de una API REST con interfaz web integrada para facilitar su uso y demostración directa desde el navegador.

---

## Quickstart (arranque local)

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd API_Infracciones_Trafico
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Añadir el modelo

Coloca el archivo `model.pkl` en la raíz del proyecto (mismo directorio que `app.py`).

> ⚠️ `model.pkl` no está incluido en el repositorio. Solicítalo al equipo o genéralo ejecutando el notebook de entrenamiento.

### 5. Arrancar la aplicación

```bash
python app.py
```

La app estará disponible en `http://127.0.0.1:8000`.

---

## Demo en 90 segundos

Flujo recomendado para presentación o evaluación:

1. Abre `http://127.0.0.1:8000` → simulador individual con selects guiados.
2. Selecciona un perfil de alto riesgo (ej. conductor joven, novel, con varias infracciones) → resultado en rojo con probabilidad.
3. Cambia el perfil → observa el cambio de clase y probabilidad.
4. Navega a `/predict/batch` → evalúa múltiples conductores a la vez con JSON de ejemplo ya cargado.
5. Navega a `/model/info` → visualiza los metadatos y parámetros del modelo activo.
6. Abre `/docs` → Swagger UI generado automáticamente por FastAPI para probar los endpoints.

---

## Estructura del proyecto

```
.
├── app.py           # Aplicación principal FastAPI (API + interfaz web integrada)
├── model.pkl        # Modelo de ML serializado (no incluido en el repo)
├── requirements.txt # Dependencias del proyecto
├── README.md
└── Pruebas/         # Prototipos anteriores (histórico, no productivo)
    ├── app1.py      # Versión parcial Flask (legacy)
    ├── app2.py      # Versión experimental Flask (legacy, con duplicaciones)
    └── appflask.py  # Implementación completa Flask (legacy, reemplazada por FastAPI)
```

> La carpeta `Pruebas/` contiene versiones anteriores del proyecto en Flask, conservadas como histórico. El código productivo es únicamente `app.py`.

---

## Páginas interactivas

| URL | Descripción |
|-----|-------------|
| `/` | Landing con simulador individual y documentación API |
| `/model/info` | Metadatos y parámetros del modelo activo |
| `/predict/batch` | Formulario para predicción por lotes |
| `/docs` | Swagger UI (generado automáticamente por FastAPI) |
| `/redoc` | Documentación alternativa ReDoc |

Demo desplegada: [https://api-infracciones-trafico.onrender.com](https://api-infracciones-trafico.onrender.com)

---

## Endpoints API

### `POST /api/v1/predict` — Predicción individual

Envía los datos de un conductor en el body JSON y devuelve la predicción junto con la probabilidad estimada.

**Request:**
```json
{
  "sexo": 1,
  "novel": 0,
  "edad": 3,
  "num_infracciones": 2
}
```

**Response:**
```json
{
  "prediction": 1,
  "probability": 0.82,
  "missing": []
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{"sexo": 1, "novel": 0, "edad": 3, "num_infracciones": 2}'
```

---

### `GET /api/v1/predict` — Predicción individual por URL

Misma funcionalidad que el POST pero con parámetros en la URL. No devuelve probabilidad.

```
GET /api/v1/predict?sexo=1&novel=0&edad=3&num_infracciones=2
```

**Response:**
```json
{
  "prediction": 1,
  "missing": []
}
```

**Ejemplo con curl:**
```bash
curl "http://127.0.0.1:8000/api/v1/predict?sexo=1&novel=0&edad=3&num_infracciones=2"
```

---

### `GET /api/v1/model/info` — Metadatos del modelo

Devuelve los metadatos del modelo activo: tipo, features esperadas, clases y parámetros del estimador si están disponibles.

**Response:**
```json
{
  "model_type": "RandomForestClassifier",
  "features": ["SEXO", "NOVEL", "EDAD", "NUM_INFRACCIONES"],
  "feature_descriptions": {
    "SEXO": "Sexo del conductor (0 o 1)",
    "NOVEL": "Conductor novel (0 o 1)",
    "EDAD": "Tramo de edad codificado (1 a 6)",
    "NUM_INFRACCIONES": "Número de infracciones registradas"
  },
  "target": "Riesgo de infracción grave (0 = bajo, 1 = alto)",
  "supports_proba": true,
  "classes": [0, 1]
}
```

**Ejemplo con curl:**
```bash
curl "http://127.0.0.1:8000/api/v1/model/info"
```

---

### `POST /api/v1/predict/batch` — Predicción por lotes

Envía un array de conductores y recibe una predicción por cada registro. La validación la gestiona automáticamente Pydantic, devolviendo errores detallados por campo si algún valor está fuera de rango.

> ⚠️ Este endpoint solo acepta `POST`. Para usarlo desde el navegador, accede a `/predict/batch` o usa el Swagger en `/docs`.

**Request:**
```json
{
  "registros": [
    {"sexo": 1, "novel": 0, "edad": 3, "num_infracciones": 2},
    {"sexo": 0, "novel": 1, "edad": 1, "num_infracciones": 0}
  ]
}
```

**Response:**
```json
{
  "total": 2,
  "resultados": [
    {"index": 0, "prediction": 1, "probability": 0.82, "missing": []},
    {"index": 1, "prediction": 0, "probability": 0.11, "missing": []}
  ]
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predict/batch" \
     -H "Content-Type: application/json" \
     -d '{"registros": [{"sexo": 1, "novel": 0, "edad": 3, "num_infracciones": 2}, {"sexo": 0, "novel": 1, "edad": 1, "num_infracciones": 0}]}'
```

---

## Variables de entrada

| Variable | Tipo | Valores válidos | Descripción |
|----------|------|-----------------|-------------|
| `sexo` | int | `0` o `1` | `0` = Mujer · `1` = Hombre |
| `novel` | int | `0` o `1` | `0` = No novel · `1` = Conductor novel (carné ≤ 2 años) |
| `edad` | int | `1` a `6` | Tramo de edad codificado (ver tabla) |
| `num_infracciones` | int | ≥ 0 | Número de infracciones registradas |

### Tabla de tramos de edad

| Código | Rango aproximado |
|--------|-----------------|
| `1` | 18–24 años |
| `2` | 25–34 años |
| `3` | 35–44 años |
| `4` | 45–54 años |
| `5` | 55–64 años |
| `6` | 65 o más años |

Todos los campos son **obligatorios**. Si alguno falta o está fuera de rango, FastAPI devuelve automáticamente un error `422` con detalle campo a campo.

---

## Interpretación de la predicción

| Valor | Significado |
|-------|-------------|
| `0` | Riesgo **bajo** — el modelo no prevé infracción grave |
| `1` | Riesgo **alto** — el modelo clasifica el perfil como propenso a infracción grave |

El campo `probability` (disponible en POST individual y batch) indica la confianza del modelo en la clase de riesgo alto:

| Rango | Interpretación |
|-------|---------------|
| < 0.30 | Perfil claramente de bajo riesgo |
| 0.30 – 0.60 | Zona de incertidumbre |
| > 0.60 | Perfil claramente de alto riesgo |

---

## Errores comunes

### Error de validación (422) — valor fuera de rango

Ocurre cuando algún campo está fuera del rango permitido (ej. `edad = 10`):

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "edad"],
      "msg": "Input should be less than or equal to 6",
      "input": 10
    }
  ]
}
```

### Error de validación (422) — campo faltante

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "sexo"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

---

## Modelo ML

El modelo predice la probabilidad de infracción grave a partir de cuatro variables del conductor.

| Variable | Descripción |
|----------|-------------|
| `SEXO` | Sexo del conductor codificado (0/1) |
| `NOVEL` | Si es conductor novel (carné reciente) |
| `EDAD` | Tramo de edad del conductor (1–6) |
| `NUM_INFRACCIONES` | Historial de infracciones registradas |

**Salida:** clasificación binaria (`0` = bajo riesgo, `1` = alto riesgo) con probabilidad de pertenencia a la clase positiva.

**Limitaciones:** el modelo fue entrenado con datos históricos de infracciones de tráfico. Su precisión depende de la representatividad del conjunto de entrenamiento y no debe usarse como criterio único de decisión en contextos reales.

---

## Despliegue en Render

Para despliegue en producción (Render u otros servicios PaaS):

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

> ⚠️ Usar `0.0.0.0` (no `127.0.0.1`) para que el servidor acepte conexiones externas en entornos cloud.

Demo activa: [https://api-infracciones-trafico.onrender.com](https://api-infracciones-trafico.onrender.com)

---

## Tecnologías

| Herramienta | Uso |
|-------------|-----|
| FastAPI | Framework API REST |
| Pydantic | Validación automática de datos de entrada |
| scikit-learn | Modelo de clasificación ML |
| pandas / numpy | Procesamiento de datos |
| uvicorn | Servidor ASGI (desarrollo y producción) |
| gunicorn | Servidor de producción (workers) |

---

## Estado del repositorio

| Ruta | Estado |
|------|--------|
| `app.py` | ✅ Productivo — aplicación principal |
| `model.pkl` | ✅ Productivo — no incluido en el repo |
| `requirements.txt` | ✅ Productivo |
| `Pruebas/` | 🗂️ Histórico — prototipos Flask anteriores, no usados en producción |
