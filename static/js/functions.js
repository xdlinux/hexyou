$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

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
  
/* modal */

  $('.modal').modal({
    'backdrop':true,
  });

/* alerts */

  $(".alert-message").alert()

/* autocomplete */

  $("#inform-list").val("")

  function removeLabel(label){
    labels = $("#inform-list").val().split(',')
    for(var i=0;i<labels.length;i++){
      if(labels[i]==label.attr('slug')){
        labels.splice(i,1)
      }
    }
    $("#inform-list").val(labels.join(','))
    label.fadeOut('normal',function(){$(this).remove()})
  }

  $.widget( "custom.catcomplete", $.ui.autocomplete, {
    _renderMenu: function( ul, items ) {
      var self = this,
        currentCategory = "";
      $.each( items, function( index, item ) {
        if ( item.category != currentCategory ) {
          ul.append( "<div class='ui-autocomplete-category'><small>" + decodeURIComponent(item.category) + "</small></div>" );
          currentCategory = item.category;
        }
        self._renderItem( ul, item );
      });
    },
    _renderItem: function(ul, item){
      return $( "<li></li>" )
          .data( "item.autocomplete", item )
          .append( "<a>" + "<img src=\"" + item.avatar + "\" style=\"width:24px;height:24px;\" />" + item.name + '(' + item.value + ')' + "</a>" )
          .appendTo( ul )
      }
  });


  $("#inform-input").catcomplete({
    source: function(request,response){
      $.ajax({
        url : '/json/',
        type : 'POST',
        dataType : 'json',
        data : {
          request_type : $("#inform-input").attr("request-type"),
          request_phrase : request.term,
        },
        success : function(data){
          response(
            $.map(data,function(item){
              if (!item.name){
                item.name=item.slug
              }
              if (!item.avatar){
                item.avatar="/static/images/no_avatar.png"
              }
              return {
                name: item.name,
                avatar: item.avatar,
                value: item.slug,
                category: item.category,
              }
            })
          )
        },
      })
    },
    select: function(event,ui){
      $("#inform-input").val("")
      list = $("#inform-list").val()
      index = list.indexOf(ui.item.value)
      if(index==-1){
        if(list){
          $("#inform-list").val(list + ui.item.value + ',')
        }else{
         $("#inform-list").val(ui.item.value + ',')
        }
        $("#label-list").append('<span class="label"' + 'slug="' + ui.item.value + '">' + ui.item.name + ' <span class="label-close">×</span></span>')
      }
      $(".label .label-close").click(function(){
          removeLabel($(this).parent('.label'))
      })
      return false;
    },
    minLength:2
  }).data("autocomplete")
});