<?php
	session_start();
	if(isset($_SESSION['user'])){
		if(!$_SESSION["twoAuth"]){
			header("location:/dashboard/");
		}
		elseif($_SESSION["twoAuthDone"]){
			header("location:/dashboard/");
		}
	}
	else {
		header("location:/");
	}
	// if(!isset($_SESSION['user'])){
	// 	header("location:/");
	// }
	// else {
	// 	if(isset($_SESSION['twoAuth'])){
	// 		header("location:/dashboard/");
	// 	}
	// }
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta content="width=device-width, initial-scale=1.0" name="viewport">

	<title>Batangas State University - Student Portal</title>

	<meta property="og:title" content="Enrollment System">
	<meta property="og:description" content="A final project in System Integration and Architecture.">
	<meta property="og:image" content="https://blog.dranem.me/favicon.png">


	<link href="https://blog.dranem.me/favicon.png" rel="icon">
	<link href="https://blog.dranem.me/favicon.png" rel="apple-touch-icon">

	<link rel="stylesheet" type="text/css" href="../assets/css/sign-in-up.css">
	<link rel="stylesheet" type="text/css" href="style.css">

	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
	<!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"> -->

</head>
<body>
	<div class="container-fluid">
		<div class="row">
			<div class="col-lg-7 hero-img">
			</div>
			<div class="col-lg-5 input-section">
			
				<br><br>
				<h1>Two-Factor Authentication</h1>
				<br>
				
				<form class="user-form" action="auth.php" method="POST">
					<div class="inputField">
						<input type="number" placeholder=" " name="otp" autocomplete="on" onKeypress="if(this.value.length==7) return false;" required />
						<span>One Time Pin   </span>
					</div>
					<input type="hidden" name="username" value="<?php echo $_SESSION["user"]; ?>" >
					<div class="inputBtn">
						<input type="submit" name="submit" value="Log in" class="submit-btn">
					</div>
					<p style="color:#404040;">To logout, please click <a href="logout.php">here</a></p>

				</form>
			</div>
		</div>
	</div>
	
	</div><!-- 
	<footer>
		<p class="text-center">A Final Project in System Integration & Architecture.</p>
	</footer> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script> -->
</body>
</html>
