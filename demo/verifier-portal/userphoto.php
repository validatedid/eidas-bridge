<?php

/**
 * GET /userphoto
 *
 * Query Params:
 *      * id => Request id
 */

define("PHOTO_ATTRIBUTE", "photo");
define("REQUEST_ATTRIBUTES", "attributes");
define("REQUEST_DATA", "data");
define("REQUEST_SCOPE", "scope");

include_once "lib/orm.php";

run();

function run()
{
    checkMethod(['GET', 'OPTIONS']);

    try {
        $_id = $_GET['id'];
    } catch (Exception $e) {
        http_response_code(400);
        die();
    }

    $_result = retrieveUserPhoto($_id);

    if (is_null($_result)) {
        $_result = file_get_contents('default_user.jpeg');
    }

    header("Content-Type: image/jpeg");
    echo $_result;
    die();
}

function retrieveUserPhoto($_id)
{
    $_request = retrieveLoginRequest($_id);
    if (is_null($_request)) {
        return null;
    }

    $_scope = json_decode($_request[REQUEST_SCOPE]);
    if (!in_array(PHOTO_ATTRIBUTE, $_scope)) {
        return null;
    }

    $_data = json_decode($_request[REQUEST_DATA], true);
    if (!isset($_data[REQUEST_ATTRIBUTES][PHOTO_ATTRIBUTE])) {
        return null;
    }

    return base64_decode($_data[REQUEST_ATTRIBUTES][PHOTO_ATTRIBUTE]);
}

function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}