
$(document).ready(function() {
    "use strict";

    $(document).on('change', ".contact_select", function() {

        var sel_val = $(this).val();

        $('#partner_info > #'+sel_val).find('span').each(function(){

            var target = $("input[name='"+ $(this).attr("id")+"']");
            target.val( $(this).text());

            if(!$(this).text()) {
                target.attr('readonly', false);
                console.log($(this).text());
            }
            else {
                target.attr('readonly', true);
            }
        });

    });

});
