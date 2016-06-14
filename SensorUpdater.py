#!/usr/bin/python3
""" Updates all houses current sensors """

import urllib.request, urllib.error, urllib.parse
import json
import mysql.connector
from mysql.connector import errorcode
import time

connectionConfig = {
    'user': 'xxxx',
    'password': 'xxxx',
    'host': 'xxxx',
    'database': 'xxxx'
}

try:
    sensor_connection = mysql.connector.connect(**connectionConfig)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor_house = sensor_connection.cursor(buffered=True)
cursor_edit = sensor_connection.cursor(buffered=True)
cursor_query = sensor_connection.cursor(buffered=True)

## SQL Queries
##
house_getter_sql = (
    "SELECT houseID, houseServer FROM houseInfo"
)

sensor_check_sql = (
    "SELECT houseID, sensorALTID FROM sensorInfo "
    "WHERE houseID=%(houseID)s AND sensorALTID=%(sensorALTID)s "
)

sensor_insert_sql = (
    "INSERT INTO sensorInfo "
    "(houseID, sensorID, sensorALTID, sensorName, sensorCategory, lastUpdate) "
    "VALUES (%(houseID)s, %(sensorID)s, %(sensorALTID)s, "
    "%(sensorName)s, %(sensorCategory)s, %(lastUpdate)s)"
)

sensor_update_sql = (
    "UPDATE sensorInfo "
    "SET "
    "sensorID=%(sensorID)s, "
    "sensorName=%(sensorName)s, "
    "lastUpdate=%(lastUpdate)s "
    "WHERE "
    "houseID=%(houseID)s "
    "AND "
    "sensorALTID=%(sensorALTID)s"
)

## Scripts
def sensor_insert():
    """ Inserts newly discovered sensors"""
    cursor_house.execute(house_getter_sql)
    for (houseID, houseServer) in cursor_house:
        urlIns = ("http://{}/uuuu/pppp/{}/data_request?id=sdata"
                  .format(houseServer, houseID))
        sensor_ins = urllib.request.urlopen(urlIns).read().decode("utf-8")
        try:
            sensorDataInsert = json.loads(sensor_ins)
        except ValueError:
            continue
        for i in sensorDataInsert['devices']:
            cursor_query.execute(sensor_check_sql, {'houseID': houseID,
                                                    'sensorALTID':i['altid']})
            Query = cursor_query.fetchall()
            if not Query:
                cursor_edit.execute(sensor_insert_sql,
                                    {'houseID':houseID,
                                     'sensorID':i['id'],
                                     'sensorALTID':i['altid'],
                                     'sensorName':i['name'],
                                     'sensorCategory':i['category'],
                                     'lastUpdate':time.strftime('%Y-%m-%d %H:%M:%S')})
                sensor_connection.commit()

def sensor_update():
    """ Updates existing sensors for changes"""
    cursor_house.execute(house_getter_sql)
    for (houseID, houseServer) in cursor_house:
        urlUp = ("http://{}/refitvera/Smartdata2013/{}/data_request?id=sdata"
                 .format(houseServer, houseID))
        sensor_upd = urllib.request.urlopen(urlUp).read().decode("utf-8")
        try:
            sensorDataInsert = json.loads(sensor_upd)
        except ValueError:
            continue
        for i in sensorDataInsert['devices']:
            cursor_edit.execute(sensor_update_sql,
                                {'houseID':houseID,
                                 'sensorID':i['id'],
                                 'sensorALTID':i['altid'],
                                 'sensorName':i['name'],
                                 'sensorCategory':i['category'],
                                 'lastUpdate':time.strftime('%Y-%m-%d %H:%M:%S')})
            sensor_connection.commit()

if __name__ == '__main__':
    sensor_insert()
    sensor_update()
    sensor_connection.close()
