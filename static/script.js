var opcionenvio=0;
const respuestasUsuario = {
    "Situación de Tráfico_Semáforo en Verde": 0,
    "Situación de Tráfico_Accidente de Tráfico":0,
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
    "Velocidad (km/h)": 0,
    "Urgencia a llegar a un lugar_Si":0,
    "Urgencia a llegar a un lugar_No":0
};

const respuestasUsuario2={

  "Situación Ambiental_Adopción de Prácticas Sostenibles": 0,
  "Situación Ambiental_Restauración de Hábitats Naturales": 0,
  "Situación Ambiental_Explotación de Recursos Naturales": 0,
  "Situación Ambiental_Gestión de Residuos Peligrosos": 0,
  "Situación Ambiental_Desarrollo de Energías Renovables": 0,
  "Situación Ambiental_Preservación de Especies en Peligro": 0,
  "Situación Ambiental_Conservación de Ecosistemas": 0,
  "Situación Ambiental_Contaminación Acuática": 0,
  "Personas Involucradas_1 personas": 1,
  "Personas Involucradas_2 personas": 0,
  "Personas Involucradas_3 personas": 0,
  "Personas Involucradas_4 personas": 0,
  "Personas Involucradas_5 personas": 0,
  "Impacto Ambiental (% de impacto)": 0,
  "Inversión Financiera ($)": 0,
  "Riesgo Ambiental_Alto": 0,
  "Riesgo Ambiental_Moderado": 0,
  "Riesgo Ambiental_Bajo": 0,
  "Impacto en Aguas_Alto": 0,
  "Impacto en Aguas_Moderado": 0,
  "Impacto en Aguas_Bajo": 0,
  "Eficiencia Energética (%eficiente)": 0,
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

}
async function enviarRespuesta() {
  if (opcionenvio == 1) {
    await enviarRespuestaTrafico();
  } else if (opcionenvio == 2) {
    await enviarRespuestaAmbiente();
  } else {
    return;
  }
}
async function enviarRespuestaTrafico() {
    // Obtener la velocidad ingresada por el usuario
    const velocidad = document.getElementById('velocidad').value;
    // Obtener la pregunta ingresada por el usuario
    const pregunta = document.getElementById('textoInput').value;

    // Actualizar el objeto de respuestas del usuario con la velocidad
    respuestasUsuario["Velocidad (km/h)"] = parseInt(velocidad);
    // Obtener las opciones seleccionadas
    const opcionesSeleccionadas = document.querySelectorAll('.option-button.selected');

    // Iterar sobre las opciones seleccionadas y actualizar el objeto de respuestas del usuario
    opcionesSeleccionadas.forEach((opcionSeleccionada) => {
        const respuesta = opcionSeleccionada.getAttribute('data-answer');
        const preguntaPertinente = opcionSeleccionada.parentNode.previousElementSibling.querySelector('p').textContent;
        respuestasUsuario[`${preguntaPertinente}_${respuesta}`] = 1;
    });

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

async function enviarRespuestaAmbiente() {
  // Obtener la velocidad ingresada por el usuario
  const impactambiental = document.getElementById('impactambiental').value;
  const invfinanciera = document.getElementById('invfinanciera').value;
  const eficiencia = document.getElementById('eficiencia').value;
  // Obtener la pregunta ingresada por el usuario
  const pregunta = document.getElementById('textoInput').value;

  // Actualizar el objeto de respuestas del usuario con la velocidad
  respuestasUsuario2["Impacto Ambiental (% de impacto)"] = parseInt(impactambiental);
  respuestasUsuario2["Inversión Financiera ($)"] = parseInt(invfinanciera);
  respuestasUsuario2["Eficiencia Energética (%eficiente)"] = parseInt(eficiencia);
  // Obtener las opciones seleccionadas
  const opcionesSeleccionadas = document.querySelectorAll('.option-button.selected');
  // Iterar sobre las opciones seleccionadas y actualizar el objeto de respuestas del usuario
  opcionesSeleccionadas.forEach((opcionSeleccionada) => {
      const respuesta = opcionSeleccionada.getAttribute('data-answer');
      const preguntaPertinente = opcionSeleccionada.parentNode.previousElementSibling.querySelector('p').textContent;
      respuestasUsuario2[`${preguntaPertinente}_${respuesta}`] = 1;
  });

  // Crear un objeto que contenga tanto la pregunta como las respuestas
  const dataToSend = {
      pregunta: pregunta,
      respuestasUsuario2: respuestasUsuario2
  };

  // Imprimir los datos en la consola para depuración
  console.log('Datos enviados al servidor:', dataToSend);

  // Enviar los datos formateados al servidor
  fetch('/ask_ambiental', {
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
      const response = await fetch('/ask_ambiental', {
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
    opcionenvio=opcion;
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
        <!-- Pregunta 4 -->
        <div class="question">
          <p>Urgencia a llegar a un lugar</p>
        </div>
        <!-- Opciones de Pregunta 3 -->
        <div class="options">
          <!-- para el modelo 1 -->
          <div class="option-button" data-answer="Si" onclick="seleccionarRespuesta(this)">Si</div>
          <div class="option-button" data-answer="No" onclick="seleccionarRespuesta(this)">No</div>
        </div>        
        <!-- Pregunta 5 con opción para ingresar un número -->
        <div class="question">
          <p>Velocidad</p>
        </div>
        <!-- Opciones de Pregunta 4 -->
        <div class="options">
          <!-- para el modelo 1 -->
          <input type="number" id="velocidad">
          
        </div>
          `;
      } else if (opcion === 2) {
        cuadroCentral.innerHTML = `
        
        <h2>La pregunta es</h2>

        <!-- Pregunta 1 -->
        <div class="question">
          <p>Riesgo Ambiental</p>
        </div>
        <!-- Opciones de Pregunta 1 -->
        <div class="options">
          <div class="option-button" data-answer="Alto" onclick="seleccionarRespuesta(this)">ALTO</div>
          <div class="option-button" data-answer="Moderado" onclick="seleccionarRespuesta(this)">MODERADO</div>
          <div class="option-button" data-answer="Bajo" onclick="seleccionarRespuesta(this)">BAJO</div>
        </div>
        
        <!-- Pregunta 2 -->
        <div class="question">
          <p>Personas Involucradas</p>
        </div>
        <!-- Opciones de Pregunta 2 -->
        <div class="options">
          <div class="option-button" data-answer="1 personas" onclick="seleccionarRespuesta(this)">1</div>
          <div class="option-button" data-answer="2 personas" onclick="seleccionarRespuesta(this)">2</div>
          <div class="option-button" data-answer="3 personas" onclick="seleccionarRespuesta(this)">3</div>
          <div class="option-button" data-answer="4 personas" onclick="seleccionarRespuesta(this)">4</div>
          <div class="option-button" data-answer="5 personas" onclick="seleccionarRespuesta(this)">5</div>
        </div>
    
        <!-- Pregunta 3 -->
        <div class="question">
          <p>Impacto en Aguas</p>
        </div>
        <!-- Opciones de Pregunta 3 -->
        <div class="options">
          <div class="option-button" data-answer="Alto" onclick="seleccionarRespuesta(this)">ALTO</div>
          <div class="option-button" data-answer="Moderado" onclick="seleccionarRespuesta(this)">MODERADO</div>
          <div class="option-button" data-answer="Bajo" onclick="seleccionarRespuesta(this)">BAJO</div>
        </div>
        
        <!-- Pregunta 4 con opción para ingresar un número -->
        <div class="question">
          <p>Impacto Ambiental (% de impacto)</p>
        </div>
        <!-- Opciones de Pregunta 4 -->
        <div class="options">
          <input type="number" id="impactambiental"  min="1" max="100">
          
        </div>


        <div class="question">
          <p>Inversión Financiera ($)</p>
        </div>
        <!-- Opciones de Pregunta 5 -->
        <div class="options">
          <input type="number" id="invfinanciera" >
          
        </div>
        
        <div class="question">
          <p>Eficiencia Energética (%eficiente)</p>
        </div>
        <!-- Opciones de Pregunta 6 -->
        <div class="options">
          <input type="number" id="eficiencia" min="0.5" max="1">
        </div>

          `;
      } 
    }
  }