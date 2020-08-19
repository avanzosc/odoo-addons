$(document).ready( function() {
    "use strict";

    var params = new URLSearchParams(window.location.search);
    /* Set selected element for dropdown filters */
    if (params.get('zone') !== null) {
        $('#product_zone_dropdown > option').each( function() {
            if ($(this).val().includes('zone='+params.get('zone'))) {
                $("#product_zone_dropdown").val($(this).val());
            }
        });
    }
    if (params.get('state') !== null) {
        $('#product_state_dropdown > option').each( function() {
            if ($(this).val().includes('state='+params.get('state'))) {
                $("#product_state_dropdown").val($(this).val());
            }
        });
    }
    if (params.get('city') !== null) {
        $('#product_city_dropdown > option').each( function() {
            if ($(this).val().includes('city='+params.get('city'))) {
                $("#product_city_dropdown").val($(this).val());
            }
        });
    }
    if (params.get('member') !== null) {
        $('#product_member_dropdown > option').each( function() {
            if ($(this).val().includes('member='+params.get('member'))) {
                $("#product_member_dropdown").val($(this).val());
            }
        });
    }

    /* List and grid view change button selectors */
    $('.o_wsale_apply_grid').click( function() {
        params.set('layout', 'grid');
        window.location.search = params.toString();
    });
    $('.o_wsale_apply_list').click( function() {
        params.set('layout', 'list');
        window.location.search = params.toString();
    });
    $('#product_state_dropdown').change( function() {
        window.location.href = $(this).val();
    });
    $('#product_zone_dropdown').change( function() {
        window.location.href = $(this).val();
    });
    $('#product_city_dropdown').change( function() {
        window.location.href = $(this).val();
    });
    $('#product_member_dropdown').change( function() {
        window.location.href = $(this).val();
    });
    
    /* Product cart button selectors */
    $('#products_grid > table > tbody > tr > td:nth-child(7) > form').submit( function(event) {
        var product_id = $(this).closest("tr").find("td").eq(1).text().trim();
        var quantity = $(this).closest("tr").find("td").eq(5).find('input.js_quantity').val();
        if (parseInt(quantity) !== 0) {
            $(this).attr('action', $(this).attr('action') + '?product_id=' +
              product_id + '&add_qty=' + parseInt(quantity));
        }else{
            event.preventDefault();
        }
    });
    $('.product-grid-card > div > div > div:nth-child(4) > div:nth-child(2) > form').submit( function(event) {
        var product_id = $(this).closest(".card-body").find('#product-grid-id').text().trim();
        var quantity = $(this).closest(".card-body").find("input.js_quantity").val();
        if (parseInt(quantity) !== 0) {
            $(this).attr('action', $(this).attr('action') + '?product_id=' +
              product_id + '&add_qty=' + parseInt(quantity));
        }else{
            event.preventDefault();
        }
    });
    /* Sort dropdown option selector */
    $('.oe_website_sale > div.products_pager > div.dropdown_sorty_by > div > a').click( function() {
        var query = '?';
        for (let p of params) {
            query = query + p[0] + '=' + p[1] + '&';
        }
        query = query + $(this).attr('href').split('?')[1];
        $(this).attr('href', '/shop' + query);
    });
});
