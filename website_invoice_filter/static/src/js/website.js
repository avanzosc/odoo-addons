/* global mantainFilterColor */
/* global checkNavbarFilter */
/* global addUrlParameter */
/* global validateDates */
/* global orderTable */
/* global orderCustomerFilter */
/* global mantainCustomerSearchText */

$(document).ready(function() {
    "use strict";
    var url = window.location.href;
    if (url.includes('/my/invoices')) {
        if ($('table.o_portal_my_doc_table > thead > tr > th').length > 5) {
            $('table.o_portal_my_doc_table > thead > tr > th:nth-child(5)').html('Status');
        }
        mantainFilterColor('invoice');
        checkNavbarFilter('invoice');
        orderCustomerFilter('invoice');
        mantainCustomerSearchText();

        $('#portal_invoice_filter_date_to').change(function() {
            addUrlParameter('date_to', $(this).val());
            validateDates($('#portal_invoice_filter_date_from').val(), $('#portal_invoice_filter_date_to').val());
        });
        $('#portal_invoice_filter_date_from').change(function() {
            addUrlParameter('date_from', $(this).val());
            validateDates($('#portal_invoice_filter_date_from').val(), $('#portal_invoice_filter_date_to').val());
        });
        $('#search_customer_input').keydown(function (e) {
            var key = e.which;
            if (key === 13) {
                const search = $(this).val();
                addUrlParameter('customer_search', search.trim());
            }
        });
        $('#search_customer_button').click(function() {
            const search = $('#search_customer_input').val();
            addUrlParameter('customer_search', search.trim());
        });
        $('#wrap > div > div > table > thead > tr > th').click(function() {
            orderTable(this);
        });
    }
});
