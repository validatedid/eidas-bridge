$(function() {
    $("#login-button .glyphicon").hide();
});

function loginWithVIDChain () {
    $("#login-button .glyphicon").show();

    var callback  = "http://vidchainpoc.azurewebsites.net/site/index.html";
    //var callback  = "http://localhost/ViDChainBackend/site/fake/index.html";
    var requester = 2;
    var userInfo  = ["name", "email", "phone", "photo"];

    var data = {
        "callback": callback,
        "requester": requester,
        "userinfo": userInfo
    };

    $.ajax({
        type: "POST",
        url: "http://vidchainpoc.azurewebsites.net/login.php",
        //url: "http://localhost/ViDChainBackend/login.php",
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
                //url: "http://localhost/ViDChainBackend/site/vidchain/login.php?p="+data.id,
                url: "http://vidchainpoc.azurewebsites.net/site/vidchain/login.php?p="+data.id,
                size:"lg"
            }
        );
        $("#login-button .glyphicon").hide();
    } else {
        console.error('Error');
    }
}



