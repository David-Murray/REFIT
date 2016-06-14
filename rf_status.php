<!DOCTYPE html>
<html>
<head>
<style>
#header {
    background-color:grey;
    color:white;
    text-align:center;
    padding:5px;
}
table, th, td {
	border: 1px solid black;
}
</style>
</head>
<body>
<div id="header">
<a href="http://xxx.xxx.xxx.xxx/rf_status.php">Check Scripts</a>
<a href="http://xxx.xxx.xxx.xxx/rf_graph.php">Check Graph</a>
</div>
<?php
$servername = "xxxx";
$username = "xxxx";
$password = "xxxx";
$dbname = "xxxx";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error){
	die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT houseInfo.houseName, sensorInfo.houseID, sensorInfo.sensorALTID, sensorInfo.sensorName, sensorInfo.lastUpdate
FROM sensorInfo
INNER JOIN houseInfo
ON sensorInfo.houseID=houseInfo.houseID;";
$result = $conn->query($sql);

if ($result->num_rows > 0){
	echo "<table><tr><th>House</th><th>ID</th><th>Sensor</th><th>Name</th><th>lastUpdate</th>";
	while ($row = $result->fetch_assoc()){
		echo "<tr><td>".$row["houseName"]."</td><td>".$row["houseID"]."<td>".$row["sensorALTID"]."</td><td>".$row["sensorName"]."</td><td>".$row["lastUpdate"]."</td><tr>";
	}
	echo "</table>";
} else {
	echo "0 results (It's all gone wrong)";
}
$conn->close();
?>
</body>
</html>
