$(function() {

    let modalBtn = document.getElementById("select_qec")
    let eidasSubmit = document.getElementById("eidasModal")

    modalBtn.onclick = function(){
        $("#eidasModal").modal();
        // modal.style.display = "block"
    }

    eidasSubmit.onsubmit = function(e){
        var password = document.getElementById("psw").value;
        var file = document.getElementById("p12file").files[0];

        // setting up the reader
        var reader = new FileReader();

        reader.onload = function () {
            var resultHexString = buf2hex(reader.result);
            loadQEC(resultHexString, password);
        };

        reader.readAsArrayBuffer(file);
    }

});

function buf2hex(buffer) { // buffer is an ArrayBuffer
    return Array.prototype.map.call(new Uint8Array(buffer), x => ('00' + x.toString(16)).slice(-2)).join('');
}

function loadQEC (p12data, input_password) {

    var data = {
        "did": "did:example:21tDAKCERh95uGgKbJNHYp",
        "p12data": p12data,
        "password": input_password
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
        console.log("eIDAS Certificate and keys imported successfully!");
    } else {
        console.error('Error');
    }
}