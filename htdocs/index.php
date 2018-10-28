<?php
$status = substr(file_get_contents("../current_status"),0,1);
?>
<html>
	<head>
		<title>Munich Maker Lab - Lab Status</title>
		<link href="capsule.css" rel=stylesheet>
	</head>
	<body>
		<header>
			<h1>Munich Maker Lab - Lab Status</h1>
			<nav>
				<a href="https://munichmakerlab.de">Home</a>
				<a href="https://wiki.munichmakerlab.de">Wiki</a>
				<a href="https://munichmakerlab.de/contact.html">Contact</a>
			</nav>
		</header>
		<main>
		<section><article>
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
		</article>
		</section>
		<section>
		<article>
		<h2>Temperature</h2>
		<iframe src="https://graphs.maqn.de/dashboard-solo/db/mumalab-climate?panelId=1&theme=light" width="450" height="200" frameborder="0"></iframe>
		<p><a href="https://graphs.maqn.de/dashboard/db/mumalab-climate">Lab Climate Dashboard</a></p>
		</article>
		</section>
		</main>
		<footer>
<a href="https://munichmakerlab.de/imprint.html">Impressum/Imprint</a> - <a href="https://munichmakerlab.de/privacy.html">Datenschutzerklärung/Privacy Policy</a>
		</footer>
	</body>
</html>

