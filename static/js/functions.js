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

String.prototype.trim=function(){
  return this.replace(/^(\s*)|(\s*)$/g,'')
}

$(document).ready(function(){

  /* Ajax setup */

  $.ajaxSetup({
    url : '/json/',
    type : 'POST',
    dataType : 'json',
  })

  $.fn.serializeJSON = function() {
    var json = {};
      $.map($(this).serializeArray(), function(n, i){
      json[n['name']] = n['value'];
      });
    return json;
  };

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

  function getOneWeekAgo(){
    var d = new Date(new Date()-3600*1000*24*7)
    return new Date(d.getFullYear(),d.getMonth(),d.getDate())
  }

  $(".datetime input").datetimepicker({
    showButtonPanel:false,
    showAnim:'slideDown',
    currentText:"现在",
    closeText:"确认",
    monthNames:['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],
    dayNamesMin:['日','一','二','三','四','五','六'],
    minDate:new Date(new Date(new Date()-3600*1000*24*7).toDateString()),
    yearSuffix:'年',
    dateFormat:'yy-mm-dd',
    timeFormat: 'hh:mm',
    stepMinute:5,
    separator: ' ', // fixed the space ends the datetime string
  });

/* autocomplete */

  if(!$('#label-list .label').size()){  
    $(".inform-list").val("")
  }

  function getCurrentGroup(){
    match = window.location.pathname.match(/groups\/(\w+)\\?/)
    if(match){
      return match[1]
    }
    return ""
  }

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

  function words(text,length){
    if(text.length>length){
      return text.substr(0,length)+"..."
    }else{
      return text
    }
  }

  $(".label .label-close").click(function(){
      removeLabel($(this).parent('.label'),'group')
  })

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
      if(item.slug){
        item.slug = '(' + words(item.slug,16) + ')'
      }
      return $( "<li></li>" )
          .data( "item.autocomplete", item )
          .append( "<a>" + "<img src=\"" + item.avatar + "\" style=\"width:24px;height:24px;\" />" + item.name + item.slug + "</a>" )
          .appendTo( ul )
      },
    _move:function(){

    }
  });


  $("#inform-input").catcomplete({
    source: function(request,response){
      $.ajax({
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
      if($('#side-search .search-input').attr("request-type")=='group'){
        window.location.href='/'+$('#side-search .search-input').attr("redirect-type")+'/'+ui.item.slug
      }else{
        window.location.href='/'+$('#side-search .search-input').attr("redirect-type")+'/'+ui.item.value
      }
    },
  })


/* location */

  function getLocations(a){
    var ul = a.parent().parent()
    $.ajax({
      data : {
        request_type : 'location',
        request_phrase : a.attr('request-phrase')
      },
      success:function(data){
        console.log(data)
        if(data!=""){
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
      },
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
        setTimeout(function(){$('#location-no-selected').slideUp()},5000)
      })
    }else{
      $.ajax({
        data : {
          request_type : 'create_location',
          request_phrase : $.toJSON({
            name:$('#location-selected').val(),
            parent:$('#location-selected').data('location_id')
          })
        },
        success:function(data){
          clickLocation($('ul.location-parent').has('a.active').last().find('a.active'))
        },
        error:function(){
          $('#location-duplicate').slideDown('normal',function(){
            setTimeout(function(){$('#location-duplicate').slideUp()},5000)
          })
        }
      })
    }
  })

/* buttons */

  function updateAvatarList(id,url_prefix){
    var selector = '#'+id+'>li'
    if($(selector).size()==8){
      $(selector+':first').hide(200,function(){$(this).remove()})
    }
    $(selector+':first').clone().hide().find('a').attr('href','/'+url_prefix+'/'+$('#session').attr('user')).end().find('img').attr('src',$('#session-avatar>img').attr('src').replace(/_small/,'')).end().prependTo($('#'+id)).show('slide',{direction:'left'})
    var count = $('#'+id).prev().find('small')
    var n = parseInt(count.text().match(/\((\d+)\)/)[1])
    n++
    count.text('(' + n + ')')
  }

  $('#join-group').one('click',function(){
    var join_group_btn = $(this)
    join_group_btn.addClass('disabled').text('请稍等...')
    $.ajax({
      data:{
        request_type:'join_group',
        request_phrase:getCurrentGroup(),
      },
      success:function(data){
        if(data[0].condition==1){
          var group_name = $('h1').text()
          group_name = group_name.substr(0,group_name.indexOf('<')-1)
          join_group_btn.text('已加入 '+$('h1').text().match(/^(.+)\s/)[0])
          updateAvatarList('members','members')
        }else{
          join_group_btn.text('等待审核...')
        }
      }
    })
  })

  function getCurrentActivity(){
    match = window.location.pathname.match(/activities\/(\d+)\\?/)
    if(match){
      return match[1]
    }
    return ""
  }

  $('#participate-activity').one('click',function(){
    var btn = $(this)
    var origin = btn.text()
    btn.addClass('disabled').text('请稍等...')
    $.ajax({
      data:{
        request_type:'participate_activity',
        request_phrase:getCurrentActivity(),
      },
      success:function(){
        btn.text('已参加 '+origin.substr(3))
        updateAvatarList('participators','members')
      }
    })
  })

  $('#send-message-form').submit(function(){
    $.ajax({
      data:{
        request_type:'send_message',
        request_phrase:$.toJSON($('#send-message-form').serializeJSON())
      },
      success:function(){
        $(this)[0].reset()
        $('#send-message-modal').modal('hide')
      },
      error:function(){
        $('#send-message-error').slideDown('normal',function(){
          setTimeout(function(){$('#send-message-error').slideUp()},5000)
        })
      }
    })
    return false;
  })


/* alert */
  $(".alert-message").alert()


/* icons */

  function icon(icon_class){
    color = arguments[1] ? 'icon-'+arguments[1] : ""
    return $('<i></i>').addClass('icon-'+icon_class).addClass(color)
  }


/* group manager */

  function groupAction(action,dropdown_option){
    var user_id = dropdown_option.closest('.btn-group').attr('user-id')
    console.log(user_id)
    $.ajax({
      data:{
        request_type:action, // remove_member, grant_admin, revoke_admin
        request_phrase:$.toJSON(
          {
            group:getCurrentGroup(),
            user:user_id,
          }
        )
      },
      success:function(data){
       if($('#member-search').val()){
          $('#member-search').data('term_cache','').membersearch('search')
        }else{
          $.ajax({
            data:{
              request_type:'member',
              request_phrase:$.toJSON(
                {
                  group:getCurrentGroup(),
                  term:'*',
                  filter:$('#filter-current').attr('filter')
                }
              )
            },
            success:function(data){
              parseMemberSearchResult(data)
            }
          })
        }
      }
    })
  }

  $('.approve-member').click(function(){
    groupAction('approve_member',$(this))
  })

  $('.grant-admin').click(function(){
    groupAction('grant_admin',$(this))
  })

  $('.revoke-admin').click(function(){
    groupAction('revoke_admin',$(this))
  })

  $('.remove-member').click(function(){
    groupAction('remove_member',$(this))
  })

  function renderMemberSearchResult(data,is_founder){
    if(data.length){
      $.map(data,function(item){
        if(!item.avatar){
          item.avatar='/static/images/no_avatar.png'
        }
        buttons=$('<td></td>').addClass('member-actions').append("\n").append(
          $('<div></div>').addClass('btn-group').attr('user-id',item.id)
        )
        btn_group = buttons.find('div')
        if(item.is_admin){
          btn_group.append(
            $('<a></a>').addClass('btn btn-primary dropdown-toggle').attr('data-toggle','dropdown').append(icon('user','white')).append('\n管理员').append("\n").append(
              $('<span></span>').addClass('caret')
            )
          ).append(
            $('<ul></ul>').addClass('dropdown-menu').append(
              function(){
                return is_founder ? $('<li></li>').append(
                  $('<a></a>').addClass('revoke-admin').attr('href','#').text('\n撤销管理员').click(
                    function(){
                      groupAction('revoke_admin',$(this))
                    })
                ) : ""
              }
            )
          )
        }else{
          if(item.is_approved){
            btn_group.append(
              $('<a></a>').addClass('btn btn-success dropdown-toggle').attr('data-toggle','dropdown').append(icon('user','white')).append('\n普通成员').append("\n").append(
                $('<span></span>').addClass('caret')
              )
            )
          }else{
            btn_group.append(
              $('<a></a>').addClass('btn dropdown-toggle').attr('data-toggle','dropdown').append(icon('user')).append('\n未审核').append("\n").append(
                $('<span></span>').addClass('caret')
              )
            )
          }
          btn_group.append(
            $('<ul></ul>').addClass('dropdown-menu').append(
              function(){
                return is_founder ? $('<li></li>').append(
                  $('<a></a>').addClass('grant-admin').attr('href','#').text('\n设为管理员').click(
                    function(){
                      groupAction('grant_admin',$(this))
                    })
                ) : ""
              }
            )
          )
          if(!item.is_approved){
            buttons.find('div>ul').prepend(
              $('<li></li>').append(
                $('<a></a>').addClass('approve-member').attr('href','#').text('\n批准加入').click(
                  function(){
                  groupAction('approve_member',$(this))
                })
              )
            )
          }
        }
        if(item.is_admin&&!is_founder){
          buttons.find('div>ul').append(
            $('<li></li>').append(
              $('<a></a>').attr('href','#').text('\n你想做什么？')
            )
          )
        }else{
          buttons.find('div>ul').append(
            $('<li></li>').append(
              $('<a></a>').addClass('remove-member').attr('href','#').text('\n从组织中移除').click(
                function(){
                  groupAction('remove_member',$(this))
                })
            )
          )
        }
        $('<tr></tr>').append(
          $('<td></td>').addClass('avatar').append(
            $('<a></a>').attr('href','/members/'+item.slug).append(
              $('<img>').addClass('avatar').attr('src',item.avatar)
            )
          )
        ).append(
          $('<td></td>').append(
            $('<h4></h4>').text(item.name).append(
              $('<small></small>').append('(').append(
                $('<a></a>').attr('href','/members/'+item.slug).text(item.slug)
              ).append(')')
            )
          ).append(
            $('<p></p>').text(item.description)
          )
        ).append(buttons).appendTo($('#member-search-result'))
      })
    }else{
      $('#member-search-result').text('没有匹配的成员，请重试')
    }
    $('#member-search-result').addClass('in')
  }

  $.widget( "custom.membersearch", $.ui.autocomplete, {
    _renderMenu: function( ul, data ) {
      parseMemberSearchResult(data)
    },
  });

  function parseMemberSearchResult(data){
    data=data[0]
    if($('#member-search').data('digest')==data.digest){
      return
    }else{
      $('#member-search-result').html('')
      $('#member-search').data('digest',data.digest)
      $('#member-search-result').removeClass('in')
      setTimeout(function(){
        renderMemberSearchResult(data.data,data.is_founder)
      },150)
    }
  }

  $('#member-search').data('group',getCurrentGroup()).data('digest','').data('term_cache','').membersearch({
    source:function(request,response){
      $.ajax({
        data:{
          request_type:'member',
          request_phrase:$.toJSON(
            {
              group:$('#member-search').data('group'),
              term:request.term,
              filter:$('#filter-current').attr('filter'),
            }
          )
        },
        success:function(data){
          response(data)
        }
      })
    },
    search:function(event,ui){
      var input=$('#member-search')
      var real_term = input.val().trim()
      if(real_term==input.data('term_cache')){return false}else{input.data('term_cache',real_term)}
    }
  })

  $('.filter-option').click(function(){
    $('#filter-current').text($(this).text()).attr('filter',$(this).attr('filter'))
    if($('#member-search').val()){
      $('#member-search').data('term_cache','').membersearch('search')
    }else{
      $.ajax({
        data:{
          request_type:'member',
          request_phrase:$.toJSON(
            {
              group:getCurrentGroup(),
              term:'*',
              filter:$('#filter-current').attr('filter')
            }
          )
        },
        success:function(data){
          parseMemberSearchResult(data)
        }
      })
    }
  })

  /* activity manager */

  function activityManage(){
    $.ajax({
      data:{
        request_type:$(this).attr('class').replace(/-/g,'_'),
        request_phrase:$.toJSON({
          activity:$(this).closest('.btn-group').attr('activity-id'),
          group:getCurrentGroup(),
        })
      },
      success:function(){
        location.reload()
      }
    })
  }

  $('.accept-activity, .remove-activity, .cancle-cooperation').click(activityManage)

  /* float fix */
  $('#main>ul.list>li.activity:odd').each(function(index,element){
    var height = $(element).height()
    if($(element).prev())>height){
      $(element).height($(element).prev().height())
    }else{
      $(element).prev().height(height)
    }
  })
})