$(function() {
   setInterval(checkLogin, 2000);
});

var checkLogin = function() {
    $.ajax({
        data:  {id: qrId},
        url:   'http://vidchainpoc.azurewebsites.net/check_login.php',
        //url:   'http://localhost/ViDChainBackend/check_login.php',
        type:  'get',
        success:  function (result) {
            if(result !== 'false'){
                window.top.location.href = result;
            }
        }
    });
};
