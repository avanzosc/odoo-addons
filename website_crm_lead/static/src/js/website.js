$(document).ready(function() {
    "use strict";
    const lead_text = $('#wrapwrap > main > div.o_portal.container.mt-3 > div > div > ol > li:nth-child(2) > a').text().trim();
    if (lead_text === 'Crm lead') {
    	addFilters();
    	fillFilters();
    	
    	$("#portal_lead_searchbar_sortby > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            filterLeadData();
    	});
    	$("#portal_lead_status_filter > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            filterLeadData();
    	});
    	$("#portal_lead_date_filter > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            filterLeadData();
    	});
    	$("#portal_lead_datefrom_filter").change(function () {
            filterLeadData();
    	});
    	$("#portal_lead_dateto_filter").change(function () {
            filterLeadData();
    	});
    }
});

function filterLeadData() {
	console.log('Working on it.')
}

/* Returns filter selected data */
function getFilterData() {
	return {
		'filter_sort': $("#portal_lead_searchbar_sortby > a.active").text().trim(),
		'filter_status': $("#portal_lead_status_filter > a.active").text().trim(),
		'filter_dates': $("#portal_lead_date_filter > a.active").text().trim(),
		'filter_date_from': $("#portal_lead_datefrom_filter").val(),
		'filter_date_to': $("#portal_lead_dateto_filter").val(),
	}	
}

/* Returns stock table data */
function getStockData() {
	const table_rows = $('#wrap > div > div > table > tbody > tr');
	var table_data = [];
	table_rows.each(function() {
		table_data.push({
			'id': $(this).find('td').eq(0).text().trim(),
			'crm_lead': $(this).find('td').eq(1).text().trim(),
			'customer': $(this).find('td').eq(2).text().trim(),
			'customer_email': $(this).find('td').eq(3).text().trim(),
			'customer_phone': $(this).find('td').eq(4).text().trim(),
			'planned_revenue': $(this).find('td').eq(5).text().trim(),
			'probability': $(this).find('td').eq(6).text().trim(),
			'commercial': $(this).find('td').eq(7).text().trim(),
			'closure_date': $(this).find('td').eq(8).text().trim(),
			'status': $(this).find('td').eq(9).text().trim(),
		})
	});
	return table_data;
}

/* Creates different dropdown items for filters */
function addFilters() {
	$('#o_portal_navbar_content > div').append('<div class="form-inline"></div>');
	const filters_row = $('#o_portal_navbar_content > div > div');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text">Sort by: </span>');
	filters_row.append('<div class="btn-group ml-1"><button data-toggle="dropdown" class="btn btn-secondary btn-sm dropdown-toggle" aria-expanded="false">'
			+ 'Sorting</button><div class="dropdown-menu" id="portal_lead_searchbar_sortby"></div></div>');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text">Filter by: </span>');
	filters_row.append('<div class="btn-group ml-1"><button data-toggle="dropdown" class="btn btn-secondary btn-sm dropdown-toggle" aria-expanded="false">'
			+ 'Status</button><div class="dropdown-menu" id="portal_lead_status_filter"></div></div>');
	filters_row.append('<div class="btn-group ml-1"><button data-toggle="dropdown" class="btn btn-secondary btn-sm dropdown-toggle" aria-expanded="false">'
	+ 'Dates</button><div class="dropdown-menu" id="portal_lead_date_filter"></div></div>');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text">Date from: </span>');
	filters_row.append('<input class="form-control ml-1" type="date" id="portal_lead_datefrom_filter">');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text">Date to: </span>');
	filters_row.append('<input class="form-control ml-1" type="date" id="portal_lead_dateto_filter">');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text text-danger" id="portal_lead_date_error_text" style="display:none">Wrong dates!</span></div>');
}

/* Fills with data the different filters */
function fillFilters() {
	$('#portal_stock_searchbar_sortby').append('<a class="dropdown-item active" href="#" id="portal_lead_sort_all">No sorting</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_sort_name">Name</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_sort_customer">Customer</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_sort_revenue">Planned revenue</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_sort_probability">Probability</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_sort_commercial">Commercial</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_sort_date">Closure date</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_sort_status">Status</a>');
	$('#portal_stock_status_filter').append('<a class="dropdown-item active" href="#" id="portal_lead_status_all">All status</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_status_new">New</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_status_qualified">Qualified</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_status_proposition">Proposition</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_status_won">Won</a>');
	$('#portal_stock_date_filter').append('<a class="dropdown-item active" href="#" id="portal_lead_dates_all">All dates</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_dates_today">Today</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_dates_week">Last week</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_dates_month">This month</a>'
			+ '<a class="dropdown-item" href="#" id="portal_lead_dates_year">This year</a>');
}


