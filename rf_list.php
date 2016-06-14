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
<a href="http://xxx.xxx.xxx.xxx/rf_status.php">Check Sensors</a>
<a href="http://xxx.xxx.xxx.xxx/rf_graph.php">Check Graph<br /></a>
<?php
$bytes = disk_free_space(".");
    $si_prefix = array( 'B', 'KB', 'MB', 'GB', 'TB', 'EB', 'ZB', 'YB' );
    $base = 1024;
    $class = min((int)log($bytes , $base) , count($si_prefix) - 1);
    echo sprintf('%1.2f' , $bytes / pow($base,$class)) . ' ' . $si_prefix[$class] . '<br />';
?>
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

$sql = "SELECT houseInfo.houseName, scriptInfo.houseID, scriptInfo.scriptTime
FROM scriptInfo
INNER JOIN houseInfo
ON scriptInfo.houseID=houseInfo.houseID;";
$result = $conn->query($sql);

if ($result->num_rows > 0){
    echo "<table><tr><th>House</th><th>ScriptID</th><th>scriptTime</th><th>Check</th>";
    while ($row = $result->fetch_assoc()){
        $x = time() - $row["scriptTime"];
        echo "<tr><td>".$row["houseName"]."</td><td>".$row["houseID"]."</td><td>".$row["scriptTime"]."</td><td>".$x."</td><tr>";
    }
    echo "</table>";
} else {
    echo "0 results (It's all gone wrong)";
}
$conn->close();
?>
</body>
</html>
