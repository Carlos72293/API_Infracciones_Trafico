from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import pickle
import pandas as pd
import numpy as np
import uvicorn

os.chdir(os.path.dirname(__file__))

app = FastAPI(
    title="MotorRisk Analytics",
    description="Plataforma de evaluación predictiva para aseguradoras de automóviles",
    version="1.0.0"
)

# Cargar el modelo
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)



# MODELOS PYDANTIC

class ConductorInput(BaseModel):
    sexo: int = Field(..., ge=0, le=1, description="Sexo del conductor · 0 = Mujer, 1 = Hombre")
    novel: int = Field(..., ge=0, le=1, description="Conductor novel · 0 = No (experimentado), 1 = Sí (carné ≤ 2 años)")
    edad: int = Field(..., ge=1, le=6, description="Tramo de edad · 1=18-24, 2=25-34, 3=35-44, 4=45-54, 5=55-64, 6=65+")
    num_infracciones: int = Field(..., ge=0, description="Número de infracciones registradas (entero ≥ 0)")

class BatchInput(BaseModel):
    registros: List[ConductorInput] = Field(..., min_length=1, description="Lista de conductores a evaluar")


# HELPERS

def run_prediction(sexo, novel, edad, num_infracciones, include_proba=False):
    input_data = pd.DataFrame({
        'SEXO': [sexo], 'NOVEL': [novel],
        'EDAD': [edad], 'NUM_INFRACCIONES': [num_infracciones]
    })
    prediction = model.predict(input_data)
    result = {"prediction": int(prediction[0]), "missing": []}
    if include_proba:
        try:
            prob = model.predict_proba(input_data)[0][1]
            result["probability"] = float(prob)
        except Exception:
            result["probability"] = None
    return result



# LANDING PAGE

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def hello():
    return """
    <html>
        <head>
            <title>MotorRisk Analytics</title>
            <style>
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    background-color: #f4f6f9;
                    color: #24324a;
                }
                header {
                    background: linear-gradient(135deg, #172a45, #223b63);
                    color: white;
                    padding: 28px 40px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.12);
                }
                header h1 { margin: 0; font-size: 32px; }
                header p { margin: 8px 0 0 0; opacity: 0.92; font-size: 16px; }
                .container {
                    max-width: 1180px;
                    margin: 30px auto;
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 24px;
                    padding: 0 20px;
                }
                .card {
                    background: white;
                    padding: 24px;
                    border-radius: 16px;
                    box-shadow: 0 8px 24px rgba(20, 35, 60, 0.08);
                    border: 1px solid #e8edf5;
                }
                .card.full-width { grid-column: 1 / -1; }
                h2 { color: #172a45; margin-top: 0; margin-bottom: 18px; font-size: 24px; }
                h3 { color: #223b63; margin-top: 22px; margin-bottom: 10px; font-size: 18px; }
                h4 { margin-top: 16px; margin-bottom: 8px; font-size: 15px; color: #304563; }
                label { font-weight: 600; display: block; margin-bottom: 6px; margin-top: 12px; }
                input, textarea, select {
                    width: 100%;
                    padding: 12px;
                    margin: 0 0 8px 0;
                    border-radius: 8px;
                    border: 1px solid #cfd8e6;
                    box-sizing: border-box;
                    font-size: 14px;
                    background-color: #fbfcfe;
                    font-family: inherit;
                }
                input:focus, textarea:focus, select:focus {
                    outline: none;
                    border-color: #305f9b;
                    box-shadow: 0 0 0 3px rgba(48, 95, 155, 0.12);
                }
                button {
                    width: 100%;
                    padding: 13px;
                    background: linear-gradient(135deg, #1c3d68, #29558d);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 16px;
                    transition: transform 0.15s ease, box-shadow 0.15s ease;
                }
                button:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 6px 16px rgba(28, 61, 104, 0.22);
                }
                .result-box {
                    padding: 16px;
                    border-radius: 10px;
                    margin-top: 18px;
                    font-weight: 700;
                    font-size: 15px;
                }
                .low-risk  { background-color: #e9f8ef; color: #1f7a3d; border: 1px solid #bde5c8; }
                .high-risk { background-color: #fdeeee; color: #b33939; border: 1px solid #f1c0c0; }
                .neutral-box { background-color: #f5f7fb; color: #41536f; border: 1px solid #dde5f0; }
                pre {
                    background: #f3f6fa;
                    padding: 14px;
                    border-radius: 10px;
                    overflow-x: auto;
                    border: 1px solid #e1e8f2;
                    font-size: 13px;
                    line-height: 1.45;
                    white-space: pre-wrap;
                }
                code { background: #eef3f9; padding: 3px 6px; border-radius: 6px; font-size: 13px; }
                ul { line-height: 1.7; padding-left: 20px; }
                .badge {
                    display: inline-block;
                    padding: 5px 10px;
                    border-radius: 999px;
                    background-color: #e9eef7;
                    color: #1f3960;
                    font-size: 12px;
                    font-weight: 700;
                    margin-bottom: 12px;
                }
                .info-text { color: #55657d; font-size: 14px; }
                .nav-links {
                    display: flex;
                    gap: 12px;
                    flex-wrap: wrap;
                    margin-top: 16px;
                }
                .nav-link {
                    display: inline-block;
                    padding: 9px 18px;
                    border-radius: 8px;
                    background: linear-gradient(135deg, #1c3d68, #29558d);
                    color: white;
                    text-decoration: none;
                    font-size: 14px;
                    font-weight: 600;
                    transition: transform 0.15s ease, box-shadow 0.15s ease;
                }
                .nav-link:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 6px 16px rgba(28, 61, 104, 0.22);
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                    margin-top: 12px;
                }
                th {
                    background: #172a45;
                    color: white;
                    padding: 10px 12px;
                    text-align: left;
                }
                td { padding: 9px 12px; border-bottom: 1px solid #e8edf5; }
                tr:last-child td { border-bottom: none; }
                tr:hover td { background-color: #f5f8fd; }
                footer { text-align: center; padding: 24px; color: #6f7f95; font-size: 14px; }
                @media (max-width: 900px) {
                    .container { grid-template-columns: 1fr; }
                    .card.full-width { grid-column: 1; }
                }
            </style>
        </head>
        <body>

            <header>
                <h1>🚗 MotorRisk Analytics</h1>
                <p>Plataforma de evaluación predictiva para aseguradoras de automóviles</p>
            </header>

            <div class="container">

                <!-- SIMULADOR INDIVIDUAL -->
                <div class="card">
                    <div class="badge">Simulador de riesgo</div>
                    <h2>Evaluar conductor</h2>
                    <p class="info-text">
                        Introduce las variables del asegurado para obtener una predicción automática sobre el riesgo de infracción grave.
                    </p>

                    <label>Sexo</label>
                    <select id="sexo">
                        <option value="" disabled selected>Selecciona...</option>
                        <option value="1">1 — Hombre</option>
                        <option value="0">0 — Mujer</option>
                    </select>

                    <label>¿Es conductor novel?</label>
                    <select id="novel">
                        <option value="" disabled selected>Selecciona...</option>
                        <option value="0">0 — No (conductor experimentado)</option>
                        <option value="1">1 — Sí (carné reciente, ≤ 2 años)</option>
                    </select>

                    <label>Tramo de edad</label>
                    <select id="edad">
                        <option value="" disabled selected>Selecciona...</option>
                        <option value="1">1 — 18–24 años</option>
                        <option value="2">2 — 25–34 años</option>
                        <option value="3">3 — 35–44 años</option>
                        <option value="4">4 — 45–54 años</option>
                        <option value="5">5 — 55–64 años</option>
                        <option value="6">6 — 65 o más años</option>
                    </select>

                    <label>Número de infracciones registradas</label>
                    <input type="number" id="num_infracciones" placeholder="Ej: 0, 1, 2..." min="0">

                    <div id="validation_errors" style="display:none; color:#b33939; font-size:13px; margin:8px 0; background:#fdeeee; padding:10px 12px; border-radius:8px; border:1px solid #f1c0c0; line-height:1.6;"></div>

                    <button onclick="hacerPrediccion()">Evaluar riesgo</button>

                    <div id="resultado_box" class="result-box neutral-box">
                        Aquí se mostrará la interpretación del resultado.
                    </div>

                    <h3>Respuesta JSON</h3>
                    <pre id="resultado">Aquí aparecerá la respuesta del endpoint POST.</pre>
                </div>

                <!-- DOCUMENTACIÓN API -->
                <div class="card">
                    <div class="badge">Documentación técnica</div>
                    <h2>Documentación API</h2>

                    <h3>1. POST /api/v1/predict</h3>
                    <p class="info-text">Predicción individual. Envía un JSON con los datos del conductor.</p>
                    <pre>POST /api/v1/predict
{
  "sexo": 1, "novel": 0,
  "edad": 3, "num_infracciones": 2
}</pre>

                    <h3>2. GET /api/v1/predict</h3>
                    <p class="info-text">Predicción rápida por parámetros URL.</p>
                    <pre>GET /api/v1/predict?sexo=1&amp;novel=0&amp;edad=3&amp;num_infracciones=2</pre>

                    <h3>3. GET /api/v1/model/info</h3>
                    <p class="info-text">Metadatos del modelo: tipo, features esperadas y parámetros del estimador.</p>
                    <pre>GET /api/v1/model/info</pre>

                    <h3>4. POST /api/v1/predict/batch</h3>
                    <p class="info-text">Predicción por lotes. Envía un array de conductores y recibe una predicción por cada uno.</p>
                    <pre>POST /api/v1/predict/batch
{
  "registros": [
    {"sexo": 1, "novel": 0, "edad": 3, "num_infracciones": 2},
    {"sexo": 0, "novel": 1, "edad": 1, "num_infracciones": 0}
  ]
}</pre>

                    <h3>5. Variables de entrada</h3>
                    <ul>
                        <li><b>sexo</b>: <code>0</code> = Mujer · <code>1</code> = Hombre.</li>
                        <li><b>novel</b>: <code>0</code> = No novel · <code>1</code> = Conductor novel (carné ≤ 2 años).</li>
                        <li><b>edad</b>: tramo 1–6 (1=18-24, 2=25-34, 3=35-44, 4=45-54, 5=55-64, 6=65+).</li>
                        <li><b>num_infracciones</b>: entero ≥ 0, infracciones registradas.</li>
                    </ul>

                    <h3>Páginas interactivas</h3>
                    <div class="nav-links">
                        <a class="nav-link" href="/model/info">🔍 Info del modelo</a>
                        <a class="nav-link" href="/predict/batch">📋 Predicción batch</a>
                        <a class="nav-link" href="/docs">📄 Swagger UI</a>
                    </div>
                </div>

            </div>

            <footer>
                © 2026 MotorRisk Analytics · Motor de scoring predictivo para aseguradoras
            </footer>

            <script>
                function hacerPrediccion() {
                    const sexoVal = document.getElementById("sexo").value;
                    const novelVal = document.getElementById("novel").value;
                    const edadVal = document.getElementById("edad").value;
                    const infrVal = document.getElementById("num_infracciones").value;

                    const errores = [];
                    if (sexoVal === "") errores.push("• <b>Sexo</b>: selecciona una opción.");
                    if (novelVal === "") errores.push("• <b>Conductor novel</b>: selecciona una opción.");
                    if (edadVal === "") errores.push("• <b>Tramo de edad</b>: selecciona una opción.");
                    if (infrVal === "" || isNaN(parseInt(infrVal)) || parseInt(infrVal) < 0) {
                        errores.push("• <b>Infracciones</b>: introduce un número entero ≥ 0.");
                    }

                    const errDiv = document.getElementById("validation_errors");
                    if (errores.length > 0) {
                        errDiv.style.display = "block";
                        errDiv.innerHTML = "<b>Revisa los siguientes campos:</b><br>" + errores.join("<br>");
                        return;
                    }
                    errDiv.style.display = "none";

                    const data = {
                        sexo: parseInt(sexoVal),
                        novel: parseInt(novelVal),
                        edad: parseInt(edadVal),
                        num_infracciones: parseInt(infrVal)
                    };

                    fetch('/api/v1/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    })
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById("resultado").textContent = JSON.stringify(data, null, 2);
                        let box = document.getElementById("resultado_box");
                        if (data.detail) {
                            let errMsg = "<b>⚠️ Error de validación:</b><br>";
                            if (Array.isArray(data.detail)) {
                                data.detail.forEach(e => {
                                    const campo = e.loc ? e.loc[e.loc.length - 1] : "campo";
                                    errMsg += `• <b>${campo}</b>: ${e.msg}<br>`;
                                });
                            } else {
                                errMsg += data.detail;
                            }
                            box.className = "result-box high-risk";
                            box.innerHTML = errMsg;
                            return;
                        }
                        const prob = (data.probability !== null && data.probability !== undefined)
                            ? (data.probability * 100).toFixed(1) : null;
                        const probText = prob !== null ? ` · Probabilidad: <b>${prob}%</b>` : '';
                        let interp = '';
                        if (data.probability !== null && data.probability !== undefined) {
                            if (data.probability < 0.3) interp = ' — perfil claramente de bajo riesgo.';
                            else if (data.probability < 0.6) interp = ' — zona de incertidumbre.';
                            else interp = ' — perfil claramente de alto riesgo.';
                        }
                        if (data.prediction === 1) {
                            box.className = "result-box high-risk";
                            box.innerHTML = `⚠️ <b>Riesgo ALTO</b>${probText}${interp}`;
                        } else {
                            box.className = "result-box low-risk";
                            box.innerHTML = `✅ <b>Riesgo BAJO</b>${probText}${interp}`;
                        }
                    })
                    .catch(err => {
                        document.getElementById("resultado").textContent = "Error: " + err;
                        let box = document.getElementById("resultado_box");
                        box.className = "result-box high-risk";
                        box.innerHTML = "⚠️ No se ha podido completar la solicitud al endpoint.";
                    });
                }
            </script>

        </body>
    </html>
    """



# PREDICT — GET

@app.get("/api/v1/predict", summary="Predicción individual (GET)")
def predict_get(
    sexo: int = Query(..., ge=0, le=1, description="Sexo · 0 = Mujer, 1 = Hombre"),
    novel: int = Query(..., ge=0, le=1, description="Conductor novel · 0 = No, 1 = Sí (carné ≤ 2 años)"),
    edad: int = Query(..., ge=1, le=6, description="Tramo de edad · 1=18-24, 2=25-34, 3=35-44, 4=45-54, 5=55-64, 6=65+"),
    num_infracciones: int = Query(..., ge=0, description="Número de infracciones registradas (≥ 0)")
):
    return run_prediction(sexo, novel, edad, num_infracciones)



# PREDICT — POST

@app.post("/api/v1/predict", summary="Predicción individual (POST)")
def predict_post(conductor: ConductorInput):
    return run_prediction(
        conductor.sexo, conductor.novel,
        conductor.edad, conductor.num_infracciones,
        include_proba=True
    )



# MODEL INFO — API JSON

@app.get("/api/v1/model/info", summary="Información del modelo")
def model_info_api():
    info = {
        "model_type": type(model).__name__,
        "features": ["SEXO", "NOVEL", "EDAD", "NUM_INFRACCIONES"],
        "feature_descriptions": {
            "SEXO": "Sexo del conductor · 0 = Mujer, 1 = Hombre",
            "NOVEL": "Conductor novel · 0 = No (experimentado), 1 = Sí (carné ≤ 2 años)",
            "EDAD": "Tramo de edad · 1=18-24, 2=25-34, 3=35-44, 4=45-54, 5=55-64, 6=65+",
            "NUM_INFRACCIONES": "Número de infracciones registradas (entero ≥ 0)"
        },
        "target": "Riesgo de infracción grave · 0 = bajo riesgo, 1 = alto riesgo",
        "supports_proba": hasattr(model, 'predict_proba')
    }
    if hasattr(model, 'classes_'):
        info["classes"] = [int(c) for c in model.classes_]
    if hasattr(model, 'n_estimators'):
        info["n_estimators"] = model.n_estimators
    if hasattr(model, 'max_depth'):
        info["max_depth"] = model.max_depth

    return info



# MODEL INFO — HTML interactivo

@app.get("/model/info", response_class=HTMLResponse, include_in_schema=False)
def model_info_html():
    return """
    <html>
        <head>
            <title>Info del Modelo · MotorRisk Analytics</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #f4f6f9; color: #24324a; }
                header { background: linear-gradient(135deg, #172a45, #223b63); color: white; padding: 28px 40px; }
                header h1 { margin: 0; font-size: 28px; }
                header p { margin: 8px 0 0 0; opacity: 0.85; font-size: 15px; }
                .container { max-width: 860px; margin: 30px auto; padding: 0 20px; display: flex; flex-direction: column; gap: 24px; }
                .card { background: white; padding: 28px; border-radius: 16px; box-shadow: 0 8px 24px rgba(20,35,60,0.08); border: 1px solid #e8edf5; }
                h2 { color: #172a45; margin-top: 0; }
                table { width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 12px; }
                th { background: #172a45; color: white; padding: 10px 14px; text-align: left; }
                td { padding: 10px 14px; border-bottom: 1px solid #e8edf5; }
                tr:last-child td { border-bottom: none; }
                tr:hover td { background: #f5f8fd; }
                pre { background: #f3f6fa; padding: 14px; border-radius: 10px; border: 1px solid #e1e8f2; font-size: 13px; white-space: pre-wrap; }
                .badge { display: inline-block; padding: 5px 10px; border-radius: 999px; background: #e9eef7; color: #1f3960; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
                .back { display: inline-block; margin-bottom: 16px; color: #29558d; text-decoration: none; font-weight: 600; font-size: 14px; }
                .back:hover { text-decoration: underline; }
                .loading { color: #55657d; font-style: italic; }
                footer { text-align: center; padding: 24px; color: #6f7f95; font-size: 14px; }
            </style>
        </head>
        <body>
            <header>
                <h1>🔍 Información del Modelo</h1>
                <p>Metadatos y configuración del modelo activo en producción</p>
            </header>

            <div class="container">
                <a class="back" href="/">← Volver a la página principal</a>

                <div class="card">
                    <div class="badge">Modelo activo</div>
                    <h2>Resumen del modelo</h2>
                    <div id="resumen"><span class="loading">Cargando...</span></div>
                </div>

                <div class="card">
                    <div class="badge">Variables de entrada</div>
                    <h2>Features esperadas</h2>
                    <div id="features"><span class="loading">Cargando...</span></div>
                </div>

                <div class="card">
                    <div class="badge">Respuesta JSON</div>
                    <h2>Respuesta completa del endpoint</h2>
                    <pre id="json_raw">Cargando...</pre>
                </div>
            </div>

            <footer>© 2026 MotorRisk Analytics</footer>

            <script>
                fetch('/api/v1/model/info')
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('json_raw').textContent = JSON.stringify(data, null, 2);

                        let resumenHTML = '<table><thead><tr><th>Propiedad</th><th>Valor</th></tr></thead><tbody>';
                        const skip = ['features', 'feature_descriptions'];
                        for (const [k, v] of Object.entries(data)) {
                            if (!skip.includes(k)) {
                                resumenHTML += `<tr><td><b>${k}</b></td><td>${JSON.stringify(v)}</td></tr>`;
                            }
                        }
                        resumenHTML += '</tbody></table>';
                        document.getElementById('resumen').innerHTML = resumenHTML;

                        if (data.feature_descriptions) {
                            let featHTML = '<table><thead><tr><th>Variable</th><th>Descripción</th></tr></thead><tbody>';
                            for (const [k, v] of Object.entries(data.feature_descriptions)) {
                                featHTML += `<tr><td><b>${k}</b></td><td>${v}</td></tr>`;
                            }
                            featHTML += '</tbody></table>';
                            document.getElementById('features').innerHTML = featHTML;
                        }
                    })
                    .catch(err => {
                        document.getElementById('resumen').innerHTML = '<span style="color:red">Error al cargar los datos del modelo.</span>';
                    });
            </script>
        </body>
    </html>
    """



# PREDICT BATCH — API JSON

@app.post("/api/v1/predict/batch", summary="Predicción por lotes")
def predict_batch_api(batch: BatchInput):
    resultados = []
    for i, conductor in enumerate(batch.registros):
        result = run_prediction(
            conductor.sexo, conductor.novel,
            conductor.edad, conductor.num_infracciones,
            include_proba=True
        )
        result["index"] = i
        resultados.append(result)

    return {
        "total": len(batch.registros),
        "resultados": resultados
    }



# PREDICT BATCH — HTML interactivo

@app.get("/predict/batch", response_class=HTMLResponse, include_in_schema=False)
def predict_batch_html():
    return """
    <html>
        <head>
            <title>Predicción Batch · MotorRisk Analytics</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #f4f6f9; color: #24324a; }
                header { background: linear-gradient(135deg, #172a45, #223b63); color: white; padding: 28px 40px; }
                header h1 { margin: 0; font-size: 28px; }
                header p { margin: 8px 0 0 0; opacity: 0.85; font-size: 15px; }
                .container { max-width: 960px; margin: 30px auto; padding: 0 20px; display: flex; flex-direction: column; gap: 24px; }
                .card { background: white; padding: 28px; border-radius: 16px; box-shadow: 0 8px 24px rgba(20,35,60,0.08); border: 1px solid #e8edf5; }
                h2 { color: #172a45; margin-top: 0; }
                textarea { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cfd8e6; box-sizing: border-box; font-size: 13px; background: #fbfcfe; font-family: monospace; resize: vertical; }
                textarea:focus { outline: none; border-color: #305f9b; box-shadow: 0 0 0 3px rgba(48,95,155,0.12); }
                button { padding: 13px 28px; background: linear-gradient(135deg, #1c3d68, #29558d); color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: transform 0.15s ease; }
                button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(28,61,104,0.22); }
                table { width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 16px; }
                th { background: #172a45; color: white; padding: 10px 14px; text-align: left; }
                td { padding: 10px 14px; border-bottom: 1px solid #e8edf5; }
                tr:last-child td { border-bottom: none; }
                .high { color: #b33939; font-weight: 700; }
                .low  { color: #1f7a3d; font-weight: 700; }
                .err  { color: #b33939; font-style: italic; }
                pre { background: #f3f6fa; padding: 14px; border-radius: 10px; border: 1px solid #e1e8f2; font-size: 13px; white-space: pre-wrap; }
                .badge { display: inline-block; padding: 5px 10px; border-radius: 999px; background: #e9eef7; color: #1f3960; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
                .back { display: inline-block; margin-bottom: 16px; color: #29558d; text-decoration: none; font-weight: 600; font-size: 14px; }
                .back:hover { text-decoration: underline; }
                #tabla_resultados { display: none; }
                footer { text-align: center; padding: 24px; color: #6f7f95; font-size: 14px; }
            </style>
        </head>
        <body>
            <header>
                <h1>📋 Predicción por Lotes</h1>
                <p>Evalúa múltiples conductores en una sola petición</p>
            </header>

            <div class="container">
                <a class="back" href="/">← Volver a la página principal</a>

                <div class="card">
                    <div class="badge">Entrada JSON</div>
                    <h2>Introduce los registros</h2>
                    <p style="color:#55657d; font-size:14px;">
                        Pega un JSON con la clave <b>registros</b> conteniendo un array de conductores.
                        Cada registro debe incluir: <b>sexo</b>, <b>novel</b>, <b>edad</b> y <b>num_infracciones</b>.
                    </p>
                    <textarea id="batch_input" rows="12">{
  "registros": [
    {"sexo": 1, "novel": 0, "edad": 3, "num_infracciones": 2},
    {"sexo": 0, "novel": 1, "edad": 1, "num_infracciones": 0},
    {"sexo": 1, "novel": 0, "edad": 5, "num_infracciones": 5}
  ]
}</textarea>
                    <button onclick="enviarBatch()" style="margin-top:16px;">Evaluar lote</button>
                    <div id="batch_error" style="display:none; color:#b33939; font-size:13px; margin-top:12px; background:#fdeeee; padding:10px 12px; border-radius:8px; border:1px solid #f1c0c0; line-height:1.6;"></div>
                </div>

                <div class="card" id="tabla_resultados">
                    <div class="badge">Resultados</div>
                    <h2 id="resumen_titulo">Resultados del lote</h2>
                    <div id="tabla_html"></div>
                </div>

                <div class="card">
                    <div class="badge">Respuesta JSON</div>
                    <h2>Respuesta completa del endpoint</h2>
                    <pre id="json_raw">Aquí aparecerá la respuesta JSON del batch.</pre>
                </div>
            </div>

            <footer>© 2026 MotorRisk Analytics</footer>

            <script>
                function enviarBatch() {
                    let raw = document.getElementById('batch_input').value;
                    let json;
                    try {
                        json = JSON.parse(raw);
                    } catch(e) {
                        alert('JSON inválido: ' + e.message);
                        return;
                    }

                    fetch('/api/v1/predict/batch', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(json)
                    })
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('json_raw').textContent = JSON.stringify(data, null, 2);

                        if (data.detail) {
                            document.getElementById('tabla_resultados').style.display = 'none';
                            let errMsg = '<b>⚠️ Error de validación:</b><br>';
                            if (Array.isArray(data.detail)) {
                                data.detail.forEach(e => {
                                    const campo = e.loc ? e.loc[e.loc.length - 1] : 'campo';
                                    errMsg += `• <b>${campo}</b>: ${e.msg}<br>`;
                                });
                            } else {
                                errMsg += JSON.stringify(data.detail);
                            }
                            const batchErr = document.getElementById('batch_error');
                            batchErr.style.display = 'block';
                            batchErr.innerHTML = errMsg;
                            return;
                        }
                        document.getElementById('batch_error').style.display = 'none';

                        document.getElementById('resumen_titulo').textContent =
                            'Resultados del lote (' + data.total + ' registros)';

                        let html = '<table><thead><tr><th>#</th><th>Estado</th><th>Probabilidad</th><th>Clase (0/1)</th></tr></thead><tbody>';
                        for (const r of data.resultados) {
                            const risk = r.prediction === 1;
                            const label = risk ? '<span class="high">⚠️ Riesgo ALTO</span>' : '<span class="low">✅ Riesgo BAJO</span>';
                            const prob = r.probability !== null && r.probability !== undefined
                                ? (r.probability * 100).toFixed(1) + '%' : 'N/A';
                            html += `<tr><td>${r.index}</td><td>${label}</td><td>${prob}</td><td>${r.prediction}</td></tr>`;
                        }
                        html += '</tbody></table>';

                        document.getElementById('tabla_html').innerHTML = html;
                        document.getElementById('tabla_resultados').style.display = 'block';
                    })
                    .catch(err => {
                        document.getElementById('json_raw').textContent = 'Error: ' + err;
                    });
                }
            </script>
        </body>
    </html>
    """



# RUN

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
