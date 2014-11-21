<?php
$status = substr(file_get_contents("../current_status"),0,1);

if ($status == "1" ) {
	$status = "open";
} elseif  ($status == "0") {
	$status = "closed";
} else {
	$status = "unknown";
}

// Send header
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 19 Jul 1997 00:00:00 GMT');
header('Content-type: application/json; charset=utf-8');

// Fill data
$data = array(
	"door" => $status,
);

echo json_encode($data);

?>
