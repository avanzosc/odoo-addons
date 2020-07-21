/* global mantainFilterColor */
/* global checkNavbarText */
/* global checkNavbarFilter */
/* global addUrlParameter */
/* global validateDates */
/* global orderTable */
/* global orderCustomerFilter */

$(document).ready(function() {
    "use strict";
    var url = window.location.href;
    if (url.includes('/my/stock')) {
        mantainFilterColor('stock');
        checkNavbarText('stock');
        checkNavbarFilter('stock');
        orderCustomerFilter('stock');

        $('#portal_stock_filter_date_to').change(function() {
            addUrlParameter('date_to', $(this).val());
            validateDates($('#portal_stock_filter_date_from').val(), $('#portal_stock_filter_date_to').val());
        });
        $('#portal_stock_filter_date_from').change(function() {
            addUrlParameter('date_from', $(this).val());
            validateDates($('#portal_stock_filter_date_from').val(), $('#portal_stock_filter_date_to').val());
        });
        $('#wrap > div > div > table > thead > tr > th').click(function() {
            orderTable(this);
        });
    }
});
