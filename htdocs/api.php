<?php
$status = substr(file_get_contents("../current_status"),0,1);
$people_count = json_decode(file_get_contents('https://flows.yt.gl/e0f75639-6d30-429a-9553-2bc0c130cc66/lab_state'));

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
	"people" => array(
		"present" => $people_count->persons_present,
		"allowed" => $people_count->persons_allowed
	)
);

echo json_encode($data);

?>
