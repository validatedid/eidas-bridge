$(function() {
    var connection = new WebSocket('ws://vidchainpoc.azurewebsites.net:9000');

    connection.onopen = function () {
        connection.send(JSON.stringify({'action': 'new', 'id': qrId})); // Send the message 'Ping' to the server
    };

    connection.onerror = function (error) {
        console.log('WebSocket Error ' + error);
    };

    connection.onmessage = function (e) {
        console.log('Server: ' + e.data);
        window.location.href = e.data;
    };
});