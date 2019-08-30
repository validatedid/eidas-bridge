<?php

/**
 * POST /login
 *
 * body: {
 *      callback: "callback_url",
 *      requester: "requester_id",
 *      userinfo: "user_scope"
 * }
 *
 */

include_once "./lib/orm.php";

run();


function run()
{
    checkMethod(['POST', 'OPTIONS']);

    $postBody = [];

    try {
        $postBody = json_decode(file_get_contents('php://input'), true);
        $_callbackUrl = $postBody['callback'];
        $_requester = $postBody['requester'];
        $_userInfo = $postBody['userinfo'];
    } catch (Exception $e) {
        http_response_code(400);
        die();
    }

    $_requestId = persistLoginRequest($postBody);
    header("Content-Type: application/json");
    echo json_encode(["id" => $_requestId]);
    die();
}

function persistLoginRequest($parameters)
{
    $_requestId = createLoginRequest($parameters["userinfo"], $parameters["requester"], $parameters["callback"]);
    return $_requestId;
}


function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}