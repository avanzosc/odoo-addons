$(document).ready(function() {
    "use strict";
    var url = window.location.href;
    if (url.includes('/my/orders')){
    	createOrderFilters();
    	fillOrderFilters();
    	
    	$("#portal_order_customer_filter > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            filterOrderData();
    	});
    	$("#portal_order_date_filter > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            $('#portal_order_datefrom_filter').val('');
    		$('#portal_order_dateto_filter').val('');
            filterOrderData();
    	});
    	$("#portal_order_datefrom_filter").change(function () {
            filterOrderData();
    	});
    	$("#portal_order_dateto_filter").change(function () {
            filterOrderData();
    	});
    	
    }
});

/* Creates different dropdown items for filters */
function createOrderFilters() {
	var filters_button = $('#o_portal_navbar_content > div > div');
	filters_button.append(
			'<span class="small mr-1 ml-2 navbar-text">Filter by: </span>');
	filters_button.append(
			'<div class="btn-group ml-1"><button data-toggle="dropdown" class="btn btn-secondary btn-sm dropdown-toggle" aria-expanded="false">'
			+ 'Customers</button><div class="dropdown-menu" id="portal_order_customer_filter"></div></div>');
	filters_button.append(
			'<div class="btn-group ml-1"><button data-toggle="dropdown" class="btn btn-secondary btn-sm dropdown-toggle" aria-expanded="false">'
			+ 'Dates</button><div class="dropdown-menu" id="portal_order_date_filter"></div></div>');
	filters_button.append(
			'<span class="small mr-1 ml-2 navbar-text">Date from: </span>');
	filters_button.append(
			'<input class="form-control ml-1" type="date" id="portal_order_datefrom_filter">');
	filters_button.append(
			'<span class="small mr-1 ml-2 navbar-text">Date to: </span>');
	filters_button.append(
			'<input class="form-control ml-1" type="date" id="portal_order_dateto_filter">');
	filters_button.append(
		'<span class="small mr-1 ml-2 navbar-text text-danger" id="order_date_error_text" style="display:none">Wrong dates!</span>');
}

/* Fills with data the different filters */
function fillOrderFilters() {
	//customers
	var customers = getCustomers();
	$('#portal_order_customer_filter').append('<a class="dropdown-item active" href="#" id="portal_order_customer_all">All customers</a>');
	for (let i=0; i<customers.length; i++){
		$('#portal_order_customer_filter').append(
				'<a class="dropdown-item" href="#" id="portal_order_customer_'+customers[i]['id']+'">'+customers[i]['name']+'</a>');
	}
	//dates
	$('#portal_order_date_filter').append('<a class="dropdown-item active" href="#" id="portal_order_dates_all">All dates</a>'
			+ '<a class="dropdown-item" href="#" id="portal_order_dates_today">Today</a>'
			+ '<a class="dropdown-item" href="#" id="portal_order_dates_week">Last week</a>'
			+ '<a class="dropdown-item" href="#" id="portal_order_dates_month">This month</a>'
			+ '<a class="dropdown-item" href="#" id="portal_order_dates_year">This year</a>');
}

/* Filters table with given values */
function filterOrderData() {
	// get filter values
	var customer_id = $("#portal_order_customer_filter > a.active").attr("id").trim().replace('portal_order_customer_','');
	var date = $("#portal_order_date_filter > a.active").attr("id").trim().replace('portal_order_dates_','');
	var date_from = document.getElementById("portal_order_datefrom_filter").value;
	var date_to = document.getElementById("portal_order_dateto_filter").value;
	$('#wrap > div > div.table-responsive.border.rounded.border-top-0 > table > tbody > tr').each(function() {
		$(this).show();
	});
	$('#order_date_error_text').hide();
	// prepare values
	let today = new Date();
	let today_formated = formatDay(today);
	let week_days = Last7Days();
	week_days = formatMonthNumber(week_days);
	let month_days = getDaysArray(new Date(new Date().getFullYear(), new Date().getMonth(), 1), today);
	let year_days = getDaysArray(new Date(new Date().getFullYear(), 0, 1), today);
	if (date_from){
		date_from = new Date(date_from.split('-')[0],parseInt(date_from.split('-')[1] - 1).toString(),date_from.split('-')[2]);
	}
	if (date_to){
		date_to = new Date(date_to.split('-')[0],parseInt(date_to.split('-')[1] - 1).toString(),date_to.split('-')[2]);
	}
	let dates_from_to = []
	if (date_from && date_to && date_from <= date_to) {
		dates_from_to = getDaysArray(date_from,date_to);
		date_from = new Date(dates_from_to[0].split('/')[2],parseInt(dates_from_to[0].split('/')[1] - 1).toString(),dates_from_to[0].split('/')[0]);
		date_to = new Date(dates_from_to[dates_from_to.length - 1].split('/')[2],parseInt(dates_from_to[dates_from_to.length - 1].split('/')[1] - 1).toString(),dates_from_to[dates_from_to.length - 1].split('/')[0]);
	}
	
	if (date_from || date_to) {
		$("#portal_order_date_filter > a.active").removeClass('active');
		$("#portal_order_date_filter > a:nth-child(1)").addClass('active');
		date = 'all';
	}
	if (date_from && date_to && date_from > date_to) {
		$('#order_date_error_text').show();
	}
	
	
	$('#wrap > div > div.table-responsive.border.rounded.border-top-0 > table > tbody > tr').each(function() {
		var row_customer = $(this).find('td').eq(1).find('p').text().trim();
		var row_date = $(this).find('td').eq(2).find('span').eq(0).text().trim();
		//customer filter
		if (customer_id != row_customer && customer_id != 'all'){
			$(this).hide();
		}
		//date filter
		if (date != 'all'){	
			if (date == "today" && row_date != today_formated){
				$(this).hide();
			}
			if (date == "week" && !week_days.includes(row_date)){
				$(this).hide();
			}
			if (date == "month" && !month_days.includes(row_date)){
				$(this).hide();
			}
			if (date == "year" && !year_days.includes(row_date)){
				$(this).hide();
			}
		}
		//date from and date to filters
		let row_date_formated = new Date(row_date.split('/')[2],parseInt(row_date.split('/')[1] - 1).toString(),row_date.split('/')[0]);
		if (date_from && date_to){
			if (!dates_from_to.includes(row_date)){
				$(this).hide();
			}
		} else if (date_from && !date_to){
			if (date_from > row_date_formated) {
				$(this).hide();
			}
		}else if (!date_from && date_to) {
			if (date_to < row_date_formated) {
				$(this).hide();
			}
		}
	});
	
}




