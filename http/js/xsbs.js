function getClientState(hostname, cn, callback) {
	$.getJSON('http://' + hostname + '/json/clients/' + cn), function(data) {
		callback(data);
	}
}

function foreachClient(hostname, callback) {
	getClients(hostname, function(clients) {
		$.each(clients, function(i, client) {
			callback(client)
			});
		});
}

function getClients(hostname, callback) {
	$.getJSON('http://' + hostname + '/json/clients', function(data) {
		callback(data);
		});
}
