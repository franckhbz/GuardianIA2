const respuestasUsuario = {
    "Situación de Tráfico_Semáforo en Verde": 0,
    "Situación de Tráfico_Congestión de Tráfico": 0,
    "Situación de Tráfico_Cruce de Peatones": 0,
    "Situación de Tráfico_Semáforo en Rojo": 0,
    "Condiciones Climáticas_Lluvioso": 0,
    "Condiciones Climáticas_Nublado": 0,
    "Condiciones Climáticas_Soleado": 0,
    "Número de Pasajeros_1 pasajeros": 0,
    "Número de Pasajeros_2 pasajeros": 0,
    "Número de Pasajeros_3 pasajeros": 0,
    "Número de Pasajeros_4 pasajeros": 0,
    "Visibilidad_Reducida": 0,
    "Visibilidad_Buena": 0,
    "Velocidad (km/h)": 0
};

const respuestasUsuario2={

  "Situación Ambiental_Adopción de Prácticas Sostenibles": 0,
    "Situación Ambiental_Restauración de Hábitats Naturales": 0,
    "Situación Ambiental_Explotación de Recursos Naturales": 0,
    "Situación Ambiental_Gestión de Residuos Peligrosos": 0,
    "Situación Ambiental_Preservación de Especies en Peligro": 0,
    "Situación Ambiental_Conservación de Ecosistemas": 0,
    "Situación Ambiental_Contaminación Acuática": 0,
    "Situación Ambiental_Moderado": 0,
  "Número de personas 1": 0,
  "Número de personas 2": 0,
  "Número de personas 3": 0,
  "Número de personas 4": 0,
  "Riesgo Ambiental_Alto":0,
  "Riesgo Ambiental_Moderado":0,
  "Riesgo Ambiental_Bajo":0,
  "Impacto Ambiental (%)":0,
  "Inversion Financiera $":0,
  "Impacto en Aguas_Alto":0,
  "Impacto en Aguas_Moderado":0,
  "Impacto en Aguas_Bajo":0,
  "Eficiencia Energetica":0



}
  function cambiarImagen(nuevaImagen, soundId) {
  var imagen = document.getElementById('imagenGuardian');
  var sound = document.getElementById(soundId);
  imagen.src = nuevaImagen;
  
  // Reproducir el sonido
  sound.play();


  // Añadir una clase para la animación
   // Remover y volver a agregar la clase para reiniciar la animación
   imagen.classList.remove('animacion-imagen');
  void imagen.offsetWidth; // Truco para reiniciar la animación
  imagen.classList.add('animacion-imagen');
}
function seleccionarRespuesta(option) {
    const opcionesPregunta = option.parentNode.querySelectorAll('.option-button');
    opcionesPregunta.forEach((opcion) => opcion.classList.remove('selected'));

    // Activar la clase "selected" en la opción seleccionada
    option.classList.add('selected');
    // Obtener el valor de la respuesta seleccionada
    const respuesta = option.getAttribute('data-answer');
    
    // Obtener el nombre de la pregunta
    const pregunta = option.parentNode.previousElementSibling.querySelector('p').textContent;

    // Actualizar el objeto de respuestas del usuario
    respuestasUsuario[`${pregunta}_${respuesta}`] = 1;
}

async function enviarRespuesta() {
    // Obtener la velocidad ingresada por el usuario
    const velocidad = document.getElementById('numeroRespuesta').value;
    // Obtener la pregunta ingresada por el usuario
    const pregunta = document.getElementById('textoInput').value;

    // Actualizar el objeto de respuestas del usuario con la velocidad
    respuestasUsuario["Velocidad (km/h)"] = parseInt(velocidad);

    // Crear un objeto que contenga tanto la pregunta como las respuestas
    const dataToSend = {
        pregunta: pregunta,
        respuestasUsuario: respuestasUsuario
    };

    // Imprimir los datos en la consola para depuración
    console.log('Datos enviados al servidor:', dataToSend);

    // Enviar los datos formateados al servidor
    fetch('/ask', {
        method: 'POST',
        body: JSON.stringify(dataToSend),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Procesar la respuesta del servidor aquí
        console.log(data);
        // Llamar a una función que procese la respuesta combinada si es necesario
        procesarRespuestaCombinada(data);
    });
    try {
        const response = await fetch('/ask', {
          method: 'POST',
          body: JSON.stringify(dataToSend),
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const data = await response.json();
        procesarRespuestaCombinada(data);
      } catch (error) {
        console.error('Ocurrió un error al enviar los datos:', error);
      }
    // Evitar que el formulario se envíe de forma convencional
    return false;
}

// Función para procesar la respuesta combinada
function procesarRespuestaCombinada(data) {
    // Aquí puedes procesar la respuesta combinada de ambos envíos
    // data contiene la respuesta del servidor que incluye la respuesta del segundo modelo
    console.log('Procesando respuesta combinada:', data);
    // Realiza cualquier lógica necesaria para procesar la respuesta combinada
    // Puedes acceder a data.respuesta para obtener la respuesta final
    const respuestaFinal = data.response;
    // Actualiza el elemento de respuesta en tu página
    document.getElementById('respuestaTexto').textContent = respuestaFinal;
}




function seleccionar(option) {
  // Desactivar la clase "selected" en todas las opciones de la misma pregunta
  
  const opcionesPregunta = option.parentNode.querySelectorAll('.cuadrado');

  opcionesPregunta.forEach((opcion) => opcion.classList.remove('selected'));

  // Activar la clase "selected" en la opción seleccionada
  option.classList.add('selected');
}




// Función para cambiar las preguntas y opciones en el cuadro central
function cambiarPreguntas(opcion) {
    const cuadroCentral = document.getElementById("cuadroCentral");
  
    if (cuadroCentral) {
      if (opcion === 1) {
        cuadroCentral.innerHTML = `
        <h2>La pregunta es</h2>
        <!-- Pregunta 1 -->
        <div class="question">
          <p>Condiciones Climáticas</p>
        </div>
        <!-- Opciones de Pregunta 1 -->
        <!-- para el modelo 1 -->
        <div class="options">
          <div class="option-button" data-answer="Lluvioso" onclick="seleccionarRespuesta(this)">Lluvioso</div>
          <div class="option-button" data-answer="Nublado" onclick="seleccionarRespuesta(this)">Nublado</div>
          <div class="option-button" data-answer="Soleado" onclick="seleccionarRespuesta(this)">Soleado</div>
        </div>
        
        <!-- Pregunta 2 -->
        <div class="question">
          <!-- para el modelo 1 -->
          <p>Número de Pasajeros</p>
        </div>
        <!-- Opciones de Pregunta 2 -->
        <div class="options">
          <!-- para el modelo 1 -->
          <div class="option-button" data-answer="1 pasajeros" onclick="seleccionarRespuesta(this)">1</div>
          <div class="option-button" data-answer="2 pasajeros" onclick="seleccionarRespuesta(this)">2</div>
          <div class="option-button" data-answer="3 pasajeros" onclick="seleccionarRespuesta(this)">3</div>
          <div class="option-button" data-answer="4 pasajeros" onclick="seleccionarRespuesta(this)">4</div>
        </div>
    
        <!-- Pregunta 3 -->
        <div class="question">
          <p>Visibilidad</p>
        </div>
        <!-- Opciones de Pregunta 3 -->
        <div class="options">
          <!-- para el modelo 1 -->
          <div class="option-button" data-answer="Reducida" onclick="seleccionarRespuesta(this)">REDUCIDA</div>
          <div class="option-button" data-answer="Buena" onclick="seleccionarRespuesta(this)">BUENA</div>
        </div>
        
        <!-- Pregunta 4 con opción para ingresar un número -->
        <div class="question">
          <p>Velocidad</p>
        </div>
        <!-- Opciones de Pregunta 4 -->
        <div class="options">
          <!-- para el modelo 1 -->
          <input type="number" id="numeroRespuesta">
          
        </div>
          `;
      } else if (opcion === 2) {
        cuadroCentral.innerHTML = `
        
        <h2>La pregunta es</h2>

        <!-- Pregunta 1 -->
        <div class="question">
          <p>RIESGO AMBIENTAL</p>
        </div>
        <!-- Opciones de Pregunta 1 -->
        <div class="options">
          <div class="option-button" data-answer="Lluvioso" onclick="seleccionarRespuesta(this)">ALTO</div>
          <div class="option-button" data-answer="Nublado" onclick="seleccionarRespuesta(this)">MODERADO</div>
          <div class="option-button" data-answer="Soleado" onclick="seleccionarRespuesta(this)">BAJO</div>
        </div>
        
        <!-- Pregunta 2 -->
        <div class="question">
          <p>NUMERO DE PERSONAS</p>
        </div>
        <!-- Opciones de Pregunta 2 -->
        <div class="options">
          <div class="option-button" data-answer="1" onclick="seleccionarRespuesta(this)">1</div>
          <div class="option-button" data-answer="2" onclick="seleccionarRespuesta(this)">2</div>
          <div class="option-button" data-answer="3" onclick="seleccionarRespuesta(this)">3</div>
          <div class="option-button" data-answer="4" onclick="seleccionarRespuesta(this)">4</div>
          <div class="option-button" data-answer="4" onclick="seleccionarRespuesta(this)">5</div>
        </div>
    
        <!-- Pregunta 3 -->
        <div class="question">
          <p>IMPACTO EN AGUAS</p>
        </div>
        <!-- Opciones de Pregunta 3 -->
        <div class="options">
          <div class="option-button" data-answer="Reducida" onclick="seleccionarRespuesta(this)">ALTO</div>
          <div class="option-button" data-answer="Buena" onclick="seleccionarRespuesta(this)">MODERADO</div>
          <div class="option-button" data-answer="Buena" onclick="seleccionarRespuesta(this)">BAJO</div>
        </div>
        
        <!-- Pregunta 4 con opción para ingresar un número -->
        <div class="question">
          <p>IMPACTO AMBIENTAL %</p>
        </div>
        <!-- Opciones de Pregunta 4 -->
        <div class="options">
          <input type="number" id="numeroRespuesta"  min="1" max="100">
          
        </div>


        <div class="question">
          <p>INVERSION FINANCIERA%</p>
        </div>
        <!-- Opciones de Pregunta 5 -->
        <div class="options">
          <input type="number" id="numeroRespuesta" >
          
        </div>

        <div class="question">
          <p>EFICENCIA ENERGETICA 0.5 - 1%</p>
        </div>
        <!-- Opciones de Pregunta 6 -->
        <div class="options">
          <input type="number" id="numeroRespuesta" min="0.5" max="1">
          
        </div>

          `;
      } 
    }
  }