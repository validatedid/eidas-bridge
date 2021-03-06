<?php

/**
 * POST /validate_attribute
 *
 * body: {
 *      requester: "requester_id",
 *      attribute: "attribute",
 *      token: "push_token"
 * }
 *
 */

include_once "lib/orm.php";
include_once "lib/ionic_push.php";

run();


function run()
{
    checkMethod(['POST', 'OPTIONS']);

    try {
        $postBody = json_decode(file_get_contents('php://input'), true);
        $_requesterId = $postBody['requester'];
        $_attribute = $postBody['attribute'];
        $_token = $postBody['token'];
    } catch (Exception $e) {
        http_response_code(400);
        die();
    }

    $_requester = retrieveRequester($_requesterId);

    $_result = sendValidatedAttribute($_requester, $_attribute, $_token);

    header("Content-Type: application/json");
    echo json_encode(["result" => $_result]);
    die();
}

function sendValidatedAttribute($requester, $attribute, $token)
{
    //$_message = "Validate ".$attribute;
	$_message = "The University want to send to you a ".$attribute." education, do you want to save this education?";
    $_payload = [
        "requester" => $requester,
        "attribute" => $attribute
    ];

    return sendPushNotification($_message, $_payload, $token);
}

function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}