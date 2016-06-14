#!/usr/bin/python3
import argparse
import urllib.request, urllib.error, urllib.parse
import json
import mysql.connector
import time

parser = argparse.ArgumentParser()
parser.add_argument("houseID", help = "houseID")
parser.add_argument("houseServer", help = "houseServer")
args = parser.parse_args()

connectionConfig = {
    'user': 'xxxx',
    'password': 'xxxx',
    'host': 'xxxx',
    'database': 'xxxx'
}

try:
    readingsConnection = mysql.connector.connect(**connectionConfig)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print ("Something is wrong with your user-name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print ("Database does not exist")
    else:
        print (err)

cursorInsert = readingsConnection.cursor(buffered=True)
cursorTime = readingsConnection.cursor(buffered=True)

reading_Insert = (
    "INSERT INTO sensorReadings "
    "(houseID, sensorALTID, readingWatts, readingTemperature, readingLight, readingHumidity, readingArmed, readingTripped, readingLastTrip, readingStatus, readingKWH, readingBattery, serverTime) "
    "VALUES (%(houseID)s, %(sensorALTID)s, %(readingWatts)s, %(readingTemperature)s, %(readingLight)s, %(readingHumidity)s, %(readingArmed)s, %(readingTripped)s, %(readingLastTrip)s, %(readingStatus)s, %(readingKWH)s, %(readingBattery)s, %(serverTime)s) "
    )

power_Insert = (
    "INSERT INTO powerReadings "
    "(houseID, sensorALTID, readingWatts, readingTemperature, serverTime) "
    "VALUES (%(houseID)s, %(sensorALTID)s, %(readingWatts)s, %(readingTemperature)s, %(serverTime)s) "
    )

time_Update = (
    "UPDATE scriptInfo "
    "SET scriptTime=%(scriptTime)s "
    "WHERE houseID = %(houseID)s"
)

def get_Data():
    try:
        urlReadings = ("http://{}/uuuu/pppp/{}/data_request?id=sdata&loadtime=0&dataversion=0".format(args.houseServer, args.houseID))
        readingsContent = urllib.request.urlopen(urlReadings).read().decode("utf-8")
        readingsInsert = json.loads(readingsContent)
        return readingsInsert
    except:
        readingsInsert = None
        return readingsInsert

## Main
while True:
    readingsInsert = get_Data()
    if not readingsInsert:
        print ("Nothing was returned from MIOS")
        time.sleep(5)
        pass
    elif 'devices' in readingsInsert:
        for i in readingsInsert['devices']:
            if 'altid' in i:
                if i['altid']:
                    sensorALTID = i['altid']
                    print(sensorALTID)
                    readingTime = None
                    readingWatts = None
                    readingTemperature = None
                    readingLight = None
                    readingHumidity = None
                    readingArmed = None
                    readingTripped = None
                    readingLastTrip = None
                    readingStatus = None
                    readingKWH = None
                    readingBattery = None
                    if 'watts' in i:
                        readingWatts = i['watts']
                    if 'temperature' in i:
                        readingTemperature = i['temperature']
                    if 'light' in i:
                        readingLight = i['light']
                    if 'humidity' in i:
                        readingHumidity = i['humidity']
                    if 'armed' in i:
                        readingArmed = i['armed']
                    if 'tripped' in i:
                        readingTripped = i['tripped']
                    if 'lasttrip' in i:
                        readingLastTrip = i['lasttrip']
                    if 'status' in i:
                        readingStatus = i['status']
                    if 'kwh' in i:
                        readingKWH = i['kwh']
                    if 'batterylevel' in i:
                        readingBattery = i['batterylevel']
                    # This decides if it is a CurrentCost IAM or other Sensor
                    if (readingWatts and readingTemperature) and not (readingLight and readingHumidity and readingArmed and readingTripped and readingLastTrip and readingBattery):
                        try:
                            cursorInsert.execute(power_Insert, {
                                'houseID':args.houseID,
                                'sensorALTID':sensorALTID,
                                'readingWatts':readingWatts,
                                'readingTemperature':readingTemperature,
                                'serverTime':time.strftime('%Y-%m-%d %H:%M:%S')})
                        except:
                            print("Didn't Insert Power Reading")
                            pass
                    elif (readingWatts or readingTemperature or readingLight or readingHumidity or readingArmed or readingTripped or readingLastTrip or readingBattery or readingStatus or readingKWH):
                        try:
                            cursorInsert.execute(reading_Insert, {
                                'houseID':args.houseID,
                                'sensorALTID':sensorALTID,
                                'readingWatts':readingWatts,
                                'readingTemperature':readingTemperature,
                                'readingLight':readingLight,
                                'readingHumidity':readingHumidity,
                                'readingArmed':readingTripped,
                                'readingTripped':readingTripped,
                                'readingLastTrip':readingLastTrip,
                                'readingStatus':readingStatus,
                                'readingKWH':readingKWH,
                                'readingBattery':readingBattery,
                                'serverTime':time.strftime('%Y-%m-%d %H:%M:%S')})
                        except:
                            print("Didn't Insert Sensor Reading")
                            pass
        cursorTime.execute(time_Update, { 'houseID':args.houseID, 'scriptTime':time.time()})
        readingsConnection.commit()
        time.sleep(6)