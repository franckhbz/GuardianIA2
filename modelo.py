import joblib
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

def generar_ejemplo():
    situaciones = ["Cruce de Peatones", "Congestión de Tráfico", "Semáforo en Rojo", "Semáforo en Verde"]
    condiciones_climaticas = ["Soleado", "Lluvioso", "Nublado"]
    num_pasajeros = random.choice([1, 2, 3, 4])
    visibilidad = ["Buena", "Reducida"]
    velocidad = random.randint(0, 60)  # Velocidad en km/h

    situacion = random.choice(situaciones)
    clima = random.choice(condiciones_climaticas)
    visibilidad_actual = random.choice(visibilidad)

    # Agregar lógica para la decisión correcta en caso de semáforo en verde y cruces de peatones
    if situacion == "Semáforo en Verde" and "Cruce de Peatones" in situacion:
        decision_correcta = "Detenerse"
    elif situacion == "Semáforo en Verde" :
        decision_correcta = "Continuar"
    elif situacion == "Cruce de Peatones":
        decision_correcta = "Detenerse y dar paso al peatón"
    elif situacion == "Congestión de Tráfico":
        if velocidad > 20:
          decision_correcta = "bajar la velocidad y Esperar en el atasco"
        else:
          decision_correcta = "Esperar en el atasco"
    elif situacion == "Semáforo en Rojo":
        decision_correcta = "Detenerse"
    else:
        decision_correcta = "Continuar"


    ejemplo = {
        "Situación de Tráfico": situacion,
        "Condiciones Climáticas": clima,
        "Número de Pasajeros": f"{num_pasajeros} pasajeros",
        "Visibilidad": visibilidad_actual,
        "Velocidad (km/h)": velocidad,
        "Decisión Ética Correcta": decision_correcta
    }

    return ejemplo

# Generar 20 ejemplos de datos
datos_generados = [generar_ejemplo() for _ in range(100000)]
data = pd.DataFrame(datos_generados)
X = data[['Situación de Tráfico', 'Condiciones Climáticas', 'Número de Pasajeros', 'Visibilidad', 'Velocidad (km/h)']]
y = data['Decisión Ética Correcta']

# Realizar codificación one-hot para las variables categóricas
X = pd.get_dummies(X)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Normalizar los datos
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Modelos
perceptron_model = Perceptron()
rf_model = RandomForestClassifier(random_state=42)

# Entrenar los modelos
perceptron_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
perceptron_pred = perceptron_model.predict(X_test)
rf_pred = rf_model.predict(X_test)

# Calcular las precisiones de los modelos
perceptron_accuracy = accuracy_score(y_test, perceptron_pred)
rf_accuracy = accuracy_score(y_test, rf_pred)

scaler.fit(X_train)
joblib.dump(rf_model, 'modelo_rf.pkl')
joblib.dump(scaler, 'scaler.pkl')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer

# Datos de entrenamiento
textos = [
      "Un grupo de personas cruza la calle cuando el semáforo está en verde.",
      "Intersección con una manifestación de ciclistas bloqueando el tráfico.",
      "Semáforo en rojo en una intersección congestionada.",
      "Congestión de tráfico debido a un accidente en la autopista.",
      "Cruce de peatones en una intersección muy transitada.",
      "El semáforo cambió a verde y el tráfico fluye.",
      "Accidente de tráfico en una carretera principal.",
      "Manifestación de ciclistas bloqueando el tráfico en el centro de la ciudad.",
      "Calle cerrada debido a un desfile.",
      "Semáforo en verde y tráfico fluido en la avenida principal.",
      "Tráfico lento en la hora pico de la tarde.",
      "Cruce de peatones cerca de una escuela.",
      "Tráfico detenido debido a una construcción en la carretera.",
      "Manifestación de ciclistas en la avenida principal.",
      "Situación de tráfico normal en la ciudad.",
      "El semáforo cambió a rojo, y los autos se detuvieron.",
      "Accidente de tráfico en la intersección.",
      "Cruce de peatones en una zona residencial.",
      "Tráfico pesado en la carretera durante las vacaciones.",
      "Semáforo en verde en la zona comercial.",
      "Congestión de tráfico en el centro de la ciudad.",
      "Semáforo en rojo en la intersección peatonal.",
      "Tráfico fluido en la autopista.",
      "Cruce de peatones en una zona escolar.",
      "Desvío de tráfico debido a reparaciones en la carretera.",
      "Manifestación de ciclistas en el parque.",
      "Tráfico lento en una avenida principal.",
      "Calle cerrada por un evento especial.",
      "Semáforo en verde en la hora punta de la mañana.",
      "Tráfico pesado en la carretera después de un partido de fútbol."
]

etiquetas = [
    ["Situación de Tráfico_Cruce de Peatones", "Situación de Tráfico_Semáforo en Verde"],
    ["Situación de Tráfico_Congestión de Tráfico", "Situación de Tráfico_Manifestación de Ciclistas"],
    ["Situación de Tráfico_Semáforo en Rojo"],
    ["Situación de Tráfico_Congestión de Tráfico", "Situación de Tráfico_Accidente de Tráfico"],
    ["Situación de Tráfico_Cruce de Peatones"],
    ["Situación de Tráfico_Semáforo en Verde"],
    ["Situación de Tráfico_Accidente de Tráfico"],
    ["Situación de Tráfico_Manifestación de Ciclistas"],
    ["Situación de Tráfico_Cierre de Calle"],
    ["Situación de Tráfico_Semáforo en Verde"],
    ["Situación de Tráfico_Tráfico en Hora Pico"],
    ["Situación de Tráfico_Cruce de Peatones"],
    ["Situación de Tráfico_Obra en la Carretera"],
    ["Situación de Tráfico_Manifestación de Ciclistas"],
    ["Situación de Tráfico_Normal"],
    ["Situación de Tráfico_Semáforo en Rojo"],
    ["Situación de Tráfico_Accidente de Tráfico"],
    ["Situación de Tráfico_Cruce de Peatones"],
    ["Situación de Tráfico_Tráfico Pesado"],
    ["Situación de Tráfico_Semáforo en Verde"],
    ["Situación de Tráfico_Congestión de Tráfico"],
    ["Situación de Tráfico_Semáforo en Rojo"],
    ["Situación de Tráfico_Tráfico Fluido"],
    ["Situación de Tráfico_Cruce de Peatones"],
    ["Situación de Tráfico_Obra en la Carretera"],
    ["Situación de Tráfico_Manifestación de Ciclistas"],
    ["Situación de Tráfico_Tráfico Lento"],
    ["Situación de Tráfico_Cierre de Calle"],
    ["Situación de Tráfico_Semáforo en Verde"],
    ["Situación de Tráfico_Tráfico Pesado"]
]

# Crear el vectorizador BoW
vectorizer = CountVectorizer()

# Transformar los textos en vectores de características
X = vectorizer.fit_transform(textos)

# Inicializar MultiLabelBinarizer y transformar las etiquetas
mlb = MultiLabelBinarizer()
etiquetas_binarias = mlb.fit_transform(etiquetas)

# Inicializar el modelo de clasificación (en este caso, Naive Bayes) para clasificación multietiqueta
clf = MultiOutputClassifier(MultinomialNB())

# Entrenar el modelo
clf.fit(X, etiquetas_binarias)

# Texto de prueba
texto_prueba = "Cinco personas cruza la calle cuando el semáforo está en verde."

# Transformar el texto de prueba en un vector de características
X_prueba = vectorizer.transform([texto_prueba])

# Hacer predicciones en el texto de prueba
predicciones = clf.predict(X_prueba)

# Convertir las predicciones a etiquetas
predicciones_etiquetas = mlb.inverse_transform(predicciones)
joblib.dump(clf, 'modelo_naive_bayes.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(mlb, 'mlb.pkl')