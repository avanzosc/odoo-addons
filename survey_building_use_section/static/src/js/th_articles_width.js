odoo.define('survey_building_use_section.th_articles_width', function (require) {
    "use strict";

    import { surveyForm } from 'survey.form'; // Importar el módulo survey.form

    var core = require('web.core');

    // Función para verificar si la URL contiene el parámetro model=survey
    function checkURLParameter() {
        var urlParams = new URLSearchParams(window.location.search);
        return urlParams.has('model') && urlParams.get('model').startsWith('survey');
    }

    // Verificar si la URL contiene el parámetro model=survey
    if (checkURLParameter()) {
        // Agregar event listener para el evento click en los elementos <tr>
        document.addEventListener('click', function(event) {
            var target = event.target;
            // Verificar si el elemento clickeado es un <tr>
            if (target.tagName === 'TR') {
                console.log("Clicked TR in a survey page");
                // Obtener todos los elementos th en la página
                var thElements = document.getElementsByTagName('th');

                // Iterar sobre los elementos th
                for (var i = 0; i < thElements.length; i++) {
                    // Verificar si el atributo data-name es "question_article_ids" o "value"
                    if (thElements[i].getAttribute('data-name') === "question_article_ids") {
                        // Obtener el estilo actual del elemento th
                        var currentStyle = thElements[i].getAttribute('style');
                        console.log("Current style for question_article_ids:", currentStyle);
                        // Verificar si el estilo actual está definido
                        if (currentStyle) {
                            // Agregar 500px al estilo actual
                            thElements[i].style.width = (parseInt(thElements[i].style.width) + 500) + 'px';
                            console.log("Adjusted width for question_article_ids:", thElements[i].style.width);
                        } else {
                            // Si el estilo no está definido, establecer un nuevo estilo con 500px de ancho
                            thElements[i].style.width = '500px';
                            console.log("Set new width for question_article_ids:", thElements[i].style.width);
                        }
                    } else if (thElements[i].getAttribute('data-name') === "value") {
                        // Obtener el estilo actual del elemento th
                        var currentStyle = thElements[i].getAttribute('style');
                        console.log("Current style for value:", currentStyle);
                        // Verificar si el estilo actual está definido
                        if (currentStyle) {
                            // Quitar 400px del ancho actual
                            thElements[i].style.width = (parseInt(thElements[i].style.width) - 400) + 'px';
                            console.log("Adjusted width for value:", thElements[i].style.width);
                        } else {
                            // Si el estilo no está definido, establecer un nuevo estilo con 400px menos de ancho
                            thElements[i].style.width = '100px'; // Set default width if style not defined
                            console.log("Set new width for value:", thElements[i].style.width);
                        }
                    }
                }
            }
        });
    }
});
