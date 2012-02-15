  /* photo uploader */

  $('#upload-activity-photo-input').uploadify({
    'uploader'  : '/static/uploadify.swf',
    'script'    : '/upload/',
    'cancelImg' : '/static/images/uploadify-cancel.png',
    'buttonText'  : 'Select photos',
    'auto'        : true,
    'wmode'     : 'transparent',
    'multi'     : true,
    'fileExt'   : '*.jpg;*.gif;*.png',
    'fileDesc'    : 'Web Image Files(*.jpg,*.gif,*.png)',
    'scriptData' : {'save_to':'photos'},
    'onComplete'  : function(event, ID, fileObj, response, data){
      response = $.parseJSON(response);
      response.path = response.path.replace(/\\\\/g,"\\");
      response.path = response.path.replace(/\\/g,"/");
      if ( response.width>240 ){
        response.width = 240
      }
      $('<li></li>').addClass('preview').width(240).append(
        $('<div></div>').addClass('thumbnail').append(
          $('<img>').attr('src',response.path).width(response.width)
        ).append(
          $('<textarea></textarea>').width(220).height(40).attr('placeholder','（没有描述）').css('margin-top','6px').css('min-height','40px')
        )
      ).appendTo('#upload-activity-photo-preview').find('img').load(function(){
        $(this).end().show('scale',{},800)
      })
    }
  })

  $('upload-activity-photo-modal').bind('hidden',function(){
    $('#upload-activity-photo-preview').html("")
  })

  $('#save-activity-photo').click(function(){
    var photos = []
    $('#upload-activity-photo-preview>li').each(function(index,element){
      photos[index] = {
        src:$(element).find('img').attr('src'),
        description:$(element).find('textarea').val(),
      }
    })
    $.ajax({
      data:{
        request_type:'save_activity_photos',
        request_phrase:$.toJSON({
          activity:getCurrentActivity(),
          photos:photos,
        })
      },
      success:function(){
        $('#upload-activity-photo-modal').modal('hide')
      },
      error:function(){
        $('#save-photo-error').slideDown('normal',function(){
          setTimeout(function(){$('#save-photo-error').slideUp()},5000)
        })
      }
    })
  })