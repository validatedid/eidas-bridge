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

include_once "./lib/orm.php";
include_once "./lib/ionic_push.php";

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
	$_message = "The Educature University wants to send you a ".$attribute." diploma, do you want to save this education?";
    $_payload = [
        // "requester" => $requester,
        "requester" => 2, // !!! hack to be able to send an education attribute and be received correctly by the app. Need to update the app to support multiples requesters.
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