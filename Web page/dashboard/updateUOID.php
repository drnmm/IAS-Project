<?php
    $uoid = trim($_POST["uoid"]);
    $uname = trim($_POST["username"]);
    
    $json_data->username = $uname;
    $json_data->uoid = $uoid;

    $curl = curl_init();

    curl_setopt_array($curl, array(
    CURLOPT_URL => 'https://iasbot.azurewebsites.net/api/backend?method=updateUOID',
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
    if($json_response->status == "Update done.") {
        session_start();
        $_SESSION["UOID"] = $uoid;
        header("location:/dashboard/");
    }
    else {
        header("Location:/dashboard/");
    }
?>