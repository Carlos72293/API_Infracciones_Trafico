from flask import Flask, jsonify, request
import os
import pickle
import pandas as pd
import numpy as np

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)

# Cargar el modelo
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)



# LANDING PAGE
@app.route('/', methods=["GET"])
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
                input, textarea {
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
                input:focus, textarea:focus {
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

                    <label>Sexo (0 o 1)</label>
                    <input type="number" id="sexo" placeholder="Ejemplo: 1">

                    <label>Conductor novel (0 o 1)</label>
                    <input type="number" id="novel" placeholder="Ejemplo: 0">

                    <label>Edad (1 a 6)</label>
                    <input type="number" id="edad" placeholder="Ejemplo: 3">

                    <label>Número de infracciones</label>
                    <input type="number" id="num_infracciones" placeholder="Ejemplo: 2">

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
                    <p class="info-text">Metadatos del modelo: tipo, features esperadas y métricas.</p>
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
                        <li><b>sexo</b>: 0 o 1.</li>
                        <li><b>novel</b>: conductor novel, 0 o 1.</li>
                        <li><b>edad</b>: tramo de edad entre 1 y 6.</li>
                        <li><b>num_infracciones</b>: número de infracciones registradas.</li>
                    </ul>

                    <h3>Páginas interactivas</h3>
                    <div class="nav-links">
                        <a class="nav-link" href="/model/info">🔍 Info del modelo</a>
                        <a class="nav-link" href="/predict/batch">📋 Predicción batch</a>
                    </div>
                </div>

            </div>

            <footer>
                © 2026 MotorRisk Analytics · Motor de scoring predictivo para aseguradoras
            </footer>

            <script>
                function hacerPrediccion() {
                    const data = {
                        sexo: document.getElementById("sexo").value,
                        novel: document.getElementById("novel").value,
                        edad: document.getElementById("edad").value,
                        num_infracciones: document.getElementById("num_infracciones").value
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
                        if (data.error) {
                            box.className = "result-box high-risk";
                            box.innerHTML = "⚠️ Error en la petición: revisa los campos obligatorios y sus valores.";
                            return;
                        }
                        if (data.prediction === 1) {
                            box.className = "result-box high-risk";
                            box.innerHTML = "⚠️ Riesgo ALTO: el modelo clasifica este perfil como propenso a infracción grave.";
                        } else {
                            box.className = "result-box low-risk";
                            box.innerHTML = "✅ Riesgo BAJO: el modelo clasifica este perfil como no grave.";
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



# HELPERS
def to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return np.nan


def validate_inputs(sexo, novel, edad):
    errors = []
    if not np.isnan(sexo) and sexo not in (0.0, 1.0):
        errors.append("SEXO debe ser 0 o 1")
    if not np.isnan(novel) and novel not in (0.0, 1.0):
        errors.append("NOVEL debe ser 0 o 1")
    if not np.isnan(edad) and edad not in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        errors.append("EDAD debe ser un número entre 1 y 6")
    return errors


def get_missing(sexo, novel, edad, num_infracciones):
    return [
        name for name, val in [
            ('SEXO', sexo), ('NOVEL', novel),
            ('EDAD', edad), ('NUM_INFRACCIONES', num_infracciones)
        ]
        if np.isnan(val)
    ]


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



# PREDICT — GET
@app.route('/api/v1/predict', methods=["GET"])
def predict_get():
    args = {k.lower(): v for k, v in request.args.items()}

    sexo             = to_float(args.get('sexo'))
    novel            = to_float(args.get('novel'))
    edad             = to_float(args.get('edad'))
    num_infracciones = to_float(args.get('num_infracciones'))

    errors = validate_inputs(sexo, novel, edad)
    if errors:
        return jsonify({'error': errors}), 400

    missing = get_missing(sexo, novel, edad, num_infracciones)
    if missing:
        return jsonify({"error": "Faltan variables obligatorias", "missing": missing}), 400

    return jsonify(run_prediction(sexo, novel, edad, num_infracciones))


# PREDICT — POST
@app.route('/api/v1/predict', methods=["POST"])
def predict_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se ha enviado JSON"}), 400

    args = {k.lower(): v for k, v in data.items()}

    sexo             = to_float(args.get('sexo'))
    novel            = to_float(args.get('novel'))
    edad             = to_float(args.get('edad'))
    num_infracciones = to_float(args.get('num_infracciones'))

    errors = validate_inputs(sexo, novel, edad)
    if errors:
        return jsonify({'error': errors}), 400

    missing = get_missing(sexo, novel, edad, num_infracciones)
    if missing:
        return jsonify({"error": "Faltan variables obligatorias", "missing": missing}), 400

    return jsonify(run_prediction(sexo, novel, edad, num_infracciones, include_proba=True))



# MODEL INFO — API JSON
@app.route('/api/v1/model/info', methods=["GET"])
def model_info_api():
    info = {
        "model_type": type(model).__name__,
        "features": ["SEXO", "NOVEL", "EDAD", "NUM_INFRACCIONES"],
        "feature_descriptions": {
            "SEXO": "Sexo del conductor (0 o 1)",
            "NOVEL": "Conductor novel (0 o 1)",
            "EDAD": "Tramo de edad codificado (1 a 6)",
            "NUM_INFRACCIONES": "Número de infracciones registradas"
        },
        "target": "Riesgo de infracción grave (0 = bajo, 1 = alto)",
        "supports_proba": hasattr(model, 'predict_proba')
    }

    # Intentar extraer métricas si el modelo las expone
    if hasattr(model, 'classes_'):
        info["classes"] = [int(c) for c in model.classes_]
    if hasattr(model, 'n_estimators'):
        info["n_estimators"] = model.n_estimators
    if hasattr(model, 'max_depth'):
        info["max_depth"] = model.max_depth

    return jsonify(info)



# MODEL INFO — HTML interactivo
@app.route('/model/info', methods=["GET"])
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
@app.route('/api/v1/predict/batch', methods=["POST"])
def predict_batch_api():
    data = request.get_json()
    if not data or 'registros' not in data:
        return jsonify({"error": "Se esperaba un JSON con clave 'registros' (array de conductores)"}), 400

    registros = data['registros']
    if not isinstance(registros, list) or len(registros) == 0:
        return jsonify({"error": "'registros' debe ser una lista no vacía"}), 400

    resultados = []
    for i, reg in enumerate(registros):
        args = {k.lower(): v for k, v in reg.items()}

        sexo             = to_float(args.get('sexo'))
        novel            = to_float(args.get('novel'))
        edad             = to_float(args.get('edad'))
        num_infracciones = to_float(args.get('num_infracciones'))

        errors = validate_inputs(sexo, novel, edad)
        if errors:
            resultados.append({"index": i, "error": errors})
            continue

        missing = get_missing(sexo, novel, edad, num_infracciones)
        if missing:
            resultados.append({"index": i, "error": "Faltan variables obligatorias", "missing": missing})
            continue

        result = run_prediction(sexo, novel, edad, num_infracciones, include_proba=True)
        result["index"] = i
        resultados.append(result)

    return jsonify({
        "total": len(registros),
        "resultados": resultados
    })



# PREDICT BATCH — HTML interactivo
@app.route('/predict/batch', methods=["GET"])
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

                        if (data.error) {
                            document.getElementById('tabla_resultados').style.display = 'none';
                            alert('Error: ' + data.error);
                            return;
                        }

                        document.getElementById('resumen_titulo').textContent =
                            'Resultados del lote (' + data.total + ' registros)';

                        let html = '<table><thead><tr><th>#</th><th>Predicción</th><th>Probabilidad</th><th>Estado</th></tr></thead><tbody>';
                        for (const r of data.resultados) {
                            if (r.error) {
                                html += `<tr><td>${r.index}</td><td colspan="3" class="err">⚠️ Error: ${JSON.stringify(r.error)}</td></tr>`;
                            } else {
                                const risk = r.prediction === 1;
                                const label = risk ? '<span class="high">⚠️ Riesgo ALTO</span>' : '<span class="low">✅ Riesgo BAJO</span>';
                                const prob = r.probability !== null && r.probability !== undefined
                                    ? (r.probability * 100).toFixed(1) + '%' : 'N/A';
                                html += `<tr><td>${r.index}</td><td>${r.prediction}</td><td>${prob}</td><td>${label}</td></tr>`;
                            }
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
    app.run(debug=True)
