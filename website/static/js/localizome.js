$(document).ready(function(){
	setResizeHandler();
	positionFooter();
	showProteinDownloads();
	initializeVideoPlayer();
	toggleSummaryLength();
	toggleVideo();
	selectDefaultVideo();
	spatiotemporalLinks();
	fixSpatiotemporalResultsRows();
	matrixAxisHighlight();
	confirmDownload();
	hoverTags();
})

setResizeHandler = function() {
	$(window).resize(function() {
		positionFooter();
	})
}

positionFooter = function() {
	footer = $("#wrap-footer");
	footerHeight = footer.outerHeight();
	windowHeight = $(window).height();
	contentHeight = $("html").height();

	// if footer is absolute, it is not included in the content height, so add it
	if (footer.css("position") == "absolute") {
		contentHeight += footerHeight;
	}

	console.log(contentHeight, windowHeight);

	// if content is smaller than window, position the footer at bottom of page
	// otherwise position it statically (necessary in case user resizes window)
	footer.css(
		(contentHeight < windowHeight) ? {
			position: "absolute",
			bottom: "0",
			left: "0"
		} : {
			position: "static"
		}
	)
}

showProteinDownloads = function(){
	$("select[name=protein]").change(function(){
		if ($(this).val() != undefined) {
			window.location = $(this).data("path") + $(this).val();
		}
	});
}

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
		
		$(".matrix").is(":visible") ? $("#next-to-matrix").show() : $("#next-to-matrix").hide();
	});
}

selectDefaultVideo = function(){
	$("[data-video-link]").first().trigger("click"); // trigger the first link (in case no rep)
	repVideoId = $("[data-video-representative]").attr("data-video-link"); // get rep video
	$("[data-video-link='" + repVideoId + "']").trigger("click"); // trigger the rep video
}

spatiotemporalLinks = function(){
	path = $("div#spatiotemporal").data("path");
	
	// run the contents of this function whenever you click a td
	$("div#spatiotemporal td").click(function(){

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
		link = path + "compartment" + rowId + "/timepoint" + columnId;
		window.location = link;
	});

	$("div#spatiotemporal th.compartment").click(function(){
		rowId = $(this).data("id");
		link = path + "compartment" + rowId;
		window.location = link;
	});
	
	$("div#spatiotemporal th.timepoint").click(function(){
		columnId = $(this).data("id");
		link = path + "timepoint" + columnId;
		window.location = link;
	});
}

fixSpatiotemporalResultsRows = function(){
	if ($("#spatiotemporal-results").length) {	
		var tableOffset = $("#spatiotemporal-results").offset().top;
		var $header = $("#spatiotemporal-results > thead").clone();
		var $fixedHeader = $("#table-thead-fixed").append($header);

		$(window).bind("scroll", function() {
					var offset = $(this).scrollTop();
					if (offset >= tableOffset && $fixedHeader.is(":hidden")) {
						$fixedHeader.show();
					} else if (offset < tableOffset) {
						$fixedHeader.hide();
					}
		});
	}
}

matrixAxisHighlight = function(){
	$("td.signal").mouseover(function(){
		$(this).siblings(".row-header").addClass("highlight");
		index = $(this).siblings("td").index($(this).prev()) + 1;
		$(this).closest(".matrix").find(".timepoint").eq(index).addClass("highlight");
		$("#table-thead-fixed").find(".timepoint").eq(index).addClass("highlight");
	}).mouseout(function(){
		$(this).siblings(".row-header").removeClass("highlight");	
		index = $(this).siblings("td").index($(this).prev()) + 1;
		$(this).closest(".matrix").find(".timepoint").eq(index).removeClass("highlight");
		$("#table-thead-fixed").find(".timepoint").eq(index).removeClass("highlight");
	});
}

confirmDownload = function(){
	$("li#zipped-avi").click(function(){
		var answer = confirm("This is a big download. Are you sure?");
		if (answer) {
			window.open('/static/project_wide_downloads/localizome_avi_videos.zip');
		} else {
			alert("Download cancelled.");
		}
	});
	$("li#zipped-png").click(function(){
		var answer = confirm("This is a big download. Are you sure?");
		if (answer) {
			window.open('/static/project_wide_downloads/localizome_image_sequences.zip');
		} else {
			alert("Download cancelled.");
		}
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
