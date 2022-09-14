<?php

function getDeviceStatus($device) {
	    $url = "https://wiki.munichmakerlab.de/index.php?title=" . $device . "&action=edit";
	    $raw = file_get_contents($url);
	    preg_match_all('/\{\{(ThingInfoBox|project)(.+?)\}\}/s', $raw, $matches);
		$result = array();
		foreach ($matches[2] as $entry) {
			foreach ((explode(PHP_EOL, $entry)) as $line) {
				if(!str_contains($line, "=")) {
					continue;
				}
				$line = trim($line);
				$line = str_replace("|", "", $line);
				$foo = explode("=", $line, 2);
				$res[trim($foo[0])] = trim($foo[1]);
			}

			array_push($result, $res);
		}

		#echo $device . ": " .  $matches[1] . "\n";
		return $result;
	}

$data = array();
$names = array(
	"Lusa" => "Lusa (3D printer)",
	"Rusa" => "Rusa (3D printer)",
	"LaserCutter" => "Laser Cutter",
	"CNC Mill" => "CNC Mill",
);
foreach (['Prusa_Mini','LaserCutter', 'CNC_router_build'] as $device) {
	foreach (getDeviceStatus($device) as $entry) {
		$data[$names[$entry['name']]] =  $entry["status"];
	}
}

file_put_contents(__DIR__ . '/devices.json',  json_encode($data));

