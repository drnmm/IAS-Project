<?php
    $otp = trim($_POST["otp"]);
    $uname = trim($_POST["username"]);
    
    $json_data->username = $uname;
    $json_data->otp = $otp;

    $curl = curl_init();

    curl_setopt_array($curl, array(
    CURLOPT_URL => 'https://iasbot.azurewebsites.net/api/backend?method=2FA',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_ENCODING => '',
    CURLOPT_MAXREDIRS => 10,
    CURLOPT_TIMEOUT => 0,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_2_0,
    CURLOPT_CUSTOMREQUEST => 'POST',
    CURLOPT_POSTFIELDS =>json_encode($json_data),
    CURLOPT_HTTPHEADER => array(
        'Content-Type: application/json'
    ),
    ));

    $response = curl_exec($curl);

    curl_close($curl);
    // echo $response;
    $json_response = json_decode($response);
    if($json_response->auth == true) {
        session_start();
        $_SESSION["twoAuthDone"] = TRUE;
        header("location:/dashboard/");
    }
    else {
        header("Location:/dashboard/2fa.php");
    }
?>