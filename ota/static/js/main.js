$(document).ready(function(){
		
		//
		// CSRF token protection 
		//
		var csrftoken = $.cookie('csrftoken');
				
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		
		//
		// WARNING: every subsequent Ajax will use this
		// easy add of csrf token
		//
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
		
		//
		// variable/constant defines
		//
		
		var MAX_SEARCH_RESULTS = 25;
		var DELAY_SEARCH_MS = 600;
		var MIN_LENGTH_SEARCH = 2;
		
		var continents = ["Europe", "South America", "North America", "Australia", "Africa", "Asia"];
		var continentsObj = { "Europe":6,
						      "Asia":8, 
							  "North America": 1,
							  "South America": 3,
							  "Australia": 9, 
							  "Africa": 5
     					    };
		
		
		var us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
		'Kentuky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
		'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
		'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island','South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
		'West Virginia', 'Wisconsin', 'Wyoming'];
		
		var canada_prov = ['Ontario', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Manitoba', 'British Columbia', 'Price Edward Island', 'Saskatchewan', 'Alberta', 'Newfoundland and Labrador'];
		
		for ( var i = 0; i < us_states.length; i++ ){
			us_states[i] = us_states[i] + ", United States";
		}
		
		for ( var i = 0; i < canada_prov.length; i++ ){
			canada_prov[i] = canada_prov[i] + ", Canada";
		}
		
		//
		// Forces server to fill city and country data in cache
		// if not already done
		//
		var getCityAndCountryData = function() {
			var countries = [];
			var cities = [];
			
			$.ajax({
					url: "/address/allcountries/",
					datatype: "json",
					data : { },
					
				  }).done( function(data) {
					  countries = data;
					  
					  $.ajax({
						url: "/address/allcities/",
						datatype: "json",
						data : { },
						
					  }).done( function(data) {
						  cities = data;
					  });
				  });
		}
		
							
		/*var getDestinations = function() {
			var countries = [];
			var cities = [];
			
			$.ajax({
					url: "/address/allcountries/",
					datatype: "json",
					data : { },
					
				  }).done( function(data) {
					  countries = data;
					  
					  $.ajax({
						url: "/address/allcities/",
						datatype: "json",
						data : { },
						
					  }).done( function(data) {
						  
						  cities = data;						  
						  						  
						  $("#id_destination").autocomplete({
							    maxResults: MAX_SEARCH_RESULTS,
								src: countries.concat( continents ).concat(us_states).concat(canada_prov).concat(cities),
								source: function(request, response) {
											var results = $.ui.autocomplete.filter(this.options.src, request.term);
											response(results.slice(0, this.options.maxResults));
										},							
								delay : DELAY_SEARCH_MS,
								minLength : MIN_LENGTH_SEARCH
							});
					  });			  
					  
				  });
		} 		
		
		//
		// call get destinations
		//
		getDestinations(); */
		
		//
		// Get country and destination data first
		//
		getCityAndCountryData();
		
		//
		// Apply Google-Auto Complete
		//
		$("#id_destination").geocomplete({          
          details: "#destination-details",
          detailsAttribute: "name"
        }).bind("geocode:result", function(event, result){
			console.log( "locality:" + $("#id_locality").val());
			console.log( "country_short:" + $("#id_country_short").val());
			console.log( "administrative_area_level_1:" + $("#id_administrative_area_level_1").val());
		});				
		
		//
		// disable destination field when surprimeMe is checked.
		//
		$("#id_surpriseme").on( "click", function () {			
			var checked = $("#id_surpriseme").is(":checked");
			
			if (checked == true) {
			    $("#id_destination").val("");
				$("#id_destination").attr('disabled', true);
			} else {
				$("#id_destination").attr('disabled', false);
			}			
		});		

		//
		// set default values for adults/rooms/children
		//
		$("#id_adults").val(1);
		$("#id_rooms").val(1);
		$("#id_children").val(0);
});