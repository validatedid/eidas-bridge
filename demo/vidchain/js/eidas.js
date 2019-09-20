$(function() {
    $("#load-qec .glyphicon").hide();
});

function buf2hex(buffer) { // buffer is an ArrayBuffer
    return Array.prototype.map.call(new Uint8Array(buffer), x => ('00' + x.toString(16)).slice(-2)).join('');
}

$("#select_qec").click(function(e){
    e.preventDefault();
    $("#file-input").trigger('click');
 });

$('input[type="file"]').change(function(e){
    // getting a hold of the file reference
    var file = e.target.files[0];
    // setting up the reader
    var reader = new FileReader();

    reader.onload = function () {
        var resultHexString = buf2hex(reader.result);
        loadQEC(resultHexString);
    };

    reader.readAsArrayBuffer(file);
});

function loadQEC (p12data) {

    var data = {
        "did": "did:example:21tDAKCERh95uGgKbJNHYp",
        "p12data": p12data,
        "password": "passphrase"
    };

    $.ajax({
        type: "POST",
        url: "http://localhost:5002/eidas/load-qec",
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: onValidationSuccess
    });
}

function onValidationSuccess(data) {
    if (data.result) {
        alert("eIDAS Certificate and keys imported successfully!");
    } else {
        console.error('Error');
    }
}