# 🚗 MotorRisk Analytics

API REST construida con FastAPI para la evaluación predictiva del riesgo de infracción grave en conductores. Diseñada para uso interno en aseguradoras de automóviles.

---

## Requisitos

- Python 3.8+
- pip

### Instalación de dependencias

```bash
pip install fastapi uvicorn pandas numpy scikit-learn
```

---

## Estructura del proyecto

```
.
├── app.py           # Aplicación principal FastAPI
├── model.pkl        # Modelo de ML serializado (no incluido en el repo)
└── README.md
```

> ⚠️ El archivo `model.pkl` debe estar en la misma carpeta que `app.py` para que la aplicación arranque correctamente.

---

## Arrancar la aplicación

```bash
python app.py
```

La app estará disponible en `http://127.0.0.1:8000`.  
Tambien está disponible [Aquí](https://api-infracciones-trafico.onrender.com) 

Para producción (Render u otros servicios):

```bash
uvicorn app:app --host 127.0.0.1 --port $PORT
```

---

## Páginas interactivas

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/` | Landing page con simulador individual |
| `http://127.0.0.1:8000/model/info` | Información visual del modelo activo |
| `http://127.0.0.1:8000/predict/batch` | Formulario para predicción por lotes |
| `http://127.0.0.1:8000/docs` | Swagger UI (generado automáticamente por FastAPI) |
| `http://127.0.0.1:8000/redoc` | Documentación alternativa ReDoc |

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

---

### `GET /api/v1/model/info` — Información del modelo

Devuelve los metadatos del modelo activo: tipo, features esperadas, clases y parámetros si están disponibles.

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

---

### `POST /api/v1/predict/batch` — Predicción por lotes

Envía un array de conductores y recibe una predicción por cada registro. La validación la gestiona automáticamente Pydantic, devolviendo errores detallados por campo si algún valor está fuera de rango.

> ⚠️ Este endpoint solo acepta `POST`. Para usarlo desde el navegador, accede a la página interactiva en `/predict/batch` o usa el Swagger en `/docs`.

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

---

## Variables de entrada

| Variable | Tipo | Valores válidos | Descripción |
|----------|------|-----------------|-------------|
| `sexo` | int | `0` o `1` | Sexo del conductor |
| `novel` | int | `0` o `1` | Indica si es conductor novel |
| `edad` | int | `1` a `6` | Tramo de edad codificado |
| `num_infracciones` | int | ≥ 0 | Número de infracciones registradas |

Todos los campos son **obligatorios**. Si alguno falta o está fuera de rango, FastAPI devuelve automáticamente un error `422` con detalle campo a campo.

---

## Interpretación de la predicción

| Valor | Significado |
|-------|-------------|
| `0` | Riesgo **bajo** — el modelo no prevé infracción grave |
| `1` | Riesgo **alto** — el modelo clasifica el perfil como propenso a infracción grave |

El campo `probability` (disponible en POST individual y batch) indica la confianza del modelo en la clase de riesgo alto. Cuanto más cercano a `1`, mayor certeza.

---
