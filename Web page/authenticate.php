<?php
    $uname = trim($_POST["username"]);
    $upass = trim($_POST["password"]);
    
    $json_data->username = $uname;
    $json_data->password = $upass;

    $curl = curl_init();

    curl_setopt_array($curl, array(
    CURLOPT_URL => 'https://iasbot.azurewebsites.net/api/authenticate',
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
    // header("Content-Type: application/json");
    $json_response = json_decode($response);
    if($json_response->login == true) {
        session_start();
        $_SESSION['user'] = $uname;
        if($json_response->twoAuth == true){
            // echo "account 2fa enabled";
            $_SESSION["twoAuth"] = TRUE;
            $_SESSION["UOID"] = $json_response->UOID;
            header("location:/dashboard/2fa.php");
        }
        else {
            $_SESSION["twoAuth"] = FALSE;
            $_SESSION["UOID"] = $json_response->UOID;
            header("location:/dashboard/");
            // echo "account 2fa disabled";
        }
    }
    else {
        header("Location:/");
    }
    // echo json_encode($json_response->login);
?>