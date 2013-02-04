<!-- Copyright (c) 2013 Katherine Erickson -->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html>
	<?php include("includes/head.php"); ?>
	<body id='index'>
		<div id='content'>
		    <?php include("includes/header.php"); ?>
		    
		    <?php 
		        // get the strain name from the URL
			    $protein = mysql_real_escape_string($_GET["protein"]);
			?>
		    <h2><?php echo $protein;?></h2>
		</div>
	</body>
</html>