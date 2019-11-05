$(function() {

    let eidasBtn = document.getElementById("setup_eidas");
    let eidasSubmit = document.getElementById("eidasModal");
    let diddocBtn = document.getElementById("updated_diddoc");

    eidasBtn.onclick = function(){
        $("#eidasModal").modal();
    };

    eidasSubmit.onsubmit = function(){
        var password = document.getElementById("psw").value;
        var file = document.getElementById("p12file").files[0];

        // setting up the reader
        var reader = new FileReader();

        reader.onload = function () {
            var resultHexString = buf2hex(reader.result);
            var did = getDID();
            loadQEC(resultHexString, password, did);
        };

        reader.readAsArrayBuffer(file);
    };

    diddocBtn.onclick = function(){
        did = getDID();
        updateDIDDoc (did);
    };

});

function getDID() {
    return "did:example:21tDAKCERh95uGgKbJNHYp";
}

function buf2hex(buffer) { // buffer is an ArrayBuffer
    return Array.prototype.map.call(new Uint8Array(buffer), x => ('00' + x.toString(16)).slice(-2)).join('');
}

async function loadQECPOST (p12data, input_password, input_did) {

    var data_in = {
        "did": input_did,
        "p12data": p12data,
        "password": input_password
    };

    const response = await fetch('http://localhost:5002/eidas/load-qec', {
        method: 'POST',
        body: JSON.stringify(data_in),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    let result = await response.json();
    alert("eIDAS call went successfully!");
    return result;
}

function loadQEC (p12data, input_password, input_did) {

    var data_in = {
        "did": input_did,
        "p12data": p12data,
        "password": input_password
    };

    $.ajax({
        type: "POST",
        url: "http://localhost:5002/eidas/load-qec",
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify(data_in),
        success: onValidationSuccess
    });
}

function updateDIDDoc(input_did) {
    // TODO: connect to Enterprise Agent to update the DID Doc
    // and for doing that it needs to get the public key from the loaded 
    // eIDAS certificate and get the ID Hub endpoint.
    // In the following code we will just test the eIDAS Bridge API calls
    // to test that the library is working.

    var pubkey_data = {
        "did": input_did
    };

    // GET PUBLIC KEY
    $.ajax({
        type: "POST",
        url: "http://localhost:5002/eidas/get-pubkey",
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify(pubkey_data),
        success: function(data){
        }
    });

    var hub_data = {
        "did": input_did,
        "service_endpoint": "http://service_endpoint.sample/" + input_did + "/eidas"
    };

    // GET ID HUB ENDPOINT
    $.ajax({
        type: "POST",
        url: "http://localhost:5002/eidas/service-endpoint",
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify(hub_data),
        success:  function(data, textStatus, jqXHR){ 
            $('#register').html('<h1>Login successfull</h1>');
        }
    });
}

function onValidationSuccess(data) {
    alert("OUT: eIDAS call went successfully!");
    if (data.result) {
        console.log("eIDAS call went successfully!");
        alert("eIDAS call went successfully!");
    } else {
        console.error('Error');
    }
}