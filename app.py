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
#from waitress import serve
try:
#Trafico
    # Cargar el modelo Perceptron
    tperceptron_model = joblib.load('trafficmodel/tperceptron_model.pkl')
    tscaler = joblib.load("trafficmodel/tscaler.pkl")
    # Cargar el modelo Naive Bayes
    tclf = joblib.load('trafficmodel/tmodelo_naive_bayes.pkl')
    tvectorizer = joblib.load('trafficmodel/tvectorizer.pkl')
    tmlb = joblib.load('trafficmodel/tmlb.pkl')
#Ambiente
    aperceptron_model = joblib.load('ambientmodel/aperceptron_model.pkl')
    ascaler = joblib.load("ambientmodel/ascaler.pkl")
    # Cargar el modelo Naive Bayes
    aclf = joblib.load('ambientmodel/amodelo_naive_bayes.pkl')
    avectorizer = joblib.load('ambientmodel/avectorizer.pkl')
    amlb = joblib.load('ambientmodel/amlb.pkl')
except Exception as e:
    print(f"Error al cargar modelos u objetos: {str(e)}")


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('guardian.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    print("Ruta /ask ta bien")
    data = request.get_json()
    # Obtener respuestas del modelo 1
    respuestas_usuario = data.get('respuestasUsuario', None)
    # Obtener pregunta para el modelo 2
    pregunta_modelo2 = data.get('pregunta', None)
    
    if respuestas_usuario is not None and pregunta_modelo2 is not None:
        X_prueba = tvectorizer.transform([pregunta_modelo2])

        # Hacer predicciones en el texto de pregunta
        predicciones = tclf.predict(X_prueba)
        # Convertir las predicciones a etiquetas
        predicciones_etiquetas = tmlb.inverse_transform(predicciones)

        for etiquetas in predicciones_etiquetas:
            for etiqueta in etiquetas:
                respuestas_usuario[etiqueta] = 1
        # Devolver una respuesta que incluye las etiquetas predichas por el modelo Naive Bayes
        # Transformar el objeto de respuestas del usuario en un DataFrame
        respuestas_df = pd.DataFrame([respuestas_usuario])

        # Normalizar las respuestas del usuario utilizando el mismo escalador que se utilizó para los datos de entrenamiento y prueba
        respuestas_norm = tscaler.transform(respuestas_df)

        # Realizar predicciones con el modelo Random Forest
        perceptron_pred = tperceptron_model.predict(respuestas_norm)

        # Obtener las decisiones éticas predichas por el modelo Random Forest
        decision_perceptron = perceptron_pred[0]

        # Transformar el texto de pregunta en un vector de características
        
        return jsonify({'response': decision_perceptron})

    else:
        # Manejar el caso en el que no se proporcionan respuestas del usuario ni una pregunta
        return jsonify({'error': 'No se proporcionaron datos válidos'}), 400

@app.route('/ask_ambiental', methods=['POST'])
def ask_ambiental():
    data = request.get_json()

    # Obtener respuestas del modelo 1
    respuestas_usuario = data.get('respuestasUsuario2', None)

    # Obtener pregunta para el modelo 2
    pregunta_modelo2 = data.get('pregunta', None)

    if respuestas_usuario is not None and pregunta_modelo2 is not None:
        X_prueba = avectorizer.transform([pregunta_modelo2])

        # Hacer predicciones en el texto de pregunta
        predicciones = aclf.predict(X_prueba)
        # Convertir las predicciones a etiquetas
        predicciones_etiquetas = amlb.inverse_transform(predicciones)

        for etiquetas in predicciones_etiquetas:
            for etiqueta in etiquetas:
                respuestas_usuario[etiqueta] = 1
        # Devolver una respuesta que incluye las etiquetas predichas por el modelo Naive Bayes
        # Transformar el objeto de respuestas del usuario en un DataFrame
        respuestas_df = pd.DataFrame([respuestas_usuario])

        # Normalizar las respuestas del usuario utilizando el mismo escalador que se utilizó para los datos de entrenamiento y prueba
        respuestas_norm = ascaler.transform(respuestas_df)

        # Realizar predicciones con el modelo Random Forest
        perceptron_pred = aperceptron_model.predict(respuestas_norm)

        # Obtener las decisiones éticas predichas por el modelo Random Forest
        decision_perceptron = perceptron_pred[0]

        # Transformar el texto de pregunta en un vector de características
        
        return jsonify({'response': decision_perceptron})

    else:
        # Manejar el caso en el que no se proporcionan respuestas del usuario ni una pregunta
        return jsonify({'error': 'No se proporcionaron datos válidos'}), 400

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Error al cargar modelos u objetos: {str(e)}")
    return jsonify({'error': 'Ocurrió un error en el servidor'}), 500

#if __name__ == "__main__":
    #serve(app, host="0.0.0.0", port=8080)
