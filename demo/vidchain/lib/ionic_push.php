<?php

//define('IONIC_API_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1N2VmMGI1YS0wMjIyLTRiNDEtOTNhNy05OTE0ODdmZDEyYTUifQ.bMwlqFK9sH-HGrjVLwIxLpaIN7qMWbZw6STpIm09WD0');
//define('IONIC_URL', 'http://api.ionic.io');
//define('IONIC_PATH_PUSH_CREATE', '/push/notifications');
//define('IONIC_PUSH_PROFILE_TAG', 'vidchain');

define('FIREBASE_API_KEY', 'AIzaSyBizjmHYM0HRmWgdzS5UT2lOGxljBDgmgc');
define('FIREBASE_URL', 'https://fcm.googleapis.com/fcm/send');


function sendPushNotification($message, $payload, $token)
{
	/***** IONIC NOTIFICATION ****/
	/*
    $payload["content-available"] = 1;
    $_body = [
        "tokens" => [$token],
        "profile" => IONIC_PUSH_PROFILE_TAG,
        "notification" => ["message" => $message, "payload" => $payload]
    ];

    $_stringBody = json_encode($_body);

    $_curl = curl_init();
    curl_setopt_array($_curl, [
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => IONIC_URL.IONIC_PATH_PUSH_CREATE,
        CURLOPT_POST => 1,
        CURLOPT_POSTFIELDS => $_stringBody,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer '.IONIC_API_KEY,
            'Content-Type: application/json'
            ]
    ]);

    $result = curl_exec($_curl);
    curl_close($_curl);
	*/
	
	/***** FIREBASE NOTIFICATION *****/
	$_body = [
        "to" => $token,
        "notification" => [
			"body" => [
				"message" => $message, 
				"payload" => $payload
			], 
			"title" => "Education Diploma", 
			"content_available" => true, 
			"priority" => "high"
		],
		"data" => [
			"body" => [
				"message" => $message, 
				"payload" => $payload
			], 
			"title" => "Education Diploma", 
			"content_available" => true, 
			"priority" => "high"
		]
	];

    $_stringBody = json_encode($_body);
	$_curl = curl_init();
    curl_setopt_array($_curl, [
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => FIREBASE_URL,
        CURLOPT_POST => 1,
        CURLOPT_POSTFIELDS => $_stringBody,
        CURLOPT_HTTPHEADER => [
            'Authorization: Key='.FIREBASE_API_KEY,
            'Content-Type: application/json'
            ]
    ]);

    $result = curl_exec($_curl);
    curl_close($_curl);
    return $result;
}