LBP.options = {
	// if you want to use native player on iPad; default is "false"
	defaultIPadControls: true,
	
	// set up default language, en = english, de = german, fr = french, ...
	defaultLanguage: "en",
	
	// video controls bar elements;
	// by default all of them available (if present by options and in CSS theme)
	defaultControls: ["Play", "Pause", "Stop", "Progress", "Timer",
		"Playback", "Sources", "Fullscreen"],
	
	// extended controls to be shown within the player;
	// by default all of them available
	controlsExtra: ["Poster", "Embed", "Logo", "Spinner", "BigPlay"],
	
	// show controls bar below video-viewport; default is "false"
	controlsBelow: true,
	
	// (delayed) hiding of LB player controls; default is "true"
	hideControls: false,
	
	// if delayed hiding, hide controls bar after x seconds
	hideControlsTimeout: 1,
	
	// prevent hiding of controls bar if video paused; default is "false"
	hideControlsOnPause: false,
	
	// logo path/url; set up position with CSS
	//logo: "{{ STATIC_URL }}images/ee-logo.png",
}
