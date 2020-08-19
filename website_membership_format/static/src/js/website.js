$(document).ready(
        function() {
            "use strict";

            var p_zone = $('#partner_zone').text().trim();
            $('#partner_zone').parent().find('div.w-100').append('</br>' + p_zone);
            $('#partner_zone').remove();

            $("#membership_details_product_table > tbody > tr > td > div > div > div > a").click(function() {
                var oldValue = $(this).closest("tr").find("input.js_quantity").val();
                if ($(this).attr('title') == "Add one") {
                    var newVal = parseFloat(oldValue) + 1;
                    if (isNaN(newVal))
                        newVal = parseFloat(0) + 1
                } else {
                    if (oldValue > 0)
                        var newVal = parseFloat(oldValue) - 1;
                    else
                        newVal = 0;
                }
                $(this).closest("tr").find("input.js_quantity").val(newVal);
                return false;
            });

            $("#membership_details_product_table > tbody > tr > td:nth-child(6) > form").submit(
                    function(event) {
                        var product_id = $(this).closest("tr").find("td").eq(0).text().trim();
                        var quantity = $(this).closest("tr").find("td").eq(4).find('input.js_quantity').val();
                        if (parseInt(quantity) !== 0) {
                            $(this).attr(
                                    'action',
                                    $(this).attr('action') + '?product_id=' + product_id + '&add_qty='
                                            + parseInt(quantity));
                        } else {
                            event.preventDefault();
                        }
                    });
        });
