/* global mantainFilterColor */
/* global checkNavbarFilter */
/* global addUrlParameter */
/* global validateDates */
/* global orderTable */
/* global orderCustomerFilter */

$(document).ready(function() {
    "use strict";
    var url = window.location.href;
    if (url.includes('/my/orders')) {
        mantainFilterColor('order');
        checkNavbarFilter('order');
        orderCustomerFilter('order');

        $('#portal_order_filter_date_to').change(function() {
            addUrlParameter('date_to', $(this).val());
            validateDates($('#portal_order_filter_date_from').val(), $('#portal_order_filter_date_to').val());
        });
        $('#portal_order_filter_date_from').change(function() {
            addUrlParameter('date_from', $(this).val());
            validateDates($('#portal_order_filter_date_from').val(), $('#portal_order_filter_date_to').val());
        });
        $('#wrap > div > div > table > thead > tr > th').click(function() {
            orderTable(this);
        });
    }
});