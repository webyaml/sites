// Functions for marking up cells created by datatables_ajax

function markup(data,args) {

	var field = args[0];
	var template = args[1];

	for (var key in data) {
		
		template = template.split("[["+key+"]]").join(data[key]);
		
	}
	
	data[field] = template;

}

function umi_markup(data,args) {

	var field = args[0];
	var template = args[1];

	for (var key in data) {
		
		template = template.split("[["+key+"]]").join(data[key][0]);
		
	}
	
	data[field] = template;

}

function TS_to_date(data,field) {
	
	function addZero(i) {
	    if (i < 10) {
		i = "0" + i;
	    }
	    return i;
	}	
	
	
	var d = new Date(parseInt(data[field])*1000);
	
	data[field] = d.getFullYear()+"-"+addZero(d.getMonth())+"-"+addZero(d.getDate())+" "+addZero(d.getHours())+":"+addZero(d.getMinutes())
	
}

function status(data) {

	// Status Menu
	var states = {
		
		"Start": {
			"icon": "fa fa-play",
			"label": "Start",
			"color": "success",
			"disable": "data['status'] == 'Start'"
		},
		
		"Pause": {
			"icon": "fa fa-pause",
			"label": "Pause",
			"color": "warning",
			"disable": "data['status'] == 'Pause'"
		},		

		"Stop": {
			"icon": "fa fa-stop",
			"label": "Stop",
			"color": "danger",
			"disable": "data['status'] == 'Stop'"
		},		
			
		"Erase": {
			"icon": "fa fa-trash-o",
			"label": "Erase",
			"color": "danger",
			"disable": "data['status'] != 'Stop'"
		}
	};

	var wrap = [];
	wrap[0] = `
		<ul class="status-list">
			<li class="dropdown">
				<a class="btn btn-`+states[data['status']]['color']+` btn-sm dropdown-toggle" data-toggle="dropdown" href="">
					<i class="`+states[data['status']]['icon']+` text-default">
					`+data['status']+`
					</i>
				</a>
				<ul class="dropdown-menu status-dropdown">						
		`;
	wrap[1] = `
				</ul>
			</li>
		</ul>							
		`;
	
	var output = "";
	
	for (var state in states) {
	
		var disabled = "";
		
		if ( eval(states[state]['disable']) == true ) {
		
			disabled = "disabled";
		
		}

		var button = `
			<li>                                    
				<button type="submit" name="command" class="btn btn-sm btn-`+states[state]['color']+` `+disabled+`" value="">
					<i class="`+states[state]['icon']+`"> `+states[state]['label']+` </i>
				</button>
			</li>
		`;

		output = output+button;

	}					
	
	data['status'] = wrap[0]+output+wrap[1];
}



function umi_status(data) {
	
	// convert umi_status to status
	
	if (data['active'][0] == 'TRUE' && data['delete'][0] == 'FALSE') {
		data['status'] = 'Start'
	}

	if (data['active'][0] == 'FALSE' && data['delete'][0] == 'FALSE') {
		data['status'] = 'Pause'
	}	
	
	if (data['active'][0] == 'FALSE' && data['delete'][0] == 'TRUE') {
		data['status'] = 'Stop'
	}

	status(data);
	
}