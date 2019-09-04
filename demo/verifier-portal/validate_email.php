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
include_once "lib/vidchain_mailer.php";

$funcs= [
    "POST" => "sendVerificationCode",
    "GET" => "confirmVerificationCode"
];

run();


function run()
{
    global $funcs;

    checkMethod(['GET', 'POST', 'OPTIONS']);
    call_user_func($funcs[$_SERVER['REQUEST_METHOD']]);
}

function sendVerificationCode()
{
    $_parameters = json_decode(file_get_contents('php://input', true), true);
    $_email = $_parameters["email"];
    $_verificationCode = mt_rand(100000, 999999);

    $_htmlBody = generateHtmlMessage($_verificationCode);
    $_plainBody = generatePlainMessage($_verificationCode);

    $error = null;
    try {
        $result = sendHtmlMail($_htmlBody, $_plainBody, $_email);
    } catch (Exception $e) {
        $result = false;
        $error = $e->getMessage();
    }

    $_id = null;
    if ($result) {
        $_id = createEmailValidationRequest($_verificationCode, $_email);
    }

    header('Content-Type: application/json');
    echo json_encode([
        "result" => $result,
        "request_id" => $_id,
        "error" => $error
    ]);
    die();
}

function confirmVerificationCode()
{
    $_parameters = $_GET;
    $_requestId = $_parameters['request_id'];
    $_verificationCode = $_parameters['verification_code'];

    $_validationRequest = retrieveEmailValidationRequest($_requestId);
    $_correctValidationCode = $_validationRequest['code'];

    $_status = $_correctValidationCode === $_verificationCode ? 'verified' : 'failed';
    updateEmailValidationRequest($_requestId, $_status);

    header('Content-Type: application/json');
    echo json_encode([
        "result" => $_status,
        "request_id" => $_requestId
    ]);
    die();
}

function generateHtmlMessage($code)
{
    return "Verification code: ".$code;
}

function generatePlainMessage($code)
{
    return "Verification code: ".$code;
}

function checkMethod($methods)
{
    if (!in_array($_SERVER['REQUEST_METHOD'], $methods)) {
        http_response_code(405);
        die('Method not allowed');
    }
}