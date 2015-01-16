function piDisplayConfig() {
	showSettings();
	clickUpdateGif();
	autoUpdate();
	prevGif();
	categorySelect();
	setDelay();
	showPrevious();
	prev5();
	theaterButton();
	openSavedGifs();
	saveGif();
}

function showNotification(message) {
	var html = '<span>' + message + '</span>';
	$('#notification').empty();
	$('#notification').fadeIn(100);
	$('#notification').append(html);
	setTimeout(fadeNotification, 2000)
}

function fadeNotification() {
	$('#notification').fadeOut('slow');
}

function updateGif() {
	console.log('Updating GIF...');
	$('#dynamic-image').remove();
	$('#normal-image').remove();
	$.getJSON($SCRIPT_ROOT + '/pi-display-config-update', {
	}, function(data) {
		var html = '<img id="normal-image" style="display:none;" id="img" src="' + data['current_gif'] + '">';
		$('#image').append(html);
		$('#normal-image').fadeIn('slow');
		$('#normal-image').imgCentering();
		showNotification(data['message']);
	});
	return false;
}

function buttonSelect(idName) {
	var buttons = ['#all', '#animals', '#gaming', '#strange', '#educational'];
	for (i = 0; i < buttons.length; i++) {
		$(buttons[i]).removeClass('button-selected');
	}
	$(idName).addClass('button-selected');
}

function categoryAjax(selection) {
	$.getJSON($SCRIPT_ROOT + '/pi-display-config-categories', {
		category: selection
	}, function(data) {
		showNotification(data['message']);
		updateCurrentSettings(data['category'], data['delay']);
	});
	return false;
}

function updateCurrentSettings(category, delay) {
	$('#current-settings').empty();
	var html = '<span>' + category + '</span><span>' + delay + ' seconds</span>';
	$('#current-settings').append(html);
}

function populateImages() {
	$('#last-played').fadeIn('fast');
	$.getJSON($SCRIPT_ROOT + '/previous-gifs', {
	}, function(data) {
		var html = '<div style="display: none;" id="' + data['id'] + '" class="last-played-images"></div>';
		$('#last-played').append(html);
		for (var i = 0; i < data['prev_5'].length; i++) {
			var image = '<img src="' + data['prev_5'][i] + '" class="animate">';
			$('#' + data['id']).append(image);
		};
		$('#' + data['id']).fadeIn('slow');
		clickImage();
	});
	return false;
}

function theaterMode() {
	$('body').css('background-image', 'none');
	$('body').css('background-color', '#000');
	$('#image').css({
		'width': 1024,
		'height': 768,
		'margin-left': '-=192px'
	});
	$('#dynamic-image').css({
		'width': 1024,
		'height': 768,
	});

	$('#title').css('margin-top', '-=125px');
	$("#image img").imgCentering();
	$("#dynamic-image img").imgCentering();
}

function removeTheater() {
	$('body').css('background-color', '#FFF');
	$('body').css('background-image', 'url(../static/images/pi_display_config/swirl_pattern.png)');
	$('#image').css({
		'width': 640,
		'height': 480,
		'margin-left': '+=192px'
	});

	$('#dynamic-image').css({
		'width': 640,
		'height': 480,
	});

	$('#title').css('margin-top', '+=125px');
	$("#image img").imgCentering();
	$("#dynamic-image img").imgCentering();
}

function showEmailGif() {
	$('#email-icon, #icon-label').remove();
	var html = '<div style="display: none;" id="email-div"><input id="email" type="text" placeholder="Email Address"><input id="email-gifs" type="submit" value="Submit" class="animate"></div>';
	$('#save-gif').append(html);
	$('#email-div').fadeIn('fast');
}

// Functions bound to HTML elements via click
function showSettings() {
	$('#settings-button').on('click', function() {
		$('#settings').fadeIn('fast');
	});
	$('#settings-close').on('click', function() {
		$('#settings').fadeOut('fast');
	});
}

function clickUpdateGif() {
	$('#update-gif').on('click', function() {
		updateGif();
	});
}

function autoUpdate() {
	var clicked = false;
	$('#auto-update').on('click', function() {
		if (clicked) {
			clearInterval(window.delay);
			clicked = false;
			$(this).removeClass('selected');
			var message = 'Auto Update Off';
		    showNotification(message);
		} else {
			clearInterval(window.delay);
			clicked = true;
			$(this).addClass('selected');
			$.getJSON($SCRIPT_ROOT + '/pi-display-config-auto', function(data) {
		        delay = data['delay'];
		        window.delay = setInterval(updateGif, delay);
		        var message = 'Auto Update On';
		        showNotification(message);
		    });
		    return false
		}
	});
}

function prevGif() {
	$('#prev-gif').on('click', function() {
		$.getJSON($SCRIPT_ROOT + '/pi-display-config-prev', {
		}, function(data) {
			var html = '<img style="display: none;" id="dynamic-image" src="' + data['last_played'] + '">';
			$('#image img').remove();
			$('#dynamic-image').remove();
			$('#image').append(html);
			$("#dynamic-image").fadeIn('slow');
			$("#dynamic-image img").imgCentering();
			showNotification(data['message']);
		});
		return false;
	});
}

function categorySelect() {
	$('#all').on('click', function() {
		var selection = 'all';
		categoryAjax(selection);
		buttonSelect('#all');
	});
	$('#animals').on('click', function() {
		var selection = 'animals';
		categoryAjax(selection);
		buttonSelect('#animals');
	});
	$('#gaming').on('click', function() {
		var selection = 'gaming';
		categoryAjax(selection);
		buttonSelect('#gaming');
	});
	$('#strange').on('click', function() {
		var selection = 'strange';
		categoryAjax(selection);
		buttonSelect('#strange');
	});
	$('#educational').on('click', function() {
		var selection = 'educational';
		categoryAjax(selection);
		buttonSelect('#educational');
	});
}

function setDelay() {
	$('#submit').on('click', function() {
	    var delay = $('#delay').val();
	    if (delay >= 5) {
		    $.getJSON($SCRIPT_ROOT + '/pi-display-config-delay', {
				delay: delay
			}, function(data) {
				showNotification(data['message']);
				$('#delay').val('');
				updateCurrentSettings(data['category'], data['delay']);
			});
			return false;
		} else {
			message = 'Delay must be at least 5 seconds';
			showNotification(message);
		}
	});
}

function showPrevious() {
	var clicked = false;
	$('#previous-button').on('click', function() {
		if (clicked) {
			clicked = false;
			closePrevious();
			$(this).removeClass('button-selected');
			$('#title').css('margin-top', '+=50px');
	} else {
		clicked = true;
		$(this).addClass('button-selected');
		$('#title').css('margin-top', '-=50px');
		$('#last-played').fadeIn('fast');
		populateImages();
		}
	});
}

function closePrevious() {
	$('#previous-button').removeClass('button-selected');
	$('#last-played').fadeOut('fast');
	$.getJSON($SCRIPT_ROOT + '/clear-session', {
	}, function(data) {
		console.log(data['message']);
		$('.last-played-images').remove();
	});
	return false;
}

function prev5() {
	$('#prev-5-gifs').on('click', function() {
		populateImages();
	});
}

function theaterButton() {
	var clicked = false;
	$('#theater-button').on('click', function() {
		if (clicked) {
			clicked = false;
			$(this).removeClass('button-selected');
			removeTheater();
			$('#title').css('display', 'block');
		} else {
			clicked = true;
			$(this).addClass('button-selected');
			$('#title').css('display', 'none');
			theaterMode();
		}
	});
}

function clickImage() {
	$('#last-played img').on('click', function() {
		$('#dynamic-image').remove();
		$('#normal-image').remove();
		var url = $(this)[0].src;
		var imageHeight = $('#image').height();
		if (imageHeight === 768) {
		    var html = '<div style="width: 1024px; height: 768px;" id="dynamic-image"><img src="' + url + '"></div>';
		} else {
		    var html = '<div id="dynamic-image"><img src="' + url + '"></div>';
		}
		$('#image').prepend(html);
		$('#dynamic-image').fadeIn('slow');
		$('#dynamic-image img').imgCentering();
	});
}

function openSavedGifs() {
	$('#open-saved').on('click', function() {
		$('#email-icon, #icon-label, #email-div').remove();
		var html = '<i id="email-icon" class="fa fa-paper-plane-o fa-2x animate"></i><span id="icon-label">Email GIFs</span>';
		$('#save-gif').append(html);
		$('#save-gif').fadeIn('fast');
		$('#email-icon').on('click', function() {
			$('#email-link').remove();
			showEmailGif();
			sendEmail();
		});
	});
	$('#save-close').on('click', function() {
		$('#email-div').fadeOut('fast');
		$('#save-gif').fadeOut('fast');
	});
	$('#email-icon').on('click', function() {
		$('#email-link').remove();
		showEmailGif();
		sendEmail();
	});	
}

function saveGif() {
	$('#save-button').on('click', function() {
		var dynamicImg = $('#dynamic-image img').length;
		if (dynamicImg) {
			var url = $('#dynamic-image img')[0].src;		
		} else {
			var url = $('#image img')[0].src;
		}
		var html = '<div class="saved-gif"><i class="fa fa-times save-img-close animate"></i><img style="height: 50px; width: 50px;" src="' + url + '" class="animate"></div>';
		var message = 'GIF Saved!';
		$('#saved-images').append(html);
		showNotification(message);
		removeSavedGif();
	});
}

function removeSavedGif() {
	$('.save-img-close').on('click', function() {
		$(this).parent().remove();
	});
}

function sendEmail() {
	$('#email-gifs').on('click', function() {
		$('#email-link').remove();
		var email = $('#email').val();
		var images = $('#saved-images').find('img').map(function() {
			return $(this).attr('src')
		}).get();

		var imagesArray = JSON.stringify(images);

		$.getJSON($SCRIPT_ROOT + '/email-gifs', {
			email: email,
			images: imagesArray
		}, function(data) {
			$('#email-div').fadeOut('fast');
			var html = '<a href="' + data['link'] + '"><div id="email-link" class="animate">Email</div></a>';
			$('#save-gif').append(html);
		});
		return false;		
	});
};