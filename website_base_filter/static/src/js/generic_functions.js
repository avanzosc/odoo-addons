/* Delete repeated filters and alphabetically order customer filter*/
$(document).ready( function() {
    "use strict";

    var url = window.location.href;
    if (!(url.includes('/my/invoices') || url.includes('/my/orders')
      || url.includes('/my/stock') || url.includes('/my/crm_claim')
      || url.includes('/my/crm_lead'))) {
     var cont = 0;
     $('nav.navbar.o_portal_navbar').each( function() {
      if (cont !=  0) $(this).remove();
      cont++;
     });
     $('#o_portal_navbar_content').each( function() {
      var nav_elements = $(this).find('.form-inline');
      nav_elements.each( function() {
       var nav_id = $(this).attr('id');
       if (nav_id !== undefined && nav_id.includes('filter')) {
        $(this).remove();
       }
     });
     });
    }

});

/* Sorts alphabetically customer filter option values */
function orderCustomerFilter(module_str) {
    var btn_id = '';
    if (module_str === 'invoice') btn_id = $('#portal_invoice_filter_customer > div');
    if (module_str === 'order') btn_id =  $('#portal_order_filter_customer > div');
    if (module_str === 'stock') btn_id =  $('#portal_stock_filter_customer > div');
    if (module_str === 'claim') btn_id =  $('#portal_claim_filter_customer > div');
    if (module_str === 'lead') btn_id =  $('#portal_lead_filter_customer > div');
    if (btn_id) {
        btn_id.html($("#btn_id option").sort(function (a, b) {
            return a.text == b.text ? 0 : a.text < b.text ? -1 : 1
        }));
    }
}

/* Adds new parameter and value to the current URL */
function addUrlParameter(name, value) {
 var searchParams = new URLSearchParams(window.location.search)
 searchParams.set(name, value)
 window.location.search = searchParams.toString()
}

/* Mantains navbar selected element color */
function mantainFilterColor(module_str) {
 var filter_nav_id = '';
 var date_nav_pos = 0;
 if (module_str === 'invoice') {
  filter_nav_id = 'invoice_filters';
  date_nav_pos = 5;
 }else if(module_str === 'order') {
  filter_nav_id = 'order_filters';
  date_nav_pos = 3;
 }else if(module_str === 'stock') {
  filter_nav_id = 'stock_filters';
  date_nav_pos = 5;
 }else if(module_str === 'claim') {
 filter_nav_id = 'claim_filters';
 date_nav_pos = 5;
}else if(module_str === 'lead') {
 filter_nav_id = 'lead_filters';
 date_nav_pos = 5;
}
 var params = new URLSearchParams(window.location.search);
 if (params.get('customer') !== null) {
  if (params.get('customer').toString() !== 'All customers') {
   $("#" + filter_nav_id +" > div:nth-child(2) > div > a").each( function() {
    var href_params = $(this).attr('href').split('?')[1];
    var href_params_list = href_params.split('&');
    for (i=0; i<href_params_list.length; i++) {
     if (href_params_list[i].includes('customer') && href_params_list[i].replace(
       'customer=','').toString() === params.get('customer').toString()) {
      $(this).addClass('active');
     }
    }
   });
  }else{
   $("#" + filter_nav_id +" > div:nth-child(2) > div > a:nth-child(1)").addClass('active');
  }
 }
 if (params.get('state') !== null) {
  $('#'+ filter_nav_id +' > div:nth-child(3) > div > a > span').each( function(index) {
   var span_text = $(this).text().trim()
   if (index !== 0) span_text = span_text.toLowerCase();
   if (span_text.split(' ').length > 1 && index !== 0) span_text = span_text.replace(' ','_');
    if (span_text === params.get('state').toString()) {
     $(this).parent().addClass('active');
    }
  });
 }
 if (params.get('date_type') !== null) {
  $('#'+ filter_nav_id +' > div:nth-child('+(date_nav_pos-1)+') > div > a > span').each( function() {
   var span_text = $(this).text().trim();
    if (span_text === params.get('date_type').toString()) {
     $(this).parent().addClass('active');
    }
  });
 }
 if (params.get('date') !== null) {
  $('#'+ filter_nav_id +' > div:nth-child('+ date_nav_pos +') > div > a > span').each( function() {
   var span_text = $(this).text().trim();
    if (span_text === params.get('date').toString()) {
     $(this).parent().addClass('active');
    }
  });
 }
 if (params.get('date_from') !== null) {
  $('#portal_'+module_str+'_filter_date_from').val(params.get('date_from'));
 }
 if (params.get('date_to') !== null) {
  $('#portal_'+module_str+'_filter_date_to').val(params.get('date_to'));
 }
}

/* Checks correct navbar filters */
function checkNavbarFilter(module_str) {
 var data = []
 if (module_str == 'stock') {
  data = ['#my_stock_details_container', 'stock_filters'];
 } else if (module_str == 'lead') {
  data = ['#my_crm_lead_details_container', 'lead_filters'];
 } else if (module_str == 'claim') {
  data = ['#my_crm_claim_details_container', 'claim_filters'];
 } else if (module_str == 'invoice') {
 data = ['#invoice_content', 'invoice_filters'];
} else if (module_str == 'order') {
 data = ['#quote_content', 'order_filters'];
}
  if ($(data[0]).length) {
   $('nav.o_portal_navbar').each( function() {
    $(this).remove();
   });
  } else {
   $('nav.o_portal_navbar').each( function(index) {
    if (index != 0) {
     $(this).remove();
    }
   });
   $('nav.o_portal_navbar').find('div.form-inline').each( function() {
    if ($(this).attr('id') != data[1]) {
     $(this).remove();
    }
   });
  }
}

/* Checks correct navbar text */
function checkNavbarText(module_str) {
 var text = $('div.col > ol.o_portal_submenu');
 var text_elems = text.find('li.breadcrumb-item');
 var data = []
 if (module_str == 'stock') {
  data = ['Stock', '/my/stock'];
 } else if (module_str == 'lead') {
  data = ['Crm lead', '/my/crm_lead'];
 } else if (module_str == 'claim') {
  data = ['Crm claim', '/my/crm_claim'];
 }
  if (text_elems.length == 2) {
   text_elems.eq(1).find('a').eq(0).attr('href', data[1]);
   text_elems.eq(1).find('a').eq(0).text(data[0]);
   text_elems.eq(1).find('a').eq(0).css('color', '#00A09D');
  }else{
   var elem_1 = text_elems.eq(1);
   var elem_2 = text_elems.eq(2);
   if (!elem_1.has('a')) {
    elem_2.find('a').eq(0).attr('href', data[1]);
    elem_2.find('a').eq(0).text(data[0]);
    elem_2.before(elem_1);
   }else {
    elem_1.find('a').eq(0).attr('href', data[1]);
    elem_1.find('a').eq(0).text(data[0]);
    elem_1.find('a').eq(0).css('color', '#00A09D');
   }
  }
}

/* Validates inputed dates */
function validateDates(date_from, date_to) {
 if (date_from && date_to) {
  date_from = new Date(date_from);
  date_to = new Date(date_to);
  if (date_from > date_to) {
   var searchParams = new URLSearchParams(window.location.search)
   searchParams.delete(searchParams.get('date_from'));
   searchParams.delete(searchParams.get('date_to'));
   swal({
    title: "Wrong dates!",
    icon: "warning",
    confirm: true,
    dangerMode: true,
   })
   window.location.search = searchParams.toString();
  }
 }
}

/* Table comparer functions */
function orderTable(tab) {
 var table = $(tab).parents('table').eq(0);
 var rows = table.find('tr:gt(0)').toArray().sort(comparer($(tab).index()));
 tab.asc = !tab.asc;
 if (!tab.asc) {
  rows = rows.reverse();
 }
 for (var i = 0; i < rows.length; i++) {
  table.append(rows[i]);
 }
 setIcon($(tab), tab.asc);

}

function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index),
            valB = getCellValue(b, index);
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.localeCompare(valB);
    }
}
function getCellValue(row, index) {
    return $(row).children('td').eq(index).html();
}
function setIcon(element, asc) {
    $("th").each(function() {
        $(this).removeClass("sorting");
        $(this).removeClass("asc");
        $(this).removeClass("desc");
    });
    element.addClass("sorting");
    if (asc) element.addClass("asc");
    else element.addClass("desc");
}
