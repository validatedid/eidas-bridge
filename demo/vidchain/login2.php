<?php

$qrId = run();

function run()
{
    checkMethod('GET');

    try {
        $qrId = $_GET['p'];
    } catch (Exception $e) {
        http_response_code(400);
        die();
    }

    return $qrId;
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
    <title>ViDChain</title>
    <meta name="description" content="ViDChain sample site">
    <meta name="author" content="ViDChain">

    <!-- Mobile Specific Metas
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- FONT
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
    <link href="//fonts.googleapis.com/css?family=Roboto" rel="stylesheet">

    <!-- JS
    -------------------------------------------------- -->
    <script
        src="https://code.jquery.com/jquery-3.2.1.min.js"
        integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4="
        crossorigin="anonymous"></script>
    <script src="./js/vidchain_login.js"></script>

    <!-- Favicon
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link rel="icon" type="image/png" href="./img/favicon.ico">

</head>
<body class="vidchain">

<!-- Primary Page Layout
–––––––––––––––––––––––––––––––––––––––––––––––––– -->
<div class="container">
    <div>
        <div class="offset-by-four four columns" style="margin-top: 5%; margin-bottom: 5%;text-align: center; color:white;">        
                <img id="qr-code" class="qr" src="<?php echo "http://localhost:8080/vidchain/qr.php?id=".$qrId; ?>"/>
                <p id="qr-explanation" class="qr">Please, scan QR Code with ViDChain in order to login</p>
        </div>
    </div>
</div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
<script> var qrId = "<?php echo $qrId;?>"</script>
</html>