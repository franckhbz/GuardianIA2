from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer
import logging

try:
    # Cargar el modelo Random Forest
    rf_model = joblib.load('modelo_rf.pkl')
    scaler = joblib.load("scaler.pkl")
    # Cargar el modelo Naive Bayes
    clf = joblib.load('modelo_naive_bayes.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    mlb = joblib.load('mlb.pkl')
except Exception as e:
    print(f"Error al cargar modelos u objetos: {str(e)}")


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('guardian.html')


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()

    # Obtener respuestas del modelo 1
    respuestas_usuario = data.get('respuestasUsuario', None)

    # Obtener pregunta para el modelo 2
    pregunta_modelo2 = data.get('pregunta', None)

    if respuestas_usuario is not None and pregunta_modelo2 is not None:
        X_prueba = vectorizer.transform([pregunta_modelo2])

        # Hacer predicciones en el texto de pregunta
        predicciones = clf.predict(X_prueba)
        # Convertir las predicciones a etiquetas
        predicciones_etiquetas = mlb.inverse_transform(predicciones)

        for etiquetas in predicciones_etiquetas:
            for etiqueta in etiquetas:
                respuestas_usuario[etiqueta] = 1
        # Devolver una respuesta que incluye las etiquetas predichas por el modelo Naive Bayes
        # Transformar el objeto de respuestas del usuario en un DataFrame
        respuestas_df = pd.DataFrame([respuestas_usuario])

        # Normalizar las respuestas del usuario utilizando el mismo escalador que se utilizó para los datos de entrenamiento y prueba
        respuestas_norm = scaler.transform(respuestas_df)

        # Realizar predicciones con el modelo Random Forest
        rf_pred = rf_model.predict(respuestas_norm)

        # Obtener las decisiones éticas predichas por el modelo Random Forest
        decision_rf = rf_pred[0]

        # Transformar el texto de pregunta en un vector de características
        
        return jsonify({'response': decision_rf})

    else:
        # Manejar el caso en el que no se proporcionan respuestas del usuario ni una pregunta
        return jsonify({'error': 'No se proporcionaron datos válidos'}), 400


@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Error al cargar modelos u objetos: {str(e)}")
    return jsonify({'error': 'Ocurrió un error en el servidor'}), 500

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
