import joblib
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
def generar_ejemplo_ambiental():
    situaciones_ambientales = [
        "Explotación de Recursos Naturales",
        "Adopción de Prácticas Sostenibles",
        "Conservación de Ecosistemas",
        "Gestión de Residuos Peligrosos",
        "Desarrollo de Energías Renovables",
        "Preservación de Especies en Peligro",
        "Contaminación Acuática",
        "Restauración de Hábitats Naturales"
    ]
    num_personas_involucradas = random.choice([1, 2, 3, 4, 5])
    impacto_ambiental = random.randint(0, 100)  # Impacto ambiental (valor hipotético)
    inversion_financiera = random.randint(10000, 1000000)  # Inversión financiera requerida
    riesgo_ambiental = random.choice(["Bajo", "Moderado", "Alto"])  # Nivel de riesgo ambiental
    impacto_acuatico = random.choice(["Bajo", "Moderado", "Alto"])  # Nivel de impacto en los cuerpos de agua
    eficiencia_energetica = random.uniform(0.5, 1.0)  # Nivel de eficiencia energética

    situacion_ambiental = random.choice(situaciones_ambientales)

    # Agregar lógica para la decisión ética correcta según la situación ambiental
    if situacion_ambiental in ["Explotación de Recursos Naturales", "Gestión de Residuos Peligrosos"]:
        decision_correcta = "Regular la actividad con restricciones ambientales estrictas"
    elif situacion_ambiental in ["Adopción de Prácticas Sostenibles", "Desarrollo de Energías Renovables"]:
        decision_correcta = "Implementar prácticas sostenibles para reducir el impacto ambiental"
    elif situacion_ambiental in ["Conservación de Ecosistemas", "Preservación de Especies en Peligro"]:
        decision_correcta = "Preservar el ecosistema y hábitat natural"
    elif situacion_ambiental == "Contaminación Acuática":
        decision_correcta = "Restringir o eliminar fuentes de contaminación para restaurar cuerpos de agua"
    elif situacion_ambiental == "Restauración de Hábitats Naturales":
        decision_correcta = "Recuperar y preservar hábitats ecológicos para especies locales"
    else:
        decision_correcta = "Sin acción específica"

    ejemplo_ambiental = {
        "Situación Ambiental": situacion_ambiental,
        "Personas Involucradas": f"{num_personas_involucradas} personas",
        "Impacto Ambiental (% de impacto)": impacto_ambiental,
        "Inversión Financiera ($)": inversion_financiera,
        "Riesgo Ambiental": riesgo_ambiental,
        "Impacto en Aguas": impacto_acuatico,
        "Eficiencia Energética (%eficiente)": eficiencia_energetica ,
        "Decisión Ética Correcta": decision_correcta
    }

    return ejemplo_ambiental

# Generar 20 ejemplos de datos relacionados con cuestiones ambientales
datos_ambientales_generados = [generar_ejemplo_ambiental() for _ in range(10000)]


data = pd.DataFrame(datos_ambientales_generados)
X = data[['Situación Ambiental','Personas Involucradas', 'Impacto Ambiental (% de impacto)','Inversión Financiera ($)','Riesgo Ambiental', 'Impacto en Aguas', 'Eficiencia Energética (%eficiente)']]
y = data['Decisión Ética Correcta']

# Realizar codificación one-hot para las variables categóricas
X = pd.get_dummies(X)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
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
joblib.dump(rf_model, 'modeloa_rf.pkl')
joblib.dump(scaler, 'scalera.pkl')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MultiLabelBinarizer

# Datos de entrenamiento
textos = [
    "Restauración de ríos para preservar la vida acuática.",
    "Incidente de derrame de petróleo en el mar, afectando la fauna marina.",
    "Iniciativa de reciclaje para reducir desechos y promover la sostenibilidad.",
    "Programa de reforestación en áreas urbanas para combatir la contaminación del aire.",
    "Accidente de barcos de pesca, poniendo en riesgo la biodiversidad marina.",
    "Proyecto de parques eólicos para fomentar la energía limpia.",
    "Manifestación por la conservación de áreas verdes en la ciudad.",
    "Deterioro del suelo debido a la deforestación masiva.",
    "Inundaciones causadas por el cambio climático en zonas costeras.",
    "Protección de la fauna en peligro en su hábitat natural.",
    "Contaminación del suelo por desechos tóxicos en vertederos.",
    "Construcción de plantas de energía solar para reducir las emisiones de carbono.",
    "Crisis de sequía afectando la agricultura y recursos hídricos.",
    "Protesta contra la deforestación en zonas selváticas.",
    "Recolección de desechos electrónicos para evitar la contaminación del suelo y agua.",
    "Proyecto de restauración de manglares para proteger la biodiversidad costera.",
    "Tráfico ilegal de especies en peligro, poniendo en riesgo su existencia.",
    "Contaminación del aire por la industria pesada en áreas urbanas.",
    "Protección de humedales para mantener ecosistemas acuáticos.",
    "Planes de conservación para las abejas y otros polinizadores."
]


etiquetas = [
    ["Situación Ambiental_Adopción de Prácticas Sostenibles"],
    ["Situación Ambiental_Conservación de Ecosistemas", "Situación Ambiental_Gestión de Residuos Peligrosos"],
    ["Situación Ambiental_Restauración de Hábitats Naturales", "Situación Ambiental_Contaminación Acuática"],
    ["Situación Ambiental_Preservación de Especies en Peligro", "Situación Ambiental_Moderado"],
    ["Situación Ambiental_Explotación de Recursos Naturales"],
    ["Situación Ambiental_Gestión de Residuos Peligrosos"],
    ["Situación Ambiental_Contaminación Acuática"],
    ["Situación Ambiental_Restauración de Hábitats Naturales"],
    ["Situación Ambiental_Explotación de Recursos Naturales"],
    ["Situación Ambiental_Conservación de Ecosistemas"],
    ["Situación Ambiental_Contaminación Acuática", "Situación Ambiental_Explotación de Recursos Naturales"],
    ["Situación Ambiental_Restauración de Hábitats Naturales", "Situación Ambiental_Gestión de Residuos Peligrosos"],
    ["Situación Ambiental_Conservación de Ecosistemas", "Situación Ambiental_Adopción de Prácticas Sostenibles"],
    ["Situación Ambiental_Moderado", "Situación Ambiental_Preservación de Especies en Peligro"],
    ["Situación Ambiental_Contaminación Acuática", "Situación Ambiental_Conservación de Ecosistemas"],
    ["Situación Ambiental_Explotación de Recursos Naturales", "Situación Ambiental_Gestión de Residuos Peligrosos"],
    ["Situación Ambiental_Restauración de Hábitats Naturales", "Situación Ambiental_Adopción de Prácticas Sostenibles"],
    ["Situación Ambiental_Conservación de Ecosistemas", "Situación Ambiental_Preservación de Especies en Peligro"],
    ["Situación Ambiental_Moderado", "Situación Ambiental_Gestión de Residuos Peligrosos"],
    ["Situación Ambiental_Explotación de Recursos Naturales", "Situación Ambiental_Preservación de Especies en Peligro"]
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
texto_prueba = "Contaminación del suelo por desechos tóxicos en vertederos."

# Transformar el texto de prueba en un vector de características
X_prueba = vectorizer.transform([texto_prueba])

# Hacer predicciones en el texto de prueba
predicciones = clf.predict(X_prueba)

# Convertir las predicciones a etiquetas
predicciones_etiquetas = mlb.inverse_transform(predicciones)
joblib.dump(clf, 'modeloa_naive_bayes.pkl')
joblib.dump(vectorizer, 'vectorizera.pkl')
joblib.dump(mlb, 'mlba.pkl')

