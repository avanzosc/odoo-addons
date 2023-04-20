odoo.define('website_custom_saca.script', function (require) {
    "use strict";
    $('#btn_saca_edit').click(function(){
        var first = $('.weight_input')[0];
        if ($(first).css('display') == 'none'){
            $('.info_span').css('display', 'none');
            $('.weight_input').css('display', 'block');
            $('#btn_saca_save').css('display', 'block');
            $('#btn_saca_edit').css('display', 'none');
        }
        else{
            $('.info_span').css('display', 'block');
            $('.weight_input').css('display', 'none');
        }
    });
});