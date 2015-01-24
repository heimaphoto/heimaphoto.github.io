// Sidebar code
$(document).ready(function(){
	$('#first #first_nav li a').click(function(){
		$('#first > div').hide().filter(this.hash).fadeIn();
		$('#first #first_nav li a').removeClass('selected');
		$(this).addClass('selected');
		return false;
	}).filter(':first').click();
});