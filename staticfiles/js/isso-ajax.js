$('#followers').click(function(){
	var algNameSlug;
	algNameSlug = $(this).attr("data-algNameSlug");
	$.get('/rango/follow_algorithm/', {algorithmNameSlug: algNameSlug}, function(data){
		$('#follower_count').html(data);
		$('#followers').hide();
	});
});

$('#suggestion').keyup(function(){
	var query;
	query = $(this).val();
	$.get('/rango/suggest_search/', {suggestion: query}, function(data){
		$('#cats').html(data);
	});
});

$('.algButton').click(function(){
	var algName = $(this).html();
	$.get('/rango/update_alg_choice/', {algorithmName: algName}, function(data){
		data = JSON.parse(data);
		$('#follower_count').html(data['followers']);
		$('#changing_link').attr('href','/rango/algorithm/'+data['algSlug']); 
		$('#algName').html(data['algName']);
	});
});
