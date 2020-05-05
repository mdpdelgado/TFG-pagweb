<!DOCTYPE html>
<html>
	<head>
		<title>Página web</title>
		<link href="estilo.css" rel="stylesheet" type="text/css">
	</head>
	<body class="index">
<?php
$salida =shell_exec("sudo ovs-vsctl show |grep Bridge");
#echo "<pre>$salida</pre>";
$arr1 = preg_split("/[\s,]+/", $salida);
#print_r($arr1);
$arr2 =array();
foreach ($arr1 as &$valor){
	if ($valor != null && $valor != "Bridge"){
		$valor2 = substr($valor, 1, -1);
		array_push ($arr2,$valor2);
	}
} 

#print_r($arr2);

unset($_SESSION['sw']);
unset($_SESSION['file']);
unset($_SESSION['profile']);
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(session_name(), '', time() - 42000,
        $params["path"], $params["domain"],
        $params["secure"], $params["httponly"]
    );
}
session_destroy();

?>

	<div class="cajam">
	<p class="titulo">Menú</p>
	<select name="nindex" onchange="location = this.value">
	<option value="index.php">Tablas de flujos</option> 
	<option value="indexgrupos.php" disabled selected>Tabla de grupos</option> 
	<option value="indexcsv.php">Tabla de datos formato csv</option> 
	</select> 
	</div> 

	<div class="caja">
	<p class="titulo">Formulario para el comando de tabla de grupos</p>
	<form action="accion-grupo.php" method="get">
	<p class="p1">Elegir entre un switch del escenario o el fichero txt:</p>
	<!--<label >sw: </label><input class="input" type="text" name="sw" placeholder="switch del que quieras la tabla de grupos"/><br><br>-->
	<label>sw: </label><select class="inputselect" name="sw">
		<option value="">switch del que quieras las tablas de flujos</option>
		<?php
		foreach($arr2 as $key => $value):
		echo '<option value="'.$value.'">'.$value.'</option>'; //close your tags!!
		endforeach;
		?>
	</select><br><br>

	<label >file (.txt): </label><input class="input" type="text" name="file" placeholder="ruta al fichero txt que contiene la tabla de grupos"/><br>
	<p class="p1">Elegir las columnas que quieras visualizar:</p>
	<label >columns: </label><input class="input" type="text" name="columns" placeholder="elige las columnas que quieres ver"/><br>
	<p><input type="submit" value="Submit"/></p>
	</form>
	</div>


	</body>
</html>
