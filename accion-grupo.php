<!DOCTYPE html>
<html>
	<head>
		<title>Página web</title>
		<link href="estilo.css" rel="stylesheet" type="text/css">
		<!-- choose a theme file -->
		<link rel="stylesheet" href="tablesorter-master/css/theme.blue.css">
		<!-- load jQuery and tablesorter scripts -->
		<script type="text/javascript" src="jquery-3.4.1.js"></script>
		<script type="text/javascript" src="tablesorter-master/js/jquery.tablesorter.js"></script>

		<!-- tablesorter widgets (optional) -->
		<script type="text/javascript" src="tablesorter-master/js/jquery.tablesorter.widgets.js"></script>
		<script type="text/javascript" src="tablesorter-master/js/widgets/widget-columnSelector.js"></script>
	</head>
	<body class="accion">

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
	?>


	<?php
	$str = "python3 tablaGrupos.py";
	$str2 = "Tabla de grupos del";
	session_start();

	if(!empty($_GET['sw'])){
	  $sw= $_GET['sw'];
	  $str .= " --sw $sw";
	  $str2 .= " sw: $sw";
	  $_SESSION ['sw'] = $_GET['sw'];
	}elseif(!empty($_SESSION ['sw'])){
	  $sw = $_SESSION ['sw'];
	  $str .= " --sw $sw";
	  $str2 .= " sw: $sw";
	}

	if(!empty($_GET['file'])){
	  $file= $_GET['file'];
	  $str .= " --file $file";
	  $str2 .= " file: $file";
	  $_SESSION ['file'] = $_GET['file'];
	}elseif(!empty($_SESSION ['file'])){
 	  $file= $_SESSION ['file'];
	  $str .= " --file $file";
	  $str2 .= " file: $file";
	}
	
	if(!empty($_GET['columns'])){
	  $columns= $_GET['columns'];
	  $str .= " --columns $columns";
	  $str2 .= " columns: $columns";
	}
	#echo '<p class="cmd">'.$str.'</p>';
	$salida =shell_exec($str);
	#echo "<pre>$salida</pre>";
	?>
	

	<?php
		if ($str != "python3 tablaGrupos.py"){
	?>
	<div class="menu">
		<div class="botones" >
		<a href="indexgrupos.php"><input type="button" value="Volver" onclick="resetcol()"></a>
		<input type="button" value="refrescar" onclick="javascript:window.location.reload();" />
		<br><br>
		</div>
		
		<?php if(!empty($_GET['sw']) or !empty($_SESSION ['sw'])){
		?>
		<div class="caja3" >
			<form action="accion-grupo.php" method="get">
			<p class="p3">Cambiar de sw</p>
			<select class="inputselect" name="sw" style="width: 320px;">
				<option value="">switch del que quieras la tabla de grupos</option>
				<?php
				foreach($arr2 as $key => $value):
				echo '<option value="'.$value.'">'.$value.'</option>'; //close your tags!!
				endforeach;
				?>
			</select>
			
			<p><input type="submit" value="Submit"/></p>
			</form>
		</div>
		<div class="botones" >
		<a href="accion.php"><input type="button" value="Tablas flujos" onclick="resetcol()" style="margin-left:10px"></a>
		</div>	
		<?php }
		?>

	</div>
		
		<div class="menu">
		<div class="caja4">
			<p class="p2">Seleccionar las columnas que quieras visualizar en la tabla</p>

			<div class="columnSelectorWrapper">
			  <input id="colSelect1" type="checkbox" class="hidden">
			  <!-- set "auto-on" here based on your initial auto mode -->
			 <label class="columnSelectorButton auto-on" for="colSelect1">Column</label>
			  <div id="columnSelector" class="columnSelector columnSelector2">
			    <!-- this div is where the column selector is added -->
			  </div>
			</div>
		</div>

		<div class="caja4" >
			<p class="p2">- La opción auto permite mostrar todas las colunmas de esa tabla</p>
			<p class="p2">- Desactivar la opción auto y activar/desactivar las columnas</p>
		</div>
		</div>
	<?php
	}else{?>
	<a href="indexgrupos.php"><input type="button" value="Volver"></a>
	<?php
	}
	?>

	<?php
	if ($str != "python3 tablaGrupos.py"){
	echo '<p class="titulo">'.$str2.'</p>';
	}else{
	echo '<p class="titulo">'.Ayuda.'</p>';
	}
	?>


	<?php
	if ($str != "python3 tablaGrupos.py"){
	$row = 1;
	if (($handle = fopen("pandasCSV.csv", "r")) !== FALSE) {
	   
	    echo '<table border="1" id="myTable" class="tablesorter" style="width:auto;text-align: center;">';
	   
	    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
		$num = count($data);
		if ($row == 1) {
		    echo '<thead><tr>';
		}else{
		 echo '<tr>';
		}
  
		for ($c=0; $c < $num; $c++) {
		    $value = $data[$c];
		    
		    if ($row == 1) {
		        echo '<th>'.$value.'</th>';
		    }else{
		        echo '<td  style="padding: 6px;">'.$value.'</td>';
		    }
		}
	       
		if ($row == 1) {
		    echo '</tr></thead><tbody>';
		}else{
		    echo '</tr>';
		}
		$row++;
	    }
	   
	    echo '</tbody></table>';
	    fclose($handle);
	}
	}else{
	?>	
		<div class="caja2">
		<p>Vuelve a la página principal y rellena algún campo del formulario</p>
		<p>sw: switch del que quieras la tabla de grupos</p>
		<p>file (.txt): ruta al fichero txt que contiene la tabla de grupos</p>
		<p>columns: elige las columnas que quieres ver</p>
		</div>
	<?php	
	}
	?>

	<script>
	$(function() {
	
		 $("#myTable").tablesorter({
    			    theme: 'blue',
			    // initialize zebra striping of the table
			    widgets: [ "resizable", "saveSort", "zebra", "stickyHeaders", "filter","columnSelector"],
			    // change the default striping class names
			    // updated in v2.1 to use widgetOptions.zebra = ["even", "odd"]
			    // widgetZebra: { css: [ "normal-row", "alt-row" ] } still works
			    widgetOptions : {
			      zebra : [ "normal-row", "alt-row" ],
			      filter_columnFilters : true,			      
			      storage_storageType : "s",
	       		      columnSelector_container : $("#columnSelector")
			    }
  		   });

		$('#myTable').on('columnUpdate', function() {
			var isAutoOn = $('#columnSelector input[data-column="auto"]').prop('checked');
		  $('.columnSelectorButton').toggleClass('auto-on', isAutoOn);
		});

	});
	</script>
	
	<script>
		function resetcol() {
			//$("#myTable").trigger('refreshColumnSelector', true);
			$("#myTable").trigger('refreshColumnSelector', [ 'auto', [0,1,2,3,4,5,6,7,8] ]);
		}
		
	</script>

	
	</body>
</html>
