function getScoreboard(hostname, callback) {
	$.getJSON('http://' + hostname + '/json/scoreboard' + cn, function(data) {
		callback(data);
	});
}

function getClientState(hostname, cn, callback) {
	$.getJSON('http://' + hostname + '/json/clients/' + cn, function(data) {
		callback(data);
		});
}

function getClients(hostname, callback) {
	$.getJSON('http://' + hostname + '/json/clients', function(data) {
		callback(data);
		});
}

function foreachClient(hostname, callback) {
	getClients(hostname, function(clients) {
		$.each(clients, function(i, client) {
			callback(client)
			});
		});
}

function displayAlert(text) {
	$('#content').fadeTo('slow', 0.4).attr('disabled', '');
	$('<div class=\"alert_box\" id=\"alert\">' + text + '</div>').fadeIn('slow').appendTo('#alerts');
}

function clearAlert() {
	$('#alert_box').fadeOut('slow', function() {
		$('#alerts').empty();
		});
}

function loadPlayerAdminPage(username, password) {
}

function tryLogin(hostname, username, password, error_callback, success_callback) {
	$.getJSON('http://' + hostname + '/json/login?username=' + username + '&password=' + password, function(data) {
		if(data.hasOwnProperty('result') && data.result == 'SUCCESS')
			success_callback();
		else
			error_callback(data.error);
		});
}

function disableTopNav()
{
	$('#topnav_players').click(function() { });
}

function enableTopNav()
{
	$('#topnav_players').click(function() { alert('foo'); });
}

function loadLoginPage(hostname, callback) {
	html_page = '<h3>Please login</h3>Username: <input type=\"text\" id=\"username_input\" /><br />Password: <input type=\"password\" id=\"password_input\" /><br /><input type=\"submit\" value=\"Login\" id=\"login_submit\" /><br /><span id=\"login_status\"></span>';
	displayAlert(html_page);
	$('#login_submit').click(function() {
		$('#login_status').empty();
		$('#login_status').html('Trying login...');
		var username = $('#username_input').val();
		var password = $('#password_input').val();
		tryLogin(hostname, username, password, function(error_code) {
				$('#login_status').empty();
				if(error_code == 'INVALID_LOGIN')
					$('#login_status').html('Invalid login.');
				else
					$('#login_status').html('Unknown error.');
				},
			function() {
				$('#login_status').empty();
				$('#login_status').html('Success.');
				callback(username, password);
				});
		});
}

function setup(hostname) {
	loadLoginPage(hostname, function(username, password) {
		clearAlert();
		enableTopNav();
		});
}

