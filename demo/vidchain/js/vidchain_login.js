$(function() {
   setInterval(checkLogin, 2000);
});

var checkLogin = function() {
    $.ajax({
        data:  {id: qrId},
        url:   'https://vidchain-demo-acmecompany.azurewebsites.net/check_login.php',
        type:  'get',
        success:  function (result) {
            if(result !== 'false'){
                window.top.location.href = result;
            }
        }
    });
};
