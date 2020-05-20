$(document).ready(function() {
 "use strict";
 repositionHeader();

 var url = window.location.pathname;

 if (url === '/shop') {
  $('#products_grid > div > form > div > section > div.product_price > a').click(function(event) {
   var qty = $(this).closest('div.oe_product').find('input.js_quantity').val();
   if (qty === "0") {
    event.preventDefault();
    return false;
   }
  });

 }

});

function repositionHeader() {
 const header = $('#product_list_header');
 $('#products_grid').prepend(header);
 if (!$('body').hasClass('o_connected_user')) {
  $('#product_list_header > b:nth-child(4)').hide();
 }
}
