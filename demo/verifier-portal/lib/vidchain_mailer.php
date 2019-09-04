<?php

include_once "vendor/phpMailer/PHPMailer.php";
include_once "vendor/phpMailer/SMTP.php";
include_once "vendor/phpMailer/Exception.php";


define('MAILER_USERNAME', 'vidchain@validatedid.com');
define('MAILER_PASSWORD', 'C6lHww0x');
define('MAILER_FROM_MAIL', 'vidchain@validatedid.com');
define('MAILER_FROM_NAME', 'ViDChain');
define('MAILER_REPLY_TO_MAIL', 'no-reply@validatedid.com');
define('MAILER_REPLY_TO_NAME', 'ViDChain');


function getConfiguredMailer()
{
    $_mailer = new \PHPMailer\PHPMailer\PHPMailer(true);

    $_mailer->SMTPOptions = array(
        'ssl' => array(
            'verify_peer' => false,
            'verify_peer_name' => false,
            'allow_self_signed' => true
        )
    );

    $_mailer->isSMTP();
    $_mailer->SMTPDebug = 0;
    $_mailer->Host = 'smtp.gmail.com';
    $_mailer->Port = 587;
    $_mailer->SMTPSecure = 'tls';
    $_mailer->SMTPAuth = true;
    $_mailer->Username = MAILER_USERNAME;
    $_mailer->Password = MAILER_PASSWORD;

    $_mailer->setFrom(MAILER_FROM_MAIL, MAILER_FROM_NAME);
    $_mailer->addReplyTo(MAILER_REPLY_TO_MAIL, MAILER_REPLY_TO_NAME);

    return $_mailer;
}

function sendHtmlMail($htmlBody, $plainBody, $to)
{
    try {
        $_mailer = getConfiguredMailer();
        $_mailer->addAddress($to);
        $_mailer->Subject = '[ViDChain] Email Address Validation';
        $_mailer->msgHTML($htmlBody);
        $_mailer->AltBody = $plainBody;

        return $_mailer->send();
    } catch (\PHPMailer\PHPMailer\Exception $e) {
        throw new Exception($e->errorMessage());
    }
}