$(document).ready(function(){
	hoverTags()
})

  window.hoverTags = function() {
    $('body').on('mouseover', '[data-hover-tag]', function(e) {
      var left_offset, name, old_title, pointer_styles, position, tag, tag_styles, target, top_offset;
      target = $(this).closest('[data-hover-tag]');
      name = unescape(target.attr('data-hover-tag'));

      position = target.offset();
      if ($('.hover_tag').length === 0) {
        tag_styles = {
          position: 'absolute',
          display: 'none',
          padding: '4px 6px 2px',
          background: 'black',
          background: 'rgba(0,0,0,0.8)',
          color: 'white',
          fontSize: '13px',
          zIndex: 800,
          textShadow: 'none',
	  borderRadius: '4px'
        };
        pointer_styles = {
          position: 'absolute',
          bottom: '-6px',
          right: '5px',
          width: '8px',
          height: '6px',
          background: 'url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAGCAYAAAD+Bd/7AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAEpJREFUeNpiZGBg2AzEkgzYwXNGIGEMxDNxKEhnBqkCYl4g1kWTXA7EaxmhHJCCZUhWgTRFAfFnZB0gq85AsTEOKxmKoRgOAAIMAEyPC0YZftrNAAAAAElFTkSuQmCC) no-repeat'
        };
        $('body').append("        <div class='hover_tag'>          <div class='text'></div>          <div class='tag_pointer'></div>        </div>");
        $('.hover_tag').css(tag_styles);
        $('.hover_tag .tag_pointer').css(pointer_styles);
      }
      tag = $('.hover_tag');
      tag.find('.text').html(name);
      top_offset = -7;
      left_offset = 5;
      if (target.data('hover-tag-top')) {
        top_offset = target.data('hover-tag-top');
      }
      if (target.data('hover-tag-left')) {
        left_offset = target.data('hover-tag-left');
      }
      return tag.css({
        top: position.top - tag.outerHeight() + top_offset,
        left: position.left - tag.outerWidth() + target.width() / 2 + 3 + left_offset // "3" for half of the pointer's width
      }).show();
    });
    return $('body').on('mouseout', '[data-hover-tag]', function(e) {
      return $('.hover_tag').hide();
    });
  };
