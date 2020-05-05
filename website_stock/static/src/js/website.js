$(document).ready(function() {
    "use strict";
    const picking_text = $('#wrapwrap > main > div.o_portal.container.mt-3 > div > div > ol > li:nth-child(2) > a').text().trim();
    if (picking_text === 'Stock picking') {
    	addFilters();
    	fillFilters();
    	
    	$("#portal_stock_searchbar_sortby > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            filterStockData();
    	});
    	$("#portal_stock_status_filter > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            filterStockData();
    	});
    	$("#portal_stock_date_filter > a").click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            filterStockData();
    	});
    	$("#portal_stock_datefrom_filter").change(function () {
            filterStockData();
    	});
    	$("#portal_stock_dateto_filter").change(function () {
            filterStockData();
    	});
    }

});


function filterStockData() {
	var table_data = getStockData();
	const filter_data = getFilterData();
	/* Sorting */
	if (filter_data['filter_sort'] != 'No sorting') {
		if (filter_data['filter_sort'] === 'Name') table_data.sort((a, b) => a.stock_picking.localeCompare(b.stock_picking));
		else if (filter_data['filter_sort'] === 'Company') table_data.sort((a, b) => a.company.localeCompare(b.company));
		else if (filter_data['filter_sort'] === 'Schedule date') table_data.sort((a, b) => a.schedule_date.localeCompare(b.schedule_date));
		else if (filter_data['filter_sort'] === 'Origin document') table_data.sort((a, b) => a.origin_document.localeCompare(b.origin_document));
		else if (filter_data['filter_sort'] === 'Order pending') table_data.sort((a, b) => a.order_pending_for.localeCompare(b.order_pending_for));
		else table_data.sort((a, b) => a.status.localeCompare(b.status));
	}
	/* Status filter */
	if (filter_data['filter_status'] != 'All status') {
		for (let i=0; i<table_data.length; i++) {
			console.log(table_data[i]['status'])
			if (table_data[i]['status'] != filter_data['filter_status']) {
				delete table_data[i];
			}
		}
	}
	table_data = table_data.filter(Boolean);
	/* Dates */
	var today_date = formatDay(new Date());
	var week_dates = Last7Days();
	for (let i=0; i<week_dates.length; i++) {
		week_dates[i] = formatDay(new Date(parseInt(week_dates[i].split('-')[0]),parseInt(week_dates[i].split('-')[1]),parseInt(week_dates[i].split('-')[2])));
	}
	var month_dates = getDaysArray(new Date(new Date().getFullYear(), new Date().getMonth(), 1), new Date());
	var year_dates = getDaysArray(new Date(new Date().getFullYear(), 0, 1), new Date());
	if (filter_data['filter_dates'] != 'All dates') {
		for (let i=0; i<table_data.length; i++) {
			var row_date = table_data[i]['schedule_date'].split(' ')[0];
			if (filter_data['filter_dates'] == 'Today' && row_date != today_date) {
				delete table_data[i];
			}
			if (filter_data['filter_dates'] == 'Last week' && !week_dates.includes(row_date)) {
				delete table_data[i];
			}
			if (filter_data['filter_dates'] == 'This month' && !month_dates.includes(row_date)) {
				delete table_data[i];
			}
			if (filter_data['filter_dates'] == 'This year' && !year_dates.includes(row_date)) {
				delete table_data[i];
			}
		}
		
	}
	table_data = table_data.filter(Boolean);
	/* Date from && date to */
	if (filter_data['filter_date_from']) {
		var date_from = new Date(filter_data['filter_date_from'].split('-')[0], parseInt(filter_data['filter_date_from'].split('-')[1] - 1), filter_data['filter_date_from'].split('-')[2]);
	}
	if (filter_data['filter_date_to']) {
		var date_to = new Date(filter_data['filter_date_to'].split('-')[0],parseInt(filter_data['filter_date_to'].split('-')[1] - 1),filter_data['filter_date_to'].split('-')[2]);
	}
	if (date_from && date_to && date_to >= date_from) {
		var from_to_dates = getDaysArray(date_from,date_to);
	}
	for (let i=0; i<table_data.length; i++) {
		var table_row_date = new Date(table_data[i]['schedule_date'].split(' ')[0].split('-')[0], parseInt(table_data[i]['schedule_date'].split(' ')[0].split('-')[1] - 1), table_data[i]['schedule_date'].split(' ')[0].split('-')[2]);
		if (date_from && !date_to && table_row_date < date_from) {
			delete table_data[i];
		}else if (!date_from && date_to && table_row_date > date_to) {
			delete table_data[i];
		}else if (from_to_dates) {
			var row_date_formated = formatDay(table_row_date);
			if (!from_to_dates.includes(row_date_formated)) {
				delete table_data[i];
			}
		}
	}
	table_data = table_data.filter(Boolean);
	/* Show/Hide elements */
	showStockTableElements();
	hideStockTableElements(table_data);
	
}

/* Returns filter selected data */
function getFilterData() {
	return {
		'filter_sort': $("#portal_stock_searchbar_sortby > a.active").text().trim(),
		'filter_status': $("#portal_stock_status_filter > a.active").text().trim(),
		'filter_dates': $("#portal_stock_date_filter > a.active").text().trim(),
		'filter_date_from': $("#portal_stock_datefrom_filter").val(),
		'filter_date_to': $("#portal_stock_dateto_filter").val(),
	}	
}

/* Returns stock table data */
function getStockData() {
	const table_rows = $('#wrap > div > div > table > tbody > tr');
	var table_data = [];
	table_rows.each(function() {
		table_data.push({
			'id': $(this).find('td').eq(0).text().trim(),
			'stock_picking': $(this).find('td').eq(1).text().trim(),
			'company': $(this).find('td').eq(2).text().trim(),
			'schedule_date': $(this).find('td').eq(3).text().trim(),
			'origin_document': $(this).find('td').eq(4).text().trim(),
			'order_pending_for': $(this).find('td').eq(5).text().trim(),
			'status': $(this).find('td').eq(6).text().trim(),
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
			+ 'Sorting</button><div class="dropdown-menu" id="portal_stock_searchbar_sortby"></div></div>');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text">Filter by: </span>');
	filters_row.append('<div class="btn-group ml-1"><button data-toggle="dropdown" class="btn btn-secondary btn-sm dropdown-toggle" aria-expanded="false">'
			+ 'Status</button><div class="dropdown-menu" id="portal_stock_status_filter"></div></div>');
	filters_row.append('<div class="btn-group ml-1"><button data-toggle="dropdown" class="btn btn-secondary btn-sm dropdown-toggle" aria-expanded="false">'
	+ 'Dates</button><div class="dropdown-menu" id="portal_stock_date_filter"></div></div>');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text">Date from: </span>');
	filters_row.append('<input class="form-control ml-1" type="date" id="portal_stock_datefrom_filter">');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text">Date to: </span>');
	filters_row.append('<input class="form-control ml-1" type="date" id="portal_stock_dateto_filter">');
	filters_row.append('<span class="small mr-1 ml-2 navbar-text text-danger" id="portal_stock_date_error_text" style="display:none">Wrong dates!</span></div>');
}

/* Fills with data the different filters */
function fillFilters() {
	$('#portal_stock_searchbar_sortby').append('<a class="dropdown-item active" href="#" id="portal_stock_sort_all">No sorting</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_sort_name">Name</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_sort_company">Company</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_sort_date">Schedule date</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_sort_document">Origin document</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_sort_order">Order pending</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_sort_status">Status</a>');
	$('#portal_stock_status_filter').append('<a class="dropdown-item active" href="#" id="portal_stock_status_all">All status</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_status_draft">Draft</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_status_waiting">Waiting</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_status_confirmed">Confirmed</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_status_asigned">Asigned</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_status_done">Done</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_status_cancelled">Cancelled</a>');
	$('#portal_stock_date_filter').append('<a class="dropdown-item active" href="#" id="portal_stock_dates_all">All dates</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_dates_today">Today</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_dates_week">Last week</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_dates_month">This month</a>'
			+ '<a class="dropdown-item" href="#" id="portal_stock_dates_year">This year</a>');
}

/* Show all table elements */
function showStockTableElements() {
	$('#wrap > div > div > table > tbody > tr').each(function () {
		$(this).show();
	});
}

/* Hide filtered table elements */
/* Terminar con esto */
function hideStockTableElements(data) {
	const rows = $('#wrap > div > div > table > tbody > tr');
	rows.each(function () {
		const row_id = $(this).find('td').eq(0).text().trim();
		/*for (let i=0; i<data.length; i++){
			if (data[i]['id'] != row_id) {
				$(this).hide();
				break;
			}
		}*/
		console.log(row_id)
	});
}


