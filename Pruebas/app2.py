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


# Enruta la landing page (endpoint /)

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


# Enruta la landing page (endpoint /)

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

                header h1 {
                    margin: 0;
                    font-size: 32px;
                }

                header p {
                    margin: 8px 0 0 0;
                    opacity: 0.92;
                    font-size: 16px;
                }

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

                h2 {
                    color: #172a45;
                    margin-top: 0;
                    margin-bottom: 18px;
                    font-size: 24px;
                }

                h3 {
                    color: #223b63;
                    margin-top: 22px;
                    margin-bottom: 10px;
                    font-size: 18px;
                }

                h4 {
                    margin-top: 16px;
                    margin-bottom: 8px;
                    font-size: 15px;
                    color: #304563;
                }

                label {
                    font-weight: 600;
                    display: block;
                    margin-bottom: 6px;
                    margin-top: 12px;
                }

                input {
                    width: 100%;
                    padding: 12px;
                    margin: 0 0 8px 0;
                    border-radius: 8px;
                    border: 1px solid #cfd8e6;
                    box-sizing: border-box;
                    font-size: 14px;
                    background-color: #fbfcfe;
                }

                input:focus {
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

                .low-risk {
                    background-color: #e9f8ef;
                    color: #1f7a3d;
                    border: 1px solid #bde5c8;
                }

                .high-risk {
                    background-color: #fdeeee;
                    color: #b33939;
                    border: 1px solid #f1c0c0;
                }

                .neutral-box {
                    background-color: #f5f7fb;
                    color: #41536f;
                    border: 1px solid #dde5f0;
                }

                pre {
                    background: #f3f6fa;
                    padding: 14px;
                    border-radius: 10px;
                    overflow-x: auto;
                    border: 1px solid #e1e8f2;
                    font-size: 13px;
                    line-height: 1.45;
                }

                code {
                    background: #eef3f9;
                    padding: 3px 6px;
                    border-radius: 6px;
                    font-size: 13px;
                }

                ul {
                    line-height: 1.7;
                    padding-left: 20px;
                }

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

                .info-text {
                    color: #55657d;
                    font-size: 14px;
                }

                footer {
                    text-align: center;
                    padding: 24px;
                    color: #6f7f95;
                    font-size: 14px;
                }

                @media (max-width: 900px) {
                    .container {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>

        <body>

            <header>
                <h1>🚗 MotorRisk Analytics</h1>
                <p>Plataforma de evaluación predictiva para aseguradoras de automóviles</p>
            </header>

            <div class="container">

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

                <div class="card">
                    <div class="badge">Documentación técnica</div>
                    <h2>Documentación API</h2>

                    <h3>1. Endpoint POST</h3>
                    <p class="info-text">
                        Endpoint principal recomendado para integrar la predicción en aplicaciones, dashboards o sistemas internos.
                    </p>

                    <h4>Ruta</h4>
                    <pre>POST /api/v1/predict</pre>

                    <h4>Input JSON</h4>
                    <pre>{
  "sexo": 1,
  "novel": 0,
  "edad": 3,
  "num_infracciones": 2
}</pre>

                    <h4>Output esperado</h4>
                    <pre>{
  "prediction": 1,
  "probability": 0.82,
  "missing": []
}</pre>

                    <h4>Interpretación de la salida (POST)</h4>
                    <ul>
                        <li><b>prediction</b>: etiqueta predicha por el modelo. <b>0</b> indica riesgo bajo y <b>1</b> indica riesgo alto de infracción grave.</li>
                        <li><b>probability</b>: probabilidad estimada de pertenecer a la clase de riesgo alto. Cuanto más próximo a 1, mayor confianza del modelo en esa clasificación.</li>
                        <li><b>missing</b>: lista de variables obligatorias no informadas en la petición. Si está vacía, significa que el envío fue completo.</li>
                    </ul>

                    <h3>2. Endpoint GET</h3>
                    <p class="info-text">
                        Endpoint alternativo para consultas rápidas mediante parámetros en la URL.
                    </p>

                    <h4>Ruta</h4>
                    <pre>GET /api/v1/predict?sexo=1&novel=0&edad=3&num_infracciones=2</pre>

                    <h4>Output esperado</h4>
                    <pre>{
  "prediction": 1,
  "missing": []
}</pre>

                    <h4>Interpretación de la salida (GET)</h4>
                    <ul>
                        <li><b>prediction</b>: etiqueta generada por el modelo. <b>0</b> significa que la infracción prevista no es grave y <b>1</b> significa que la predicción corresponde a una infracción grave.</li>
                        <li><b>missing</b>: lista con las variables obligatorias que faltan en la petición. Si aparece vacía, todos los campos necesarios fueron enviados correctamente.</li>
                    </ul>

                    <h3>3. Variables de entrada</h3>
                    <ul>
                        <li><b>sexo</b>: variable codificada como <b>0</b> o <b>1</b>.</li>
                        <li><b>novel</b>: indica si el conductor es novel, con valores <b>0</b> o <b>1</b>.</li>
                        <li><b>edad</b>: tramo de edad codificado entre <b>1</b> y <b>6</b>.</li>
                        <li><b>num_infracciones</b>: número de infracciones registradas.</li>
                    </ul>

                    <h3>4. Consideraciones</h3>
                    <ul>
                        <li>Todos los campos son obligatorios para poder generar una predicción válida.</li>
                        <li>Si hay datos ausentes o fuera de rango, la API devolverá un error de validación.</li>
                        <li>El endpoint POST es la opción más adecuada para integraciones más robustas.</li>
                    </ul>
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
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
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
                    .catch(error => {
                        document.getElementById("resultado").textContent = "Error: " + error;
                        let box = document.getElementById("resultado_box");
                        box.className = "result-box high-risk";
                        box.innerHTML = "⚠️ No se ha podido completar la solicitud al endpoint.";
                    });
                }
            </script>

        </body>
    </html>
    """



# PREDICT PERO EN GET 

@app.route('/api/v1/predict', methods=["GET"])
def predict_get():
    args = {k.lower(): v for k, v in request.args.items()}

    
    sexo = args.get('sexo')
    novel = args.get('novel')
    edad = args.get('edad')
    num_infracciones = args.get('num_infracciones')  

   
    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return np.nan

    sexo = to_float(sexo)
    novel = to_float(novel)
    edad = to_float(edad)
    num_infracciones = to_float(num_infracciones)

    # Comprobaciones
    errors = []

    if not np.isnan(sexo) and sexo not in (0.0, 1.0):
        errors.append("SEXO debe ser 0 o 1")

    if not np.isnan(novel) and novel not in (0.0, 1.0):
        errors.append("NOVEL debe ser 0 o 1")

    if not np.isnan(edad) and edad not in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        errors.append("EDAD debe ser un número entre 1 y 6")

    if errors:
        return jsonify({'error': errors}), 400

    # Detectar missing correctamente
    missing = [
        name for name, val in [
            ('SEXO', sexo),
            ('NOVEL', novel),
            ('EDAD', edad),
            ('NUM_INFRACCIONES', num_infracciones)
        ]
        if np.isnan(val)
    ]

    if missing:
        return jsonify({
            "error": "Faltan variables obligatorias",  # No puede predecir si hay missing
            "missing": missing
        }), 400


    # Crear DataFrame
    input_data = pd.DataFrame({
        'SEXO': [sexo],
        'NOVEL': [novel],
        'EDAD': [edad],
        'NUM_INFRACCIONES': [num_infracciones]
    })

    prediction = model.predict(input_data)

    # Convertir a tipo Python 
    response = {
        "prediction": int(prediction[0]),
        "missing": missing
    }

    return jsonify(response)



# PREDICT PERO EN POST (Body)

@app.route('/api/v1/predict', methods=["POST"])
def predict_post():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No se ha enviado JSON"}), 400

    args = {k.lower(): v for k, v in data.items()}

    sexo = args.get('sexo')
    novel = args.get('novel')
    edad = args.get('edad')
    num_infracciones = args.get('num_infracciones')

    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return np.nan

    sexo = to_float(sexo)
    novel = to_float(novel)
    edad = to_float(edad)
    num_infracciones = to_float(num_infracciones)

    errors = []

    if not np.isnan(sexo) and sexo not in (0.0, 1.0):
        errors.append("SEXO debe ser 0 o 1")

    if not np.isnan(novel) and novel not in (0.0, 1.0):
        errors.append("NOVEL debe ser 0 o 1")

    if not np.isnan(edad) and edad not in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        errors.append("EDAD debe ser un número entre 1 y 6")

    if errors:
        return jsonify({'error': errors}), 400

    missing = [
        name for name, val in [
            ('SEXO', sexo),
            ('NOVEL', novel),
            ('EDAD', edad),
            ('NUM_INFRACCIONES', num_infracciones)
        ]
        if np.isnan(val)
    ]

    if missing:
        return jsonify({
            "error": "Faltan variables obligatorias",
            "missing": missing
        }), 400

    input_data = pd.DataFrame({
        'SEXO': [sexo],
        'NOVEL': [novel],
        'EDAD': [edad],
        'NUM_INFRACCIONES': [num_infracciones]
    })

    prediction = model.predict(input_data)

    try:
        probability = model.predict_proba(input_data)[0][1]
    except:
        probability = None

    return jsonify({
        "prediction": int(prediction[0]),
        "probability": float(probability) if probability is not None else None,
        "missing": missing
    })




if __name__ == '__main__':
    app.run(debug=True)




# PREDICT PERO EN GET 

@app.route('/api/v1/predict', methods=["GET"])
def predict_get():
    args = {k.lower(): v for k, v in request.args.items()}

    
    sexo = args.get('sexo')
    novel = args.get('novel')
    edad = args.get('edad')
    num_infracciones = args.get('num_infracciones')  

   
    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return np.nan

    sexo = to_float(sexo)
    novel = to_float(novel)
    edad = to_float(edad)
    num_infracciones = to_float(num_infracciones)

    # Comprobaciones
    errors = []

    if not np.isnan(sexo) and sexo not in (0.0, 1.0):
        errors.append("SEXO debe ser 0 o 1")

    if not np.isnan(novel) and novel not in (0.0, 1.0):
        errors.append("NOVEL debe ser 0 o 1")

    if not np.isnan(edad) and edad not in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        errors.append("EDAD debe ser un número entre 1 y 6")

    if errors:
        return jsonify({'error': errors}), 400

    # Detectar missing correctamente
    missing = [
        name for name, val in [
            ('SEXO', sexo),
            ('NOVEL', novel),
            ('EDAD', edad),
            ('NUM_INFRACCIONES', num_infracciones)
        ]
        if np.isnan(val)
    ]

    if missing:
        return jsonify({
            "error": "Faltan variables obligatorias",  # No puede predecir si hay missing
            "missing": missing
        }), 400


    # Crear DataFrame
    input_data = pd.DataFrame({
        'SEXO': [sexo],
        'NOVEL': [novel],
        'EDAD': [edad],
        'NUM_INFRACCIONES': [num_infracciones]
    })

    prediction = model.predict(input_data)

    # Convertir a tipo Python 
    response = {
        "prediction": int(prediction[0]),
        "missing": missing
    }

    return jsonify(response)



# PREDICT PERO EN POST (Body)

@app.route('/api/v1/predict', methods=["POST"])
def predict_post():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No se ha enviado JSON"}), 400

    args = {k.lower(): v for k, v in data.items()}

    sexo = args.get('sexo')
    novel = args.get('novel')
    edad = args.get('edad')
    num_infracciones = args.get('num_infracciones')

    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return np.nan

    sexo = to_float(sexo)
    novel = to_float(novel)
    edad = to_float(edad)
    num_infracciones = to_float(num_infracciones)

    errors = []

    if not np.isnan(sexo) and sexo not in (0.0, 1.0):
        errors.append("SEXO debe ser 0 o 1")

    if not np.isnan(novel) and novel not in (0.0, 1.0):
        errors.append("NOVEL debe ser 0 o 1")

    if not np.isnan(edad) and edad not in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        errors.append("EDAD debe ser un número entre 1 y 6")

    if errors:
        return jsonify({'error': errors}), 400

    missing = [
        name for name, val in [
            ('SEXO', sexo),
            ('NOVEL', novel),
            ('EDAD', edad),
            ('NUM_INFRACCIONES', num_infracciones)
        ]
        if np.isnan(val)
    ]

    if missing:
        return jsonify({
            "error": "Faltan variables obligatorias",
            "missing": missing
        }), 400

    input_data = pd.DataFrame({
        'SEXO': [sexo],
        'NOVEL': [novel],
        'EDAD': [edad],
        'NUM_INFRACCIONES': [num_infracciones]
    })

    prediction = model.predict(input_data)

    try:
        probability = model.predict_proba(input_data)[0][1]
    except:
        probability = None

    return jsonify({
        "prediction": int(prediction[0]),
        "probability": float(probability) if probability is not None else None,
        "missing": missing
    })




if __name__ == '__main__':
    app.run(debug=True)
