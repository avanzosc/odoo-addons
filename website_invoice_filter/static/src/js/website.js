/* global mantainFilterColor */
/* global checkNavbarFilter */
/* global addUrlParameter */
/* global validateDates */
/* global orderTable */

$(document).ready(function() {
    "use strict";
    var url = window.location.href;
    if (url.includes('/my/invoices')) {
        if ($('table.o_portal_my_doc_table > thead > tr > th').length > 5) {
            $('table.o_portal_my_doc_table > thead > tr > th:nth-child(5)').html('Status');
        }
        mantainFilterColor('invoice');
        checkNavbarFilter('invoice');

        $('#portal_invoice_filter_date_to').change(function() {
            addUrlParameter('date_to', $(this).val());
            validateDates($('#portal_invoice_filter_date_from').val(), $('#portal_invoice_filter_date_to').val());
        });
        $('#portal_invoice_filter_date_from').change(function() {
            addUrlParameter('date_from', $(this).val());
            validateDates($('#portal_invoice_filter_date_from').val(), $('#portal_invoice_filter_date_to').val());
        });
        $('#wrap > div > div > table > thead > tr > th').click(function() {
            orderTable(this);
        });
    }
});
