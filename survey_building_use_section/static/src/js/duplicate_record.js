odoo.define('survey_building_use_section.duplicate_record', function (require) {
    'use strict';

    // Definir la función para agregar la columna y el botón de duplicación de registros
    function addDuplicateButton() {
        var $body = $('body');

        // Check if the conditions are met to add the column and button
        if (this.props.list.resModel === "survey.question.article") {
            // Add a new column header for "Duplicate"
            var $headerCell = $('<th>', {
                class: 'o_list_record_selector'
            }).append($('<span>', {
                class: 'o_checkbox'
            }));
            this.columns.forEach(function (column) {
                var $th = $('<th>', {
                    class: 'o_column_sortable',
                    role: 'columnheader',
                    name: column.id,
                }).text(column.string);
                $headerCell.after($th);
            });
            $body.find('thead tr').prepend($headerCell);

            // Add a button for each row to duplicate the record
            $body.find('tbody tr').each(function () {
                var $row = $(this);
                var recordId = parseInt($row.data('id'), 10);
                var $buttonCell = $('<td>', {
                    class: 'o_list_record_selector'
                }).append($('<button>', {
                    class: 'o_duplicate_button btn btn-sm btn-default',
                    text: 'Duplicate'
                }).on('click', function () {
                    // Aquí llama a la función _duplicateRecord con recordId
                    // this._duplicateRecord(recordId);
                    // Para acceder al contexto correcto, puedes almacenar el valor de `this` en una variable.
                    var self = this;
                    console.log("Duplicate button clicked for record with ID:", recordId);
                    self._duplicateRecord(recordId);
                }));
                $row.prepend($buttonCell);
            });
        }
    }

    // Añadir un event listener para ejecutar la función cuando la página esté completamente cargada
    document.addEventListener('DOMContentLoaded', function() {
        // Obtener la instancia del ListRenderer y ejecutar la función addDuplicateButton
        var listRenderer = new Object();
        listRenderer.props = {
            list: {
                resModel: "survey.question.article" // Puedes establecer la propiedad resModel según tus necesidades
            },
            columns: [
                // Aquí puedes definir las columnas según tu estructura de datos
            ]
        };
        addDuplicateButton.call(listRenderer);
    });
});
