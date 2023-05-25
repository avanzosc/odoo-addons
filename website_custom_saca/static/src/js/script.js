odoo.define('website_custom_saca.script', function (require) {
    "use strict";
    var ajax = require("web.ajax");

    $('#btn_saca_edit_2').click(function(){
        $('#btn_saca_edit').trigger( "click" );
    });
    $('#btn_saca_edit').click(function(){
        var first = $('.weight_input')[0];
        if ($(first).css('display') == 'none'){
            $('.info_span').css('display', 'none');
            $('.weight_input').css('display', 'block');
            $('.saca_input').css('display', 'initial');
            $('.saca_input_file').css('display', 'initial');
            $('.unload_input').css('display', 'initial');
            $('#btn_saca_save').css('display', 'block');
            $('#btn_saca_save_2').css('display', 'block');
            $('#btn_saca_edit').css('display', 'none');
            $('#btn_saca_edit_2').css('display', 'none');
            $('#chbx_fork').removeAttr('disabled');
        }
        else{
            $('.info_span').css('display', 'block');
            $('.weight_input').css('display', 'none');
            $('.unload_input').css('display', 'none');
            $('.saca_input').css('display', 'none');
            $('.saca_input_file').css('display', 'none');
            $('.chbx_fork').attr('disabled','disabled');
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
    $('#img_origin').change(function(){
        var image_input = null;
        var saca_line_id = $("#current_saca_line").val()
        var file = document.getElementById('img_origin').files[0];
        console.log(file);
        console.log(saca_line_id);
        if (file) {
             var reader = new FileReader();
             reader.readAsDataURL(file);
             reader.onload = function(e)
                 {
                     image_input = e.target.result;
                 }
        }
        var result = {'img_origin': image_input, 'saca_line_id': saca_line_id}
        $.ajax({
            url: "/my/saca/line/save/file",
            method: "POST",
            dataType: "json",
            data: result,
        });
    });
});