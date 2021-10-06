odoo.define('website_sale_zip_autocomplete.web_zip_autocomplete', function (require) {
    "use strict";

    var ajax = require('web.ajax');
$(document).ready(function() {

    $('select').selectpicker();

    $('.div_state').css('display', 'block');
    $(".div_zip").css('display', 'none');
    $("label[for='zip']").css('display', 'none');
    $("input[name='zip']").css('display', 'none');
    $("select[name='state_id']").css('display', 'none');
    $("select[name='country_id']").css('display', 'none');

    var update_json = $.Deferred();
    update_json.resolve();
    $("#zip_id").change(function(){
        update_json = update_json.then(function(){
            return ajax.jsonRpc("/shop/address/update_json", 'call', {
                'zip_str': $("#zip_id").val(),
                }).
            then(function (data) {
                if (!data) {
                    return;
                }
                $('#country_id').val(data['country_id']);
                $('#state_id').val(data['state_id']);
                $("input[name='city']").val(data['city']);
                $("input[name='zip']").val(data['zip']);
                $('.selectpicker').selectpicker('refresh');
            });
        });
    });
});
});
