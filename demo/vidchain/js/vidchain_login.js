$(function() {
   setInterval(checkLogin, 2000);
});

var checkLogin = function() {
    $.ajax({
        data:  {id: qrId},
        url:   'http://localhost:8080/vidchain/check_login.php',
        type:  'get',
        success:  function (result) {
            if(result !== 'false'){
                window.top.location.href = result;
            }
        }
    });
};
