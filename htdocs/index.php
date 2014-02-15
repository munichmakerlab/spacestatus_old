<?php
$status = substr(file_get_contents("../current_status"),0,1);
if ($status == "1" ) {
	echo "The Munich Maker Lab is currently open.";
} elseif  ($status == "0") {
	echo "The Munich Maker Lab is currently closed.";
} else {
	echo "unknown";
}
?>
