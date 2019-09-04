<?php

/**
 * GET /qr
 *
 * Query Params:
 *      * id => Request id
 */

include('./vendor/phpqrcode/qrlib.php');

run();

function run()
{
    checkMethod(['GET', 'OPTIONS']);
    $backColor = 0xFFFF00;
    $foreColor = 0xffffff;

    try {
        $_requestId = $_GET['id'];
    } catch (Exception $e) {
        http_response_code(400);
        die();
    }

    die(QRcode::svg($_requestId,false, 'L', 9, 2, false, false, $foreColor));

}

function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}