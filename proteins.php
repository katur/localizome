<!-- Copyright (c) 2013 Katherine Erickson -->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html>
	<?php include("includes/head.php"); ?>
	<body id='index'>
		<div id='content'>
		    <?php include("includes/header.php"); ?>
		    <h2>Protein List</h2>
		    <table id='proteins'>
		        <tr class='top-row'>
	        		<td>Common Name</td>
					<td>Canonical Name</td>
					<!--<td>Wormbase Gene ID</td>-->
				</tr>    
    		    <?php
    		        $query = "SELECT common_name, canonical_name 
    		            FROM protein 
    		            ORDER BY common_name
    		        ";
    		        // Run the query
					$result = mysql_query($query);
					if (!$result) {
						echo 'Could not run query: ' . mysql_error();
						exit;
					}
    		        // Retrieve results
					while ($row = mysql_fetch_assoc($result)) {
					    $common_name = $row['common_name'];
					    $canonical_name = $row['canonical_name'];
					    echo "<tr>
			    			<td><a href='/protein.php?protein=$common_name' class='all-caps'>$common_name</a></td>
							<td>$canonical_name</td>
							<!-- <td>$wormbase_id</td> -->
						</tr>";
					}
    		    ?>
		    </table>
		</div>
	</body>
</html>