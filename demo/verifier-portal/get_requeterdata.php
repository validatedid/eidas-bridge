<?php
/**
 * POST /validate_email
 *
 * body: {
 *      email: "email"
 * }
 *
 */

/**
 * PUT /validate_email
 *
 * body: {
 *      id: "request_id"
 *      code: "verification_code"
 * }
 *
 */

include_once "lib/orm.php";

$funcs= [
    "GET" => "getRequesterData"
];

run();


function run()
{
    global $funcs;

    checkMethod(['GET']);
    call_user_func($funcs[$_SERVER['REQUEST_METHOD']]);
}

function getRequesterData()
{
    $_requesterid = $_GET['id'];
    $_requester = retrieveRequester($_requesterid);
	header('Content-Type: application/json');
    echo json_encode([
        "requester" => $_requester
    ]);
    die();
}
function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}