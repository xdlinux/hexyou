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
    if(ts.val()!='')ts.siblings('.holder').hide();
    ts.siblings('.holder').click(function(){ts.focus()});
  })
  holding.focus(function(){
    $(this).siblings('.holder').hide(200);
  }).blur(function(){
    if($(this).val()==''){
      $(this).siblings('.holder').show();
    }
  })
 
  $('input[rel=popover]').popover({'trigger':'focus','offset':32});



/* datepicker */

  $(".datetime input").datetimepicker({
    showButtonPanel:false,
    showAnim:'slideDown',
    currentText:"现在",
    closeText:"确认",
    monthNames:['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],
    dayNamesMin:['日','一','二','三','四','五','六'],
    minDate:new Date(),
    yearSuffix:'年',
    dateFormat:'yy-mm-dd',
    timeFormat: 'hh:mm',
    separator: ' ', // fixed the space ends the datetime string
  });

  $('form').has('.datetime').submit(function(){
    inputs = $('.datetime input')
    if(new Date(inputs[0].value)>=new Date(inputs[1].value)){
      return false
    }
  })

/* autocomplete */

  $(".inform-list").val("")

  function removeLabel(label,category){
    labels = $(".inform-list."+category).val().split(',')
    for(var i=0;i<labels.length;i++){
      if(labels[i]==label.attr('value')){
        labels.splice(i,1)
      }
    }
    $(".inform-list."+category).val(labels.join(','))
    label.fadeOut('normal',function(){$(this).remove()})
  }

  function getCategoryName(category){
    category_name = {
      'user':'用户',
      'group':'组织',
      'location':'地点',
      'activity':'活动',
    }
    return eval('category_name.'+category)
  }

  $.widget( "custom.catcomplete", $.ui.autocomplete, {
    _renderMenu: function( ul, items ) {
      var self = this,
        currentCategory = "";
      $.each( items, function( index, item ) {
        if ( item.category != currentCategory ) {
          ul.append( "<div class='ui-autocomplete-category'><small>" + getCategoryName(item.category) + "</small></div>" );
          currentCategory = item.category;
        }
        self._renderItem( ul, item );
      });
    },
    _renderItem: function(ul, item){
      return $( "<li></li>" )
          .data( "item.autocomplete", item )
          .append( "<a>" + "<img src=\"" + item.avatar + "\" style=\"width:24px;height:24px;\" />" + item.name + '(' + item.slug + ')' + "</a>" )
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
                slug: item.slug,
                value: item.id,
                category: item.category,
              }
            })
          )
        },
      })
    },
    select: function(event,ui){
      $("#inform-input").val("")
      listclass = ".inform-list."+ui.item.category
      list = $(listclass).val()
      index = list.indexOf(ui.item.value + ',')
      if(index==-1){
        if(list){
          $(listclass).val(list + ui.item.value + ',')
        }else{
         $(listclass).val(ui.item.value + ',')
        }
        $("#label-list").append('<span class="label ' + ui.item.category + '"' + 'slug="' + ui.item.slug + '" value="' + ui.item.value + '">' + ui.item.name + ' <span class="label-close">×</span></span>')
      }
      $(".label .label-close").click(function(){
          removeLabel($(this).parent('.label'),ui.item.category)
      })
      return false;
    },
  }).data("autocomplete")

  $('#side-search .search-input').catcomplete({
    source: function(request,response){
      $.ajax({
        url : '/json/',
        type : 'POST',
        dataType : 'json',
        data : {
          request_type : $('#side-search .search-input').attr("request-type"),
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
                slug:item.slug,
                value: item.id,
                category: item.category,
              }
            })
          )
        },
      })
    },
    select:function(event,ui){
      window.location.href='/'+$('#side-search .search-input').attr("redirect-type")+'/'+ui.item.slug
    }
  })


/* dropdowns */

  $.ajax({
    url : '/json/',
    type : 'POST',
    dataType : 'json',
    data : {
      request_type : 'current_user',
      request_phrase : 'current_user',
    },
    success:function(data){
      data=data[0]
      $('#session-avatar>img').attr({'src':data.avatar})
      $('#session>a>b').before(data.name)
    }
  })


/* location */

  function getLocations(a){
    ul = a.parent().parent()
    $.ajax({
      url : '/json/',
      type : 'POST',
      dataType : 'json',
      data : {
        request_type : 'location',
        request_phrase : a.attr('request-phrase')
      },
      success:function(data){
        if(data.length){
          $("#location-no-child").slideUp()
          ul.nextAll().slideUp('normal',function(){
            $(this).not("#location-no-child").remove()
          })
          s=""
          $.map(data,function(item){
            s+="<li><a href='#' request-phrase='" + item.id + "'>" + item.name + "</a></li>\n"
          })
          $("<ul class='location-parent hide'></ul>").append(s).appendTo(ul.parent()).slideDown().find('a').click(function(){
            clickLocation($(this))
          })
        }else{
          ul.nextAll('ul').slideUp('normal',function(){
            $(this).remove()
          })
          $("#location-no-child").slideDown()
        }
      }
    })
  }

  function clickLocation(a){
    if(a.hasClass('active')){
      getLocations(a)
    }else{
      $('#location-no-selected').slideUp()
      a.parent().parent().find('a').removeClass('active')
      a.toggleClass('active')
      getLocations(a)
    }
    $('#location-selected').data('location_name',a.text())
    $('#location-selected').data('location_id',a.attr('request-phrase'))
  }

  $('#location-root>li>a').click(function(){
    clickLocation($(this))
  })

  $('#location-select-modal').on('hide',function(){
    $('#location-select-input').val($('#location-selected').data('location_name'))
    $('#id_location').val($('#location-selected').data('location_id'))
  })

  $('#location-select-input').click(function(){
    $('#location-select-modal').modal('show')
  })

  $('#location-select-confirm').click(function(){
    if($('#location-selected').data('location_name')){
      $('#location-select-modal').modal('hide')
    }else{
      $('#location-no-selected').slideDown('normal',function(){
        setTimeout(function(){$('#location-duplicate').slideUp()},5000)
      })
    }
  })

  $('#location-select-create').click(function(){
    if(!$('#location-selected').data('location_id')){
      $('#location-no-selected').slideDown('normal',function(){
        setTimeout(function(){$('#image-crop-error').slideUp()},5000)
      })
    }else{
      r = '{"name":"'+$('#location-selected').val()+'",'+'"parent":"'+$('#location-selected').data('location_id')+'"}'
      $.ajax({
        url : '/json/',
        type : 'POST',
        dataType : 'json',
        data : {
          request_type : 'create_location',
          request_phrase : r
        },
        success:function(data){
          if(data){
            $('#location-duplicate').slideDown('normal',function(){
              setTimeout(function(){$('#location-duplicate').slideUp()},5000)
            })
          }else{
            
          }
        }
      })
    }
  })

/* buttons */
  $('#join-group').one('click',function(){
    join_group_btn = $(this)
    join_group_btn.addClass('disabled').text('请稍等...')
    $.ajax({
      url:'/json/',
      type:'POST',
      data:{
        request_type:'join_group',
        request_phrase:window.location.pathname.match(/groups\/(\w+)\\?/)[1],
      },
      success:function(){
        var group_name = $('h1').text()
        group_name = group_name.substr(0,group_name.indexOf('<')-1)
        join_group_btn.text('已加入 '+$('h1').text().match(/(.+[^<\n])/)[0])
      }
    })
  })


/* alert */
  $(".alert-message").alert()
})
