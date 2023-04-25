odoo.define('website_custom_saca.script', function (require) {
    "use strict";
    var ajax = require("web.ajax");

    $('#btn_saca_edit').click(function(){
        var first = $('.weight_input')[0];
        if ($(first).css('display') == 'none'){
            $('.info_span').css('display', 'none');
            $('.weight_input').css('display', 'block');
            $('.saca_input').css('display', 'initial');
            $('.unload_input').css('display', 'initial');
            $('#btn_saca_save').css('display', 'block');
            $('#btn_saca_edit').css('display', 'none');
        }
        else{
            $('.info_span').css('display', 'block');
            $('.weight_input').css('display', 'none');
            $('.unload_input').css('display', 'none');
            $('.saca_input').css('display', 'none');
        }
    });

    $('#btn_saca_send').click(function(){
        var id = $(this).attr('value');
        var href = '/saca/line/send/' + id;
        console.log(id);
        console.log(href);
        var self = this;
        ajax.jsonRpc(href, 'call', {'saca_id': id}).then(function (data) {
            console.log('AAA');
            if (!data) {
                 return;
            }
            console.log(res);
        });
    });
});