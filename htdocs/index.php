<?php
$status = substr(file_get_contents("../current_status"),0,1);
?>
<html>
	<head>
		<title>Munich Maker Lab - Lab Status</title>
	</head>
	<body>
		<h1>Munich Maker Lab - Lab Status</h1>
		<?php if ($status == "1" ) { ?>
			<img src="open.png">
			<p>The lab is currently open.<br>If you don't have a key, call 089-21553954.</p>
		<?php } elseif  ($status == "0") { ?>
			<img src="closed.png">
			<p>The lab is currently closed.</p>
		<?php } else { ?>
			<img src="unknown.png">
			<p>The status of the lab is currently unknown.</p>
		<?php } ?>
	</body>
</html>

