<?php
$status = substr(file_get_contents("../current_status"),0,1);
if ($status == "1" ) {
	echo "open";
} elseif  ($status == "0") {
	echo "closed";
} else {
	echo "unknown";
}
?>
