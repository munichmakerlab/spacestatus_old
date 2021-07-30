<?php

function getDeviceStatus($device) {
	    $url = "https://wiki.munichmakerlab.de/index.php?title=" . $device . "&action=edit";
	        $raw = file_get_contents($url);
	        preg_match('/status\s+=\s+(\S+)/', $raw, $matches);
//		echo $device . ": " .  $matches[1] . "\n";
		return $matches[1];
}

file_put_contents(__DIR__ . '/devices.json',  json_encode(array(
	"Lusa (3D printer)" => getDeviceStatus("Lusa"),
	"Rusa (3D printer)" => getDeviceStatus("Rusa"),
	"Lasercutter" => getDeviceStatus("LaserCutter"),
	"CNC Mill"=> getDeviceStatus("CNC_router_build")
)));
?>
