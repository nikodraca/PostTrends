function showSnapshot(username) {
	if (!username) {
	    window.location.href = "/u/" + document.getElementById('input_value').value;
	}
	else {
	    window.location.href = "/u/" + username;
	}
}
