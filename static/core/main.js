window.onload = function (){
	
	$("#searchForm").hide();
	
	$( "#search" ).click(function() {
		$("#searchForm").toggle();
	});
				
	var active = function(){
		$( this ).css({"backgroundColor" : "#766b6b", "color" : "#ffffff"});
	} 
	
	var notactive = function(){
		$( this ).css({"backgroundColor" : "", "color" : ""});
	} 
		
	$( "#register" ).click(function(){
		window.location.href = "/register";
	});
	
	$( "#login" ).click(function(){
		window.location.href = "/login";
	});
	
	$( "#profile" ).click(function(){
		window.location.href = "/profile";
	});
	
	$( "#new" ).click(function(){
		window.location.href = "/new";
	});
	
	$( "#logout" ).click(function(){
		window.location.href = "/logout";
	});
	
	$( "#logo" ).click(function(){
		window.location.href = "/";
	});
	
	
	$( "#search" ).mouseenter(active);
	$( "#register" ).mouseenter(active);
	$( "#login" ).mouseenter(active);
	$( "#profile" ).mouseenter(active);
	$( "#logout" ).mouseenter(active);
	$( "#new" ).mouseenter(active);
	
	$( "#search" ).mouseleave(notactive);
	$( "#register" ).mouseleave(notactive);
	$( "#login" ).mouseleave(notactive);
	$( "#profile" ).mouseleave(notactive);
	$( "#logout" ).mouseleave(notactive);
	$( "#new" ).mouseleave(notactive);
	
}
	
