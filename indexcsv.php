<!DOCTYPE html>
<html>
	<head>
		<title>Página web</title>
		<link href="estilo.css" rel="stylesheet" type="text/css">
	</head>
	<body class="index">

	<div class="cajam">
	<p class="titulo">Menú</p>
	<select name="nindex" onchange="location = this.value">
	<option value="index.php">Tablas de flujos</option> 
	<option value="indexgrupos.php">Tabla de grupos</option> 
	<option value="indexcsv.php" disabled selected>Tabla de datos formato csv</option> 
	</select> 
	</div> 

	<div class="caja">
	<p class="titulo">Formulario para fichero csv</p>
	<form action="accion-csv.php" method="post">
	<label>file (.csv): </label><input class="input" type="text" name="filecsv" placeholder="ruta al fichero csv que contiene datos"/><br>
	<p><input type="submit" value="Submit"/></p>
	</form>
	</div>


	</body>
</html>
