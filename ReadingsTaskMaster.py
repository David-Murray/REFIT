#!/usr/bin/python3
import urllib.request, urllib.error, urllib.parse
import mysql.connector
import time
import subprocess

connectionConfig = {
	'user': 'xxxx',
	'password': 'xxxx',
	'host': 'xxxx',
	'database': 'xxxx'
}

scriptStart = time.time()
time.sleep(60)

try:
	taskmasterConnection = mysql.connector.connect(**connectionConfig)
except mysql.connection.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print ("Something is wrong with your username or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print ("Database does not exist")
	else:
		print (err)

cursorHouse = taskmasterConnection.cursor(buffered=True)
cursorQuery = taskmasterConnection.cursor(buffered=True)
cursorTime = taskmasterConnection.cursor(buffered=True)

time_check = (
	"SELECT scriptTime FROM scriptInfo "
	"WHERE houseID = %(houseID)s"
)

time_update = (
	"UPDATE scriptInfo "
	"SET scriptTime=%(scriptTime)s "
	"WHERE houseID = %(houseID)s"
)

house_getter = (
	"SELECT houseID, houseServer FROM houseInfo"
)

##Main

loop = 1
while loop == 1:
	cursorHouse.execute(house_getter)
	taskmasterConnection.commit()
	for (houseID, houseServer) in cursorHouse:
		cursorQuery.execute(time_check, {'houseID': houseID})
		taskmasterConnection.commit()
		scriptTime = cursorQuery.fetchone()[0]
		print (scriptStart)
		print (scriptTime)
		if scriptTime is None:
			scriptTime = 0
		delta = scriptTime - scriptStart
		if delta < 0:
			subprocess.Popen(["nohup", "/root/Readings.py", str(houseID), houseServer])
			scriptTime = time.time()
			print (houseID , houseServer , scriptTime, delta)
			cursorTime.execute(time_update, {'houseID':houseID, 'scriptTime': scriptTime})
			taskmasterConnection.commit()
	time.sleep(10)
