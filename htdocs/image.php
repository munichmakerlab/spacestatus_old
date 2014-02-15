<?php

function sendFile($name) {
	$fp = fopen($name, 'rb');

	header("Content-Type: image/png");
	header("Content-Length: " . filesize($name));

	fpassthru($fp);
}

$status = substr(file_get_contents("../current_status"),0,1);
if ($status == "1" ) {
	sendFile("open.png");
} elseif  ($status == "0") {
	sendFile("closed.png");
} else {
	sendFile("unknown.png");
}
?>
