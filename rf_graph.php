<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Live Graph</title>
	<link href="style.css" rel="stylesheet" type="text/css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
	<script type="text/javascript" language="javascript" src="../flot/jquery.js"></script>
	<script type="text/javascript" language="javascript" src="../flot/jquery.flot.js"></script>
	<script type="text/javascript" language="javascript" src="../flot/jquery.flot.time.js"></script>
	<script type="text/javascript" src="/js/flot/jquery.flot.stack.js"></script>
	<script type="text/javascript" src="/js/flot/jquery.flot.symbol.js"></script>
	<script type="text/javascript" src="/js/flot/jquery.flot.axislabels.js"></script>

	<?php
	$servername = "xxxx";
	$username = "xxxx";
	$password = "xxxx";
	$dbname = "xxxx";

	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error){
		die("Connection Failed: " . $conn->connect_error);
	}
	function get_Data($houseID, $ALTID, $conn)
	{
		$sql = "SELECT UNIX_TIMESTAMP(serverTime), readingWatts FROM powerReadings WHERE houseID = $houseID AND sensorALTID = '$ALTID' ORDER BY serverTime DESC LIMIT 450";
		$result = $conn->query($sql);
		if ($result)
		{
			while ($row=$result->fetch_assoc())
			{
				$data_Set[] = array($row['UNIX_TIMESTAMP(serverTime)']*1000,$row['readingWatts']);
			}
		}
		return $data_Set;
	}

    function get_Data_Label($houseID, $ALTID, $conn)
    {
        $sql = "SELECT sensorName FROM sensorInfo WHERE houseID = $houseID AND sensorALTID = '$ALTID' ";
        $result = $conn->query($sql);
        if ($result)
        {
            while ($row=$result->fetch_assoc())
            {
                $data_Set_Label = $row['sensorName'];
            }
        }
        return $data_Set_Label;
    }

    $houseID = $_POST["houseID"];
    $ALTID = "Appliance0";
    $data_Set = get_Data($houseID, $ALTID, $conn);
    $data_Set_Label = get_Data_Label($houseID, $ALTID, $conn);
    ?>

    <script type="text/javascript">
      $(function(){
       var dataset1 = <?php echo json_encode($data_Set); ?>;
       var dataset1_Label = <?php echo json_encode($data_Set_Label); ?>;
       $.plot($("#placeholder"), [ {label: dataset1_Label, data: dataset1} ], {
        series: {
         stack: true,
         lines: {
          show: true,
          fill: true
      }
  },
  xaxis: {
     mode: "time",
     timezone: "browser",
     timeformat: "%y/%m/%d %H:%M:%S",
     axisLabel: "Date",
     axisLabelUseCanvas: true,
     axisLabelFontSizePixels: 10,
     axisLabelFontFamily: 'Verdana, Arial',
     axisLabelPadding: 10
 },
 yaxis: {
     axisLabel: "Power (Watts)",
     axisLabelUseCanvas: true,
     axisLabelFontSizePixels: 10,
     axisLabelFontFamily: 'Verdana, Arial',
     axisLabelPadding: 3
 },
 grid: {
     hoverable: false,
     borderWidth: 2,
     backgroundColor: {
      colors: ["#EDF5FF", "#ffffff"]
  }
}
});
   });
  </script>
</head>
<body>
	<div id="header">
		<a href="http://xxx.xxx.xxx.xxx/rf_list.php">Check Sensors</a>
		<a href="http://xxx.xxx.xxx.xxx/rf_status.php">Check Scripts</a>
		<h2>Power
			<?php
			if ($_POST["houseID"]){
				$sqlHead = "SELECT houseName FROM REFIT.houseInfo WHERE houseID = $houseID";
				$resultHead = $conn->query($sqlHead);
				while ($rowHead = $resultHead->fetch_assoc()){
					echo $rowHead['houseName'];
				}
			}else{
				echo "Nothing Selected";
			}
			?>
			,
			Aggregate
			<?php
			$sql2 = "SELECT houseID, houseName FROM REFIT.houseInfo";
			$result2 = $conn->query($sql2);
			echo "<form action=\"testlist.php\" method=\"post\">";
			echo "<select name='houseID'>";
			while ($row2 = $result2->fetch_assoc()) {
				echo "<option value=\"{$row2['houseID']}\">";
				echo $row2['houseName'];
				echo "</option>";
			}
			echo "</select>";
			echo "<input type=\"submit\" />";
			echo "</form>";
			$conn->close();
			?>
		</h2>
	</div>

	<div id="content">
		<div class="demo-container">
			<div id="placeholder" class="demo-placeholder"></div>
		</div>
	</div>

</body>
</html>
