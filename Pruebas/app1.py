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
            <title>API Modelo ML</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f4f6f8;
                }
                h1 {
                    color: #2c3e50;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                code {
                    background: #eee;
                    padding: 5px;
                    border-radius: 5px;
                }
                pre {
                    background: #eee;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }
                ul {
                    line-height: 1.6;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚗 API de Predicción de Infracciones</h1>
                
                <p>Esta API utiliza un modelo de Machine Learning para predecir si una infracción es grave o no.</p>
                
                <h2>📌 Endpoints disponibles</h2>

                <h3>1️⃣ POST /api/v1/predict</h3>
                <p>Endpoint principal recomendado.</p>

                <h4>📥 Input (JSON)</h4>
                <pre>{
    "sexo": 1,
    "novel": 0,
    "edad": 3,
    "num_infracciones": 2
}</pre>

                <h4>📤 Output</h4>
                <pre>{
    "prediction": 1,
    "probability": 0.82,
    "missing": []
}</pre>

                <h4>Significado del output:</h4>
                <ul>
                    <li><b>prediction</b>: resultado del modelo (0 = no grave, 1 = grave)</li>
                    <li><b>probability</b>: probabilidad de que la infracción sea grave</li>
                    <li><b>missing</b>: variables no proporcionadas (vacío si todo está correcto)</li>
                </ul>

                <hr>

                <h3>2️⃣ GET /api/v1/predict</h3>
                <p>Endpoint alternativo que recibe los datos como parámetros en la URL.</p>

                <h4>📥 Input (query params)</h4>
                <pre>/api/v1/predict?sexo=1&novel=0&edad=3&num_infracciones=2</pre>

                <h4>📤 Output</h4>
                <pre>{
    "prediction": 1,
    "missing": []
}</pre>

                <h4>Significado del output:</h4>
                <ul>
                    <li><b>prediction</b>: resultado del modelo (0 = no grave, 1 = grave)</li>
                    <li><b>missing</b>: variables no proporcionadas</li>
                </ul>

                <hr>

                <h2>📊 Variables de entrada</h2>
                <ul>
                    <li><b>sexo</b>: 0 o 1</li>
                    <li><b>novel</b>: 0 o 1</li>
                    <li><b>edad</b>: valor entre 1 y 6</li>
                    <li><b>num_infracciones</b>: número de infracciones</li>
                </ul>

                <h2>⚠️ Notas</h2>
                <ul>
                    <li>Todos los campos son obligatorios</li>
                    <li>Los valores deben cumplir las restricciones indicadas</li>
                    <li>Si faltan datos, la API devolverá un error indicando qué variables faltan</li>
                </ul>

                <hr>
                <p>👨‍💻 API desarrollada con Flask</p>
            </div>
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
