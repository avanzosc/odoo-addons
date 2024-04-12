odoo.define('survey_building_use_section.th_articles_width', function (require) {
    "use strict";

    var core = require('web.core');

    // Función para verificar si la URL contiene el parámetro model=survey
    function checkURLParameter() {
        var urlParams = new URLSearchParams(window.location.search);
        return urlParams.has('model') && urlParams.get('model') === 'survey';
    }

    // Verificar si la URL contiene el parámetro model=survey
    if (checkURLParameter()) {
        // Obtener todos los elementos th en la página
        var thElements = document.getElementsByTagName('th');

        // Iterar sobre los elementos th
        for (var i = 0; i < thElements.length; i++) {
            // Verificar si el atributo data-name es "question_article_ids"
            if (thElements[i].getAttribute('data-name') === "question_article_ids") {
                // Obtener el estilo actual del elemento th
                var currentStyle = thElements[i].getAttribute('style');
                // Verificar si el estilo actual está definido
                if (currentStyle) {
                    // Agregar 500px al estilo actual
                    thElements[i].setAttribute('style', currentStyle + ' width: 876px;');
                } else {
                    // Si el estilo no está definido, establecer un nuevo estilo con 500px de ancho
                    thElements[i].setAttribute('style', 'width: 876px;');
                }
                // Detener el bucle después de encontrar el primer elemento que cumpla con la condición
                break;
            }
        }
    }
});

