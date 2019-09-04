<?php

$data = run();

function run()
{
    checkMethod('GET');

    try {
        $_data = $_GET;
    } catch (Exception $e) {
        http_response_code(400);
        die();
    }

    return $_data;
}

function checkMethod($method)
{
    if ($_SERVER['REQUEST_METHOD'] != $method) {
        http_response_code(405);
        die('Method not allowed');
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="utf-8">
    <title>ViDChain Sample Site</title>
    <meta name="description" content="ViDChain sample site">
    <meta name="author" content="ViDChain">

    <!-- Mobile Specific Metas
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- FONT
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">

    <!-- CSS
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/bootswatch/3.3.1/united/bootstrap.min.css">
    <link rel="stylesheet" href="../assets/css/normalize.css">
    <link rel="stylesheet" href="../assets/css/skeleton.css">

    <!-- JS
    -------------------------------------------------- -->
    <script
            src="https://code.jquery.com/jquery-2.2.4.min.js"
            integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44="
            crossorigin="anonymous"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.1/js/bootstrap.min.js"></script>
    <script src="//rawgit.com/saribe/eModal/master/dist/eModal.min.js"></script>
    <script src="../assets/js/fake-login-success.js"></script>

    <!-- Favicon
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link rel="icon" type="image/png" href="../assets/images/favicon.png">

</head>
<body>

<!-- Primary Page Layout
–––––––––––––––––––––––––––––––––––––––––––––––––– -->
<div class="container">
    <div class="row">
        <div class="nine column" style="margin-top: 25%">
            <h2>Successful login</h2>
            <h4>¡Welcome to the amazing ViDChain experience!</h4>
            <p>Your data is:</p>
            <ul>
                <li>Name: <strong><?php echo $data['name'];?></strong></li>
                <li>Nif: <strong><?php echo $data['nif'];?></strong></li>
                <li>Email: <strong><?php echo $data['email'];?></strong></li>
                <li>Phone: <strong><?php echo $data['phone'];?></strong></li>
            </ul>
            <button id="validate-elicence" onclick="validateElicence(1, 'Software Enginyer License', '<?php echo $data['token'];?>')">Issue eLicense <span class="glyphicon glyphicon-refresh spinning"></span></button>
        </div>
    </div>
</div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
</html>