$(document).ready(function(){
	initializeVideoPlayer();
	toggleSummaryLength();
	toggleVideo();
	selectDefaultVideo();
	spatiotemporalLinks();
	hoverTags();
})


initializeVideoPlayer = function(){
	$('video').mediaelementplayer({
		// show framecount in timecode (##:00:00:00)
		showTimecodeFrameCount: true,
		// the order of controls you want on the control bar (and other plugins below)
		features: ['playpause','current','progress','duration','tracks','fullscreen'],
	});
}

toggleSummaryLength = function(){
	$(".toggle-summary").click(function(){
		$(this).closest("li").find(".summary-collapsed, .summary-expanded").toggleClass("invisible");
	});
}


toggleVideo = function(){
	$("[data-video-link]").click(function(e){
		e.preventDefault(); // keeps page stationary after click
		$("a").removeClass("active"); // unset previous active link
		$(this).addClass("active"); // set clicked link active
		$("[data-video-content]").addClass("invisible"); // hide all videos, matrices, summaries
		
		// hide expanded and unhide truncated summaries
		$(".summary-expanded").addClass("invisible"); 
		$(".summary-collapsed").removeClass("invisible"); 

		videoId = $(this).attr("data-video-link"); // get video id for clicked link
		$("[data-video-content='" + videoId + "']").removeClass("invisible"); // make this one visible
	});
}


selectDefaultVideo = function(){
	$("[data-video-link]").first().trigger("click"); // trigger the first link (in case no rep)
	repVideoId = $("[data-video-representative]").attr("data-video-link"); // get rep video
	$("[data-video-link='" + repVideoId + "']").trigger("click"); // trigger the rep video
}


spatiotemporalLinks = function(){
	// run the contents of this function whenever you click a td
	$("table#spatiotemporal td").click(function(){

		// get all elements on the same level (row) as the td you clicked
		// filtering for THs only, then getting the data-id attribute.
		// FYI, you can pass any selector into .siblings()
		rowId = $(this).siblings("th.compartment").data("id");
	
		// get the index number of column that we clicked in e.g., 0 for the first column, 1 for the second column, etc.
		columnIndex = $(this).closest("tr").find("td").index($(this));
			
		// get all of the elements in the first row, be they either TDs or THs,
		// then choose the Nth one, where n is columnIndex, and get the data-id attribute off of that
		columnId = $("th.timepoint").eq(columnIndex).data("id");
			
		// assemble the link
		link = "spatiotemporal/compartment" + rowId + "/timepoint" + columnId;
		window.location = link;
	});

	$("table#spatiotemporal th.compartment").click(function(){
		rowId = $(this).data("id");
		link = "spatiotemporal/compartment" + rowId;
		window.location = link;
	});
	
	$("table#spatiotemporal th.timepoint").click(function(){
		columnId = $(this).data("id");
		link = "spatiotemporal/timepoint" + columnId;
		window.location = link;
	});
}


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
				borderRadius: '4px',
				maxWidth: '250px',
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
    left_offset = -1;
    if (target.data('hover-tag-top')) {
      top_offset = target.data('hover-tag-top');
    }
    if (target.data('hover-tag-left')) {
      left_offset = target.data('hover-tag-left');
    }
    return tag.css({
      top: position.top - tag.outerHeight() + top_offset,
			left: position.left + target.width() - tag.outerWidth() + left_offset
		}).show();
  });
  return $('body').on('mouseout', '[data-hover-tag]', function(e) {
    return $('.hover_tag').hide();
  });
};
