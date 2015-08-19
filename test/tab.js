<<<<<<< HEAD
﻿// Sidebar code
$(document).ready(function(){
	$('#first #first_nav li a').click(function(){
		$('#first > div').hide().filter(this.hash).fadeIn();
		$('#first #first_nav li a').removeClass('selected');
		$(this).addClass('selected');
		return false;
	}).filter(':first').click();
=======
﻿// Sidebar code
$(document).ready(function(){
	$('#first #first_nav li a').click(function(){
		$('#first > div').hide().filter(this.hash).fadeIn();
		$('#first #first_nav li a').removeClass('selected');
		$(this).addClass('selected');
		return false;
	}).filter(':first').click();
>>>>>>> 5972d3f97e67f84883bfbf97fc911834308604fa
});