$(document).ready(function(){

  /* input holder*/
	var holding = $('form>.holding>input').filter('input[type=text],input[type=email],input[type=password]');
	holding.each(function(){
        var ts=$(this);
        ts.next('.holder').click(function(){ts.focus()});
		if (ts.val()!=''){
		  ts.next('.holder').hide(200);
		}
	})
	holding.keypress(function(){
    $(this).next('.holder').hide(200);
  }).change(function(){
    if($(this).val()==''){
      $(this).next('.holder').show();
    }
  })
    $('input[rel=popover]').popover({'trigger':'focus'});
})
