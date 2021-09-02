odoo.define('website_sale_zip_autocomplete.web_zip_autocomplete', function (require) {
    "use strict";

    var ajax = require('web.ajax');
$(document).ready(function() {

    $('.div_state').css('display', 'block');
    $(".div_zip").css('display', 'none');

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
                $("#country_id").val(data['country_id']);
                $("select[name='state_id']").val(data['state_id']);
                $("input[name='country']").val(data['country']);
                $("input[name='state']").val(data['state']);
                $("input[name='city']").val(data['city']);
                $("input[name='zip']").val(data['zip']);
            });
        });
    });
});
});
