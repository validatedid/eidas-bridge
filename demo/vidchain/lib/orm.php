<?php

define('DB_SERVER', 'vidchainpoc-mysqldbserver.mysql.database.azure.com');
define('DB_USERNAME', 'mysqldbuser@vidchainpoc-mysqldbserver');
define('DB_PASSWORD', 'Vidhainpoc4389');
define('DB_DATABASE', 'mysqldatabasevidchainpoc');

define('VID_REQUEST', 'request');
define('VID_REQUESTER', 'requester');
define('VID_EMAIL_VALIDATION', 'mail_validation');

$db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);

if (mysqli_connect_errno()) {
    http_response_code(500);
    die('Cannot connect to DB');
}

function retrieveLoginRequest($id)
{
    global $db;
    $sql = mysqli_query(
        $db,
        "SELECT * FROM ".VID_REQUEST." WHERE id LIKE '$id'"
    );
    $row = mysqli_fetch_array($sql, MYSQLI_ASSOC);
    return $row;
}

function createLoginRequest($scope, $requester, $callback)
{
    global $db;
    $id = uniqid("vidchain_login");
    $parsedScope = json_encode($scope);

    $sql = mysqli_query($db, "INSERT INTO ".VID_REQUEST." (id, scope, requester, callback) VALUES ('$id', '$parsedScope', '$requester', '$callback')");
    return $sql ? $id : false;
}

function confirmLoginRequest($id, $data, $token)
{
    global $db;
    $parsedData = json_encode($data);
    $sql = mysqli_query($db, "UPDATE ".VID_REQUEST." SET data = '$parsedData', token = '$token', result = 1 WHERE id LIKE '$id'");
    return $sql;
}

function retrieveRequester($id)
{
    global $db;
    $sql = mysqli_query(
        $db,
        "SELECT * FROM ".VID_REQUESTER." WHERE id LIKE '$id'"
    );
    $row = mysqli_fetch_array($sql, MYSQLI_ASSOC);
    return $row;
}

function createEmailValidationRequest($code, $email)
{
    global $db;

    $id = uniqid("vidchain_email_validation");
    $sql = mysqli_query($db, "INSERT INTO ".VID_EMAIL_VALIDATION." (id, code, email, createdAt) VALUES ('$id', '$code', '$email', now())");

    return $sql ? $id : false;
}

function retrieveEmailValidationRequest($id)
{
    global $db;
    $sql = mysqli_query(
        $db,
        "SELECT * FROM ".VID_EMAIL_VALIDATION." WHERE id LIKE '$id'"
    );
    $row = mysqli_fetch_array($sql, MYSQLI_ASSOC);
    return $row;
}

function updateEmailValidationRequest($id, $status)
{
    global $db;
    $sql = mysqli_query(
        $db,
        "UPDATE  ".VID_EMAIL_VALIDATION." SET status = '$status', updatedAt = now() WHERE id LIKE '$id'"
    );
    return $sql;
}