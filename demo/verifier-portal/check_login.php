<?php

require_once "lib/orm.php";

run();

function run()
{
    checkMethod(['GET', 'OPTIONS']);
    checkLogin();
}

function checkLogin()
{
    if (!isset($_GET['id'])) {
        http_response_code(401);
        die('Request not valid');
    }

    $loginRequest = retrieveLoginRequest($_GET['id']);
    if (!is_null($loginRequest) && !empty($loginRequest) && $loginRequest['result'] == 1) {
        $data = json_decode($loginRequest["data"], true);
        die($data["callback"]);
    } else {
        die("false");
    }
}


function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}