/* image uploader and crop */

$(document).ready(function(){

    $('form').has('#image-uploader').find('img#preview').attr({'src':$('.span7>input[type="hidden"]').val()})

    var jcrop_api;

    $('.jcrop-holder').hide();
    
    function initJcrop() {
      jcrop_api = $.Jcrop('#image-crop-target', {
        setSelect: [0, 0, 150, 150],
        onChange: showPreview,
        onSelect: showPreview,
        aspectRatio:  1
      });
    }

    function destroyJcrop() {
      if (jcrop_api) {
        jcrop_api.destroy();
      }
    }
    
    function showPreview(coords)
    {
      var rx = 150 / coords.w;
      var ry = 150 / coords.h;
      if (parseInt(coords.w) > 0) {
        $('#image-preview').css({
          width: Math.round(rx * $('.jcrop-holder').width()) + 'px',
          height: Math.round(ry * $('.jcrop-holder').height()) + 'px',
          marginLeft: '-' + Math.round(rx * coords.x) + 'px',
          marginTop: '-' + Math.round(ry * coords.y) + 'px'
        });
      }
      updateCoords(coords);
    };
    
    function updateCoords(c)
    {
      $('#x').val(c.x);
      $('#y').val(c.y);
      $('#w').val(c.w);
      $('#h').val(c.h);
    }; 
      
    function checkCoords()
    {
      if (parseInt($('#w').val())>0) return true;
        $("#image-nocrop").modal("show");
      return false;
    }; 

    $('#image-crop').bind('shown',function(){
      $('#image-crop-target').width(350).show();
      initJcrop();
    }).bind('hide',destroyJcrop)

    $('#image-crop-confirm').click(function(){
      $.ajax({
        url:  '/crop/' + window.location.pathname.match(/\/(\w+)\//)[1],
        type: 'POST',
        data: {
          path: $('#image-path').val(),
          x: $('#x').val(),
          y: $('#y').val(),
          w: $('#w').val(),
          h: $('#h').val(),
          cw: $('.jcrop-holder').width(),
          ch: $('.jcrop-holder').height(),
        },
        dataType: 'json',
        success:  function(data){
            data.path = data.path.replace(/\\\\/g,"\\");
            data.path = data.path.replace(/\\/g,"/");
            $('.span7>input[type="hidden"]').val(data.path)
            $('#image-crop').modal("hide");
            $('#preview').attr({'src':data.path})
          },
        error: function(){
            $('#image-crop-error').slideDown('normal',function(){
              setTimeout(function(){$('#image-crop-error').slideUp()},5000)
            })
        }
        })
    })

    $('#image-uploader').uploadify({
      'uploader'      : '/static/uploadify.swf',
      'script'        : '/upload/',
      'cancelImg'   : '/static/images/uploadify-cancel.png',
      'buttonText'  : 'Upload avatar',
      'auto'        : true,
      'wmode'     : 'transparent',
      'multi'     : false,
      'fileExt'   : '*.jpg;*.gif;*.png',
      'fileDesc'    : 'Web Image Files(*.jpg,*.gif,*.png)',
      'onComplete'  : function(event, ID, fileObj, response, data) {
        response = $.parseJSON(response);
        response.path = response.path.replace(/\\\\/g,"\\");
        response.path = response.path.replace(/\\/g,"/");
        $('#image-preview').parent().show().parent().show();
        $('#image-preview, #image-crop-target').attr({'src':response.path});
        $('#image-crop-target').one('load',destroyJcrop);
        $('#image-path').val(response.path)
        $('#image-crop-target').one('load',function() {
          $('#image-crop').modal('show');
        })
      },
    })
})