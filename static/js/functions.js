$(document).ready(function(){

  /* input holder*/
	var holding = $('form>.holding>input').filter('input[type=text],input[type=email],input[type=password]');
	holding.each(function(){
        var ts=$(this);
        ts.siblings('.holder').click(function(){ts.focus()});
		if (ts.val()!=''){
		  ts.siblings('.holder').hide(200);
		}
	})
	holding.keypress(function(){
    $(this).siblings('.holder').hide(200);
  }).change(function(){
    if($(this).val()==''){
      $(this).siblings('.holder').show();
    }
  })
    $('input[rel=popover]').popover({'trigger':'focus','offset':32});
})
