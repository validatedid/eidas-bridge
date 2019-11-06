$(function() {

    let eidasBtn = document.getElementById("setup_eidas");
    let eidasSubmit = document.getElementById("submiteidas");

    eidasBtn.onclick = function(){
        $("#eidasModal").modal();
    };

    eidasSubmit.onclick = function(){
        var password = document.getElementById("psw").value;
        var file = document.getElementById("p12file").files[0];

        // setting up the reader
        var reader = new FileReader();

        reader.onload = function () {
            var resultHexString = buf2hex(reader.result);
            var did = getDID();
            loadQEC(resultHexString, password, did);
            $("#eidasModal").modal('hide');
        };

        reader.readAsArrayBuffer(file);
    };
});

function getDID() {
    return "did:example:21tDAKCERh95uGgKbJNHYp";
}

function buf2hex(buffer) { // buffer is an ArrayBuffer
    return Array.prototype.map.call(new Uint8Array(buffer), x => ('00' + x.toString(16)).slice(-2)).join('');
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
        success: function(data, textStatus){
            updateDIDDoc(getDID());
            console.log("Certificate Loaded Sucessfully!");
            $('.genric-btn.primary').css('display','none');
            $('.eidas-text').css('display','none');
            $('.eidas-success').show();
        }
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
        success: function(data, textStatus){
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
        }
    });
}