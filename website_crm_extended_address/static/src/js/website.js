$(document).ready(function() {
    "use strict";
    var template = document.title;
    if (template.includes('Contact Us | My Website')){
        if (window.localStorage.getItem("contact") == 'False'){
        	window.localStorage.setItem("contact",'True')
        }else {
        	var origin_url = window.location.origin;
            window.location.replace(origin_url.concat("/contactus_getdata"));
            window.localStorage.setItem("contact",'False')
        }
    	resetForm();
    	populateSelect();
    }
});

function resetForm() {
	let form = $('#wrap > div.container.mt-2 > div > div.col-lg-8 > div:nth-child(2) > form')
	form.attr('action', '/contactus_send');
	form.removeAttr('data-model_name');
	form.removeAttr('data-success_page');
	form.removeAttr('method');
	form.removeAttr('enctype');
	$('#wrap > div.container.mt-2 > div > div.col-lg-8 > div:nth-child(2) > form > div:nth-child(27)').hide();
	$('#wrap > div.container.mt-2 > div > div.col-lg-8 > div:nth-child(2) > form > div:nth-child(26)').after(
			'<div class="form-group row" data-oe-model="ir.ui.view" data-oe-id="1715" data-oe-field="arch" data-oe-xpath="/data/xpath/div/form[1]/div[8]">'
			+ '<div class="offset-lg-3 offset-md-4 col-md-8 col-lg-7"><button type="submit" class="btn btn-success">Submit</button>'
	        + '</div></div>');
}

function populateSelect() {
	states = []
	countries = []
	$('#state_ids_data > ul > li').each(function() {
        states.push({
        	'id': $(this).find('p').eq(0).text().trim(),
        	'name': $(this).find('p').eq(1).text().trim(),
        });
	});
	$('#country_ids_data > ul > li').each(function() {
        countries.push({
        	'id': $(this).find('p').eq(0).text().trim(),
        	'name': $(this).find('p').eq(1).text().trim(),
        });
	});
	states.sort(dynamicSort("name"));
	for (let i=0; i<states.length; i++){
		$('#state_id').append('<option value="' + states[i]['id'] + '">' + states[i]['name'] + '</option>');
		$('#sending_state_id').append('<option value="' + states[i]['id'] + '">' + states[i]['name'] + '</option>');
	}
	for (let i=0; i<countries.length; i++){
		$('#country_id').append('<option value="' + countries[i]['id'] + '">' + countries[i]['name'] + '</option>');
		$('#sending_country_id').append('<option value="' + countries[i]['id'] + '">' + countries[i]['name'] + '</option>');
	}
	
}

function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        if(sortOrder == -1){
            return b[property].localeCompare(a[property]);
        }else{
            return a[property].localeCompare(b[property]);
        }        
    }
}
