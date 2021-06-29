
$(document).ready(function() {
    "use strict";

    $(document).on('change', ".contact_select", function() {

        var sel_val = $(this).val();
        var counter = $(this).attr('id');
        if(sel_val != 'none'){
            $('#partner_info > #'+sel_val).find('span').each(function(){
                var target = $("input[name='"+ counter + "-" + $(this).attr("id")+"']");
                target.val( $(this).text());

                if(!$(this).text()) {
                    target.attr('readonly', false);
                }
                else {
                    target.attr('readonly', true);
                }
            });
        }
        else{
            $(this).find('input').each(function(){
                $(this).val('')
                $(this).attr('readonly', false);
            });
        }
    });

});
