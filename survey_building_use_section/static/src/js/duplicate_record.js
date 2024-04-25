odoo.define('survey_building_use_section.duplicate_record', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');

    var YourListRenderer = ListRenderer.extend({
        /**
         * Override to add a column and button for duplicating records.
         */
        _renderBody: function () {
            var self = this;
            var $body = this._super.apply(this, arguments);

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
                        self._duplicateRecord(recordId);
                    }));
                    $row.prepend($buttonCell);
                });
            }

            return $body;
        },

        /**
         * Function to duplicate a record when the duplicate button is clicked.
         * @param {integer} recordId - The id of the record to duplicate.
         */
        _duplicateRecord: function (recordId) {
            var self = this;
            this._rpc({
                model: this.props.list.resModel,
                method: 'copy',
                args: [recordId],
            }).then(function (_result) {
                // Refresh the list view to reflect the newly duplicated record
                self.trigger_up('reload');
            });
        },
    });

    return YourListRenderer;
});
