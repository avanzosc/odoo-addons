function formatDay(today) {
	let day = today.getDate();
	let month = parseInt(today.getMonth() +1).toString();
	if (day.toString().length == 1) {
		day = "0" + day.toString();
	}
	if (month.toString().length == 1) {
		month = "0" + month.toString();
	}
	return today.getFullYear() + '-' + month + '-' + day;
	
}

function Last7Days () {
    return '0123456'.split('').map(function(n) {
        var d = new Date();
        d.setDate(d.getDate() - n);

        return (function(day, month, year) {
            return [day<10 ? '0'+day : day, month<10 ? '0'+month : month, year].join('-');
        })(d.getFullYear(), d.getMonth(), d.getDate());
    });
}

function getDaysArray(start, end) {
    for(var days=[],dt=start; dt<=end; dt.setDate(dt.getDate()+1)){
        days.push(new Date(dt).toISOString().slice(0, 10));
    }
	    
		var last_month_day = (parseInt(days[days.length-1].split('-')[2]) + 1).toString();
		if (last_month_day.length == 1){
			last_month_day = "0" + last_month_day;
		}
		days.push(days[days.length-1].split('-')[0] + '-' + days[days.length-1].split('-')[1] + '-' + last_month_day);
		days.shift();
    
	for(let i=0; i<days.length; i++) {
		days[i] = days[i].split('-')[0] + '-' + days[i].split('-')[1] + '-' + days[i].split('-')[2];
	}
    return days;
};