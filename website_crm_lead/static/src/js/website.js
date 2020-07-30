/* global mantainFilterColor */
/* global checkNavbarText */
/* global checkNavbarFilter */
/* global addUrlParameter */
/* global validateDates */
/* global orderTable */
/* global orderCustomerFilter */
/* global mantainCustomerSearchText */

$(document).ready(function() {
    "use strict";
    var url = window.location.href;
    if (url.includes('/my/crm_lead')) {
        mantainFilterColor('lead');
        checkNavbarText('lead');
        checkNavbarFilter('lead');
        orderCustomerFilter('lead');
        mantainCustomerSearchText();

        $('#portal_lead_filter_date_to').change(function() {
            addUrlParameter('date_to', $(this).val());
            validateDates($('#portal_lead_filter_date_from').val(), $('#portal_lead_filter_date_to').val());
        });
        $('#portal_lead_filter_date_from').change(function() {
            addUrlParameter('date_from', $(this).val());
            validateDates($('#portal_lead_filter_date_from').val(), $('#portal_lead_filter_date_to').val());
        });
        $('#search_customer_input').keydown(function (e) {
            var key = e.which;
            if (key === 13) {
                const search = $(this).val();
                addUrlParameter('customer_search', search.trim());
            }
        });
        $('#wrap > div > div > table > thead > tr > th').click(function() {
            orderTable(this);
        });
    }
});
