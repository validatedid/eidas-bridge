<?php

/**
 * GET /confirm_login
 * POST /confirm_login
 *
 * Query Params:
 *      * id => Request id
 *
 * Post body:
 *  {
 *      attribute_1: "attribute_value",
 *      attribute_2: "attribute_value2"
 *  }
 *
 */

define("PHOTO_ATTRIBUTE", "photo");

require_once "lib/orm.php";

$funcs= [
    "GET" => "returnRequestedValues",
    "POST" => "persistAttributes"
];

run();

function run()
{
    global $funcs;

    checkMethod(['GET', 'POST', 'OPTIONS']);
    call_user_func($funcs[$_SERVER['REQUEST_METHOD']]);
}

function returnRequestedValues()
{
    session_start();
    $_SESSION['id'] = $_GET["id"];

    $req = retrieveLoginRequest($_SESSION["id"]);
    if (is_null($req) || empty($req) || !isset($req["scope"])) {
        http_response_code(404);
        die('Login not valid');
    }

    $userInfo = json_decode($req["scope"]);
    $requester = retrieveRequester($req["requester"]);

    header("Content-Type: application/json");
    echo json_encode([
        "requester"=> $requester,
        "userinfo"=> $userInfo
    ]);
    die();
}

function persistAttributes()
{
    session_start();

    if (!isset($_SESSION['id'])) {
        http_response_code(401);
        die('Request not valid');
    }

    $req = retrieveLoginRequest($_SESSION["id"]);

	//TODO: para que la URL sea dinámica, hay que crear el campo 'calbackurl' en la tabla requesters
	$requester = retrieveRequester($req["requester"]);
	$callbackBaseURL = $requester['callback'];
	
	//$callbackBaseURL = "http://vidchainpoc.azurewebsites.net/site/fake/student-detail.php?";
	
    $parameters = json_decode(file_get_contents('php://input', true), true);

    $scope = json_decode($req["scope"]);
    $attributes = array_intersect_key($parameters, array_fill_keys($scope, 0));
    $token = $parameters["token"];

    $callbackAttributes = $attributes;

    // If attributes contains a photo and the photo is not an url (it is a base64 encoding image), put a url to our server to serve the image
    if (isset($callbackAttributes[PHOTO_ATTRIBUTE]) && substr($callbackAttributes[PHOTO_ATTRIBUTE], 0,4) !== "http" ) {
        $callbackAttributes[PHOTO_ATTRIBUTE] = "http://vidchainpoc.azurewebsites.net/userphoto.php?id=".$_SESSION["id"];
    }

    $data = [
        "id" => $_SESSION['id'],
        "callback" => $callbackBaseURL . http_build_query(array_merge($callbackAttributes, ["token"=> $token])),
        "attributes" => $attributes,
    ];

    confirmLoginRequest($_SESSION['id'], $data, $token);
    die();
}

function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}