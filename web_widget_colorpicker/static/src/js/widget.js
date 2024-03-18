odoo.define('web.web_widget_colorpicker', function(require) {
    "use strict";

    var field_registry = require('web.field_registry');
    var Field = field_registry.get('char');


    var FieldColorPicker = Field.extend({

        template: 'FieldColorPicker',
        widget_class: 'oe_form_field_color',

        _renderReadonly: function () {
            var show_value = this._formatValue(this.value);
            this.$el.text(show_value);
            this.$el.css("background-color", show_value);

        },

        _getValue: function () {
            var $input = this.$el.find('input');

            var val = $input.val();
            var isOk = /^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/i.test(val);

            if (!isOk) {
                    return 0;
                }

            return $input.val();


        },

        _renderEdit: function () {

                var show_value = this.value ;
                var $input = this.$el.find('input');
                $input.val(show_value);

                this.$el.colorpicker({format: 'rgba'});
                this.$input = $input;

        }

    });

        field_registry
        .add('colorpicker', FieldColorPicker);



return {
    FieldColorPicker: FieldColorPicker
};


});
