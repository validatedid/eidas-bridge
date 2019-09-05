$(function() {
    $("#login-button .glyphicon").hide();
});

function loginWithVIDChain () {
    $("#login-button .glyphicon").show();

    var callback  = "http://localhost:8080/verifier-portal/site/fake/index.html";
    var requester = 6; // set the requester to the DB
    var userInfo  = ["name", "email", "phone", "photo", "education"];

    var data = {
        "callback": callback,
        "requester": requester,
        "userinfo": userInfo
    };

    $.ajax({
        type: "POST",
        url: "http://localhost:8080/verifier-portal/login.php",
        processData: false,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: onLoginSucceed
    });
}

function onLoginSucceed (data) {
    if (data.id) {
        eModal.iframe(
            {
                
                title:'ViDChain Sign in',
                url: "http://localhost:8080/verifier-portal/site/vidchain/login.php?p="+data.id,
                size:"lg"
            }
        );
        $("#login-button .glyphicon").hide();
    } else {
        console.error('Error');
    }
}



