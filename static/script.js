
  function removeSecondsFromDatetimeInputs() {
    // Obtener los inputs de tipo datetime-local
    const datetimeInputs = document.querySelectorAll('input[type=datetime-local]');

    // Iterar sobre los inputs y modificar su valor
    datetimeInputs.forEach(input => {
      const datetimeValue = input.value;
      const valueWithoutSeconds = datetimeValue.substring(0, datetimeValue.length - 3) + '00';
      input.value = valueWithoutSeconds;
    });
  }

  // Llamar a la función cuando se cargue la página
  window.addEventListener('load', removeSecondsFromDatetimeInputs);
