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

	<a href="indexcsv.php"><input type="button" value="Volver" onclick="resetcol()"></a>

	<?php
	
	$str2 = "Tabla de datos en formato csv: ";

	if(!empty($_POST['filecsv'])){
	  $filecsv= $_POST['filecsv'];
	  $str2 .= "$filecsv";
	  $aux = "cp $filecsv pandasCSV.csv"; 
	  $copiar =shell_exec($aux);
	?>

		<div class="menu">
		<div class="caja4">
			<p class="p2">Seleccionar las columnas que quieras visualizar en la tabla</p>

			<div class="columnSelectorWrapper">
			  <input id="colSelect1" type="checkbox" class="hidden">
			  <!-- set "auto-on" here based on your initial auto mode -->
			 <label class="columnSelectorButton auto-on" for="colSelect1">Column</label>
			  <div id="columnSelector" class="columnSelector">
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
	  echo '<p class="titulo">'.$str2.'</p>';
	}else{
	  echo '<p class="titulo">'.Ayuda.'</p>';
	}
	?>

	<?php
	if (!empty($_POST['filecsv'])){
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
		<p>Vuelve a la página principal y rellena el formulario</p>
		<p>file (.csv): ruta al fichero csv que contiene datos</p>
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
			$("#myTable").trigger('refreshColumnSelector', [ 'auto', [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22] ]);
		}
		
	</script>
	
	</body>
</html>
